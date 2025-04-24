from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine

from fastapi_myauth import models

from .auth import FastAuth

app = FastAPI()


class UserR(models.UserRead):
    language: str | None = None


class UserM(models.user.User):
    language: str = "en"


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def get_db():
    with Session(engine) as session:
        yield session


def db_dep() -> Session:
    return next(get_db())


fast_auth = FastAuth(SessionDep=db_dep, user_read=UserR, user_model=UserM)


app.include_router(fast_auth.get_router())

SQLModel.metadata.create_all(engine)
