from collections.abc import Callable
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlmodel import Session

from fastapi_myauth import crud, models, security
from fastapi_myauth.config import settings
from fastapi_myauth.email import (
    send_magic_login_email,
    send_reset_password_email,
)

router = APIRouter()

"""
https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Authentication_Cheat_Sheet.md
Specifies minimum criteria:
    - Change password must require current password verification to ensure that it's the legitimate user.
    - Login page and all subsequent authenticated pages must be exclusively accessed over TLS or other strong transport.
    - An application should respond with a generic error message regardless of whether:
        - The user ID or password was incorrect.
        - The account does not exist.
        - The account is locked or disabled.
    - Code should go through the same process, no matter what, allowing the application to return in approximately
      the same response time.
    - In the words of George Orwell, break these rules sooner than do something truly barbaric.

See `security.py` for other requirements.
"""


def get_login_router(
    user_model: type[models.User],
    user_read: type[models.UserRead],
    user_create: type[models.UserCreate],
    user_update: type[models.UserUpdate],
    crud_user: crud.crud_user.CRUDUser,
    deps: dict[str, Callable],
) -> APIRouter:
    router = APIRouter()

    @router.post("/signup", response_model=user_read)
    def create_user_profile(
        *,
        db: Annotated[Session, Depends(deps["SessionDep"])],
        password: Annotated[str, Body()],
        email: Annotated[EmailStr, Body()],
        full_name: str = Body(None),
    ) -> Any:
        """
        Create new user without the need to be logged in.
        """
        if not settings.USERS_OPEN_REGISTRATION:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Registration is closed.",
            )
        user = crud_user.get_by_email(db, email=email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username is not available.",
            )
        # Create user auth
        user_in = user_create(password=password, email=email, full_name=full_name)
        user = crud_user.create(db, obj_in=user_in)
        return user

    @router.post("/magic/{email}")
    def login_with_magic_link(
        *, db: Annotated[Session, Depends(deps["SessionDep"])], email: str
    ) -> models.WebToken:
        """
        First step of a 'magic link' login. Check if the user exists and generate a magic link. Generates two short-duration
        jwt tokens, one for validation, one for email. Creates user if not exist.
        """
        user = crud_user.get_by_email(db, email=email)
        if not user:
            if not settings.USERS_OPEN_REGISTRATION:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Registration is closed.",
                )
            user_in = user_create(email=email)
            user = crud_user.create(db, obj_in=user_in)
        if not crud_user.is_active(user):
            # Still permits a timed-attack, but does create ambiguity.
            raise HTTPException(
                status_code=400,
                detail="A link to activate your account has been emailed.",
            )
        tokens = security.create_magic_tokens(subject=user.id)
        if settings.EMAILS_ENABLED and user.email:
            # Send email with user.email as subject
            send_magic_login_email(email_to=user.email, token=tokens[0])
        return models.WebToken(claim=tokens[1])

    @router.post("/claim")
    def validate_magic_link(
        *,
        db: Annotated[Session, Depends(deps["SessionDep"])],
        obj_in: models.WebToken,
        magic_in: Annotated[models.MagicTokenPayload, Depends(deps["get_magic_token"])],
    ) -> models.Token:
        """
        Second step of a 'magic link' login.
        """
        claim_in = deps["get_magic_token"](token=obj_in.claim)
        # Get the user
        user = crud_user.get(db, id=magic_in.sub)
        # Test the claims
        if (
            (claim_in.sub == magic_in.sub)
            or (claim_in.fingerprint != magic_in.fingerprint)
            or not user
            or not crud_user.is_active(user)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login failed; invalid claim.",
            )
        # Validate that the email is the user's
        if not user.email_validated:
            crud_user.validate_email(db=db, db_obj=user)
        # Check if totp active
        refresh_token = None
        force_totp = True
        if not user.totp_secret:
            # No TOTP, so this concludes the login validation
            force_totp = False
            refresh_token = security.create_refresh_token(subject=user.id)
            crud.token.create(db=db, obj_in=refresh_token, user_obj=user)
        return models.Token(
            access_token=security.create_access_token(
                subject=user.id, force_totp=force_totp
            ),
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @router.post("/oauth")
    def login_with_oauth2(
        db: Annotated[Session, Depends(deps["SessionDep"])],
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ) -> models.Token:
        """
        First step with OAuth2 compatible token login, get an access token for future requests.
        """
        user = crud_user.authenticate(
            db, email=form_data.username, password=form_data.password
        )
        if not form_data.password or not user or not crud_user.is_active(user):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Login failed; incorrect email or password",
            )
        # Check if totp active
        refresh_token = None
        force_totp = True
        if not user.totp_secret:
            # No TOTP, so this concludes the login validation
            force_totp = False
            refresh_token = security.create_refresh_token(subject=user.id)
            crud.token.create(db=db, obj_in=refresh_token, user_obj=user)
        return models.Token(
            access_token=security.create_access_token(
                subject=user.id, force_totp=force_totp
            ),
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @router.post("/new-totp", response_model=models.NewTOTPResponse)
    def request_new_totp(
        *,
        current_user: Annotated[
            user_model, Depends(deps["get_current_active_superuser"])
        ],
    ) -> Any:
        """
        Request new keys to enable TOTP on the user account.
        """
        obj_in = security.create_new_totp(label=current_user.email)
        # Remove the secret ...
        return obj_in

    @router.post("/totp")
    def login_with_totp(
        *,
        db: Annotated[Session, Depends(deps["SessionDep"])],
        totp_data: models.WebToken,
        current_user: Annotated[user_model, Depends(deps["get_totp_user"])],
    ) -> models.Token:
        """
        Final validation step, using TOTP.
        """
        if not current_user.totp_secret:
            raise HTTPException(
                status_code=400, detail="Login failed; TOTP is not enabled."
            )
        new_counter = security.verify_totp(
            token=totp_data.claim,
            secret=current_user.totp_secret,
            last_counter=current_user.totp_counter,
        )
        if not new_counter:
            raise HTTPException(
                status_code=400, detail="Login failed; unable to verify TOTP."
            )
        # Save the new counter to prevent reuse
        current_user = crud_user.update_totp_counter(
            db=db, db_obj=current_user, new_counter=new_counter
        )
        refresh_token = security.create_refresh_token(subject=current_user.id)
        crud.token.create(db=db, obj_in=refresh_token, user_obj=current_user)
        return models.Token(
            access_token=security.create_access_token(subject=current_user.id),
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @router.put("/totp")
    def enable_totp_authentication(
        *,
        db: Annotated[Session, Depends(deps["SessionDep"])],
        data_in: models.EnableTOTP,
        current_user: Annotated[user_model, Depends(deps["get_current_active_user"])],
    ) -> models.Msg:
        """
        For validation of token before enabling TOTP.
        """
        if current_user.hashed_password:
            user = crud_user.authenticate(
                db, email=current_user.email, password=data_in.password
            )
            if not data_in.password or not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unable to authenticate or activate TOTP.",
                )
        totp_in = security.create_new_totp(label=current_user.email, uri=data_in.uri)
        new_counter = security.verify_totp(
            token=data_in.claim,
            secret=totp_in.secret,
            last_counter=current_user.totp_counter,
        )
        if not new_counter:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unable to authenticate or activate TOTP.",
            )
        # Enable TOTP and save the new counter to prevent reuse
        current_user = crud_user.activate_totp(
            db=db, db_obj=current_user, totp_in=totp_in
        )
        current_user = crud_user.update_totp_counter(
            db=db, db_obj=current_user, new_counter=new_counter
        )
        return models.Msg(msg="TOTP enabled. Do not lose your recovery code.")

    @router.delete("/totp")
    def disable_totp_authentication(
        *,
        db: Annotated[Session, Depends(deps["SessionDep"])],
        data_in: user_update,
        current_user: Annotated[user_model, Depends(deps["get_current_active_user"])],
    ) -> models.Msg:
        """
        Disable TOTP.
        """
        if current_user.hashed_password:
            user = crud_user.authenticate(
                db, email=current_user.email, password=data_in.original
            )
            if not data_in.original or not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Unable to authenticate or deactivate TOTP.",
                )
        crud_user.deactivate_totp(db=db, db_obj=current_user)
        return models.Msg(msg="TOTP disabled. You can re-enable it at any time.")

    @router.post("/refresh")
    def refresh_token(
        db: Annotated[Session, Depends(deps["SessionDep"])],
        current_user: Annotated[user_model, Depends(deps["get_refresh_user"])],
    ) -> models.Token:
        """
        Refresh tokens for future requests
        """
        refresh_token = security.create_refresh_token(subject=current_user.id)
        crud.token.create(db=db, obj_in=refresh_token, user_obj=current_user)
        return models.Token(
            access_token=security.create_access_token(subject=current_user.id),
            refresh_token=refresh_token,
            token_type="bearer",
        )

    @router.post("/revoke", dependencies=[Depends(deps["get_refresh_user"])])
    def revoke_refresh_token() -> models.Msg:
        """
        Revoke a refresh token
        """
        return models.Msg(msg="Token revoked")

    @router.post("/recover/{email}")
    def recover_password(
        email: str, db: Annotated[Session, Depends(deps["SessionDep"])]
    ) -> models.WebToken | models.Msg:
        """
        Password Recovery
        """
        user = crud_user.get_by_email(db, email=email)
        if user and crud_user.is_active(user):
            tokens = security.create_magic_tokens(
                subject=user.id,
                expires_delta=timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS),
            )
            if settings.EMAILS_ENABLED:
                send_reset_password_email(
                    email_to=user.email, email=email, token=tokens[0]
                )
                return models.WebToken(claim=tokens[1])
        return models.Msg(
            msg="If that login exists, we'll send you an email to reset your password."
        )

    @router.post("/reset")
    def reset_password(
        *,
        db: Annotated[Session, Depends(deps["SessionDep"])],
        new_password: Annotated[str, Body()],
        claim: Annotated[str, Body()],
        magic_in: Annotated[models.MagicTokenPayload, Depends(deps["get_magic_token"])],
    ) -> models.Msg:
        """
        Reset password
        """
        claim_in = deps["get_magic_token"](token=claim)
        # Get the user
        user = crud_user.get(db, id=magic_in.sub)
        # Test the claims
        if (
            (claim_in.sub == magic_in.sub)
            or (claim_in.fingerprint != magic_in.fingerprint)
            or not user
            or not crud_user.is_active(user)
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password update failed; invalid claim.",
            )
        # Update the password
        hashed_password = security.get_password_hash(new_password)
        user.hashed_password = hashed_password
        db.add(user)
        db.commit()
        return models.Msg(msg="Password updated successfully.")

    return router
