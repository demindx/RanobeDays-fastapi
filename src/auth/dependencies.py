from typing import Annotated

from fastapi import Depends

from src.auth.exceptions import ForbiddenError, InvalidTokenError
from src.auth.repository import AuthRepository
from src.auth.security import JwtHeaderBearer
from src.auth.service import AuthService
from src.auth.utils import decode_jwt_token
from src.core.dependencies import DbSession
from src.core.exceptions import NotFound
from src.users.dependencies import get_user_service
from src.users.models import User, UserRoleEnum
from src.users.service import UserService

header_bearer = JwtHeaderBearer()


def get_auth_repo(session: DbSession):
    return AuthRepository(session)


def get_auth_service(
    repo: Annotated[AuthRepository, Depends(get_auth_repo)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> AuthService:
    return AuthService(repo, service)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


async def get_current_user(
    service: Annotated[UserService, Depends(get_user_service)],
    token: Annotated[str, Depends(header_bearer)],
) -> User:
    token_data = decode_jwt_token(token)

    try:
        user = await service.get_user(token_data.sub)
    except NotFound:
        raise InvalidTokenError("Invalid token")

    return user


async def get_admin_user(user: Annotated[User, Depends(get_current_user)]):
    if user.role != UserRoleEnum.ADMIN:
        raise ForbiddenError
    return user
