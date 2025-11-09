from typing import override
from src.users.repository import UserProfileRepository, UserRepository
from src.users.schemas import (
    UserProfileUpdate, 
    UserRegister, 
    UserPasswordUpdate, 
    UserProfileCreate
)
from src.users.models import User, UserProfile
from src.core.service import AbstractService


class UserService(AbstractService[
                  User, 
                  UserRegister,
                  UserPasswordUpdate, UserRepository]):

    async def get_by_login(self, login: str) -> User:
        return await self.repo.get_by_login(login)

    async def get_by_email(self, email: str) -> User:
        return await self.repo.get_by_email(email)


class UserProfileService(AbstractService[
                         UserProfile,
                         UserProfileCreate,
                         UserProfileUpdate,
                         UserProfileRepository
                         ]):
    async def get_by_user_id(self, user_id: int) -> UserProfile:
        return await self.repo.get_by_user_id(user_id)
