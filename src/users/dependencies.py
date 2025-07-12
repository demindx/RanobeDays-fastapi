from typing import Annotated

from fastapi import Depends

from src.core.dependencies import DbSession
from src.users.repository import UserRepository
from src.users.service import UserService


def get_user_repo(session: DbSession) -> UserRepository:
    return UserRepository(session)


def get_user_service(repo: Annotated[UserRepository, Depends(get_user_repo)]) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
