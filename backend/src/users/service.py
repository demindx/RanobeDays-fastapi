from typing import override

from src.core.service import AbstractService
from src.users.models import User, UserProfile
from src.users.repository import UserProfileRepository, UserRepository
from src.users.schemas import (
    UserPasswordUpdate,
    UserProfileCreate,
    UserProfileUpdate,
    UserRegister,
)
from src.users.utils import get_password_hash


class UserService(
    AbstractService[User, UserRegister, UserPasswordUpdate, UserRepository]
):
    @override
    async def create(self, data: UserRegister) -> User:
        instance = User.from_data(data)

        instance.password_hash = get_password_hash(data.password1)

        instance = await self.repo.create(instance)

        return instance

    async def get_by_login(self, login: str) -> User:
        return await self.repo.get_by_login(login)

    async def get_by_email(self, email: str) -> User:
        return await self.repo.get_by_email(email)


class UserProfileService(
    AbstractService[
        UserProfile, UserProfileCreate, UserProfileUpdate, UserProfileRepository
    ]
):
    async def get_by_user_id(self, user_id: int) -> UserProfile:
        return await self.repo.get_by_user_id(user_id)
