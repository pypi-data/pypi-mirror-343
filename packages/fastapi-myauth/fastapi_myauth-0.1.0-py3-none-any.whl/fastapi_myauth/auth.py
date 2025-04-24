from collections.abc import Callable
from dataclasses import dataclass

from fastapi import APIRouter
from sqlmodel import Relationship, Session

from . import crud, models


@dataclass
class FastAuth:
    """
    FastAPI Authentication class.
    """

    SessionDep: Callable[[], Session]
    user_model: type[models.User] = models.User
    user_read: type[models.UserRead] = models.UserRead
    user_create: type[models.UserCreate] = models.UserCreate
    user_update: type[models.UserUpdate] = models.UserUpdate
    _internal_user_model: type[models.User] | None = None

    def create_internal_user_model(self):
        if self._internal_user_model is None:

            class User(self.user_model, table=True):
                refresh_tokens: list[models.RefreshToken] = Relationship(
                    back_populates="authenticates", cascade_delete=True
                )

            self._internal_user_model = User
        return self._internal_user_model

    def crud_user(self, model):
        return crud.crud_user.CRUDUser(model)

    def deps(self):
        """
        Dependency injection for FastAPI Authentication.
        """
        from fastapi_myauth.api.deps import get_deps

        return get_deps(
            crud_user=self.crud_user(self.create_internal_user_model()),
            SessionDep=self.SessionDep,
        )

    def get_router(self) -> APIRouter:
        """
        Get the router for FastAPI Authentication.
        """
        from fastapi_myauth.api.v1 import get_login_router, get_user_router

        api_router = APIRouter()

        api_router.include_router(
            get_user_router(
                user_model=self.create_internal_user_model(),
                user_read=self.user_read,
                user_create=self.user_create,
                user_update=self.user_update,
                crud_user=self.crud_user(self.create_internal_user_model()),
                deps=self.deps(),
            ),
            prefix="/users",
            tags=["users"],
        )
        api_router.include_router(
            get_login_router(
                user_model=self.create_internal_user_model(),
                user_read=self.user_read,
                user_create=self.user_create,
                user_update=self.user_update,
                crud_user=self.crud_user(self.create_internal_user_model()),
                deps=self.deps(),
            ),
            prefix="/login",
            tags=["login"],
        )

        return api_router
