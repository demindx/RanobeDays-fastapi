from typing import Annotated

from fastapi import Depends

from src.auth.repository import AuthRepository
from src.auth.service import AuthService
from src.core.dependencies import DbSession
from src.users.dependencies import get_user_service
from src.users.service import UserService


def get_auth_repo(session: DbSession):
    return AuthRepository(session)


def get_auth_service(
    repo: Annotated[AuthRepository, Depends(get_auth_repo)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> AuthService:
    return AuthService(repo, service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
