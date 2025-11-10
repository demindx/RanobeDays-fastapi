from typing import Annotated

from fastapi import Depends

from src.core.dependencies import DbSession
from src.users.models import User, UserProfile
from src.users.repository import UserProfileRepository, UserRepository
from src.users.service import UserProfileService, UserService


def get_user_repo(session: DbSession) -> UserRepository:
    return UserRepository(session, User)


def get_user_profile_repo(session: DbSession) -> UserProfileRepository:
    return UserProfileRepository(session, UserProfile)


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)


def get_user_profile_service(
    repo: Annotated[UserProfileRepository, Depends(get_user_profile_repo)],
) -> UserProfileService:
    return UserProfileService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
UserProfileServiceDep = Annotated[UserProfileService, Depends(get_user_profile_service)]
