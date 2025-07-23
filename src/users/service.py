from src.users.exceptions import UserAlreadyExists, UserNotFound, UserProfileNotFound
from src.users.models import User, UserProfile
from src.users.repository import UserRepository
from src.users.schemas import (
    UserProfileUpdateRequest,
    UserRegisterRequest,
)
from src.users.utils import get_password_hash


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository: UserRepository = repository

    async def create_user(self, data: UserRegisterRequest) -> User:
        user_exists = await self.repository.get_user_by_login(data.login)

        if user_exists:
            raise UserAlreadyExists()

        user = User(
            login=data.login,
            email=data.email,
            password_hash=get_password_hash(data.get_password()),
        )

        await self.repository.create_user(user)

        profile = UserProfile(user_id=user.id)

        await self.repository.create_user_profile(profile)

        return user

    async def get_user(self, id: int) -> User:
        user = await self.repository.get_user(id)

        if not user:
            raise UserNotFound()

        return user

    async def get_all_users(self) -> list[User]:
        users = await self.repository.get_all_users()

        if not users:
            return []

        return list(users)

    async def get_user_profile(self, user_id: int) -> UserProfile:
        profile = await self.repository.get_user_profile(user_id)

        if not profile:
            raise UserProfileNotFound

        return profile

    async def update_user_profile(
        self, user_id: int, data: UserProfileUpdateRequest
    ) -> UserProfile:
        profile = await self.repository.get_user_profile(user_id)
        if not profile:
            raise UserProfileNotFound

        for attr, value in data.model_dump(
            exclude_unset=True, exclude_none=True
        ).items():
            if hasattr(profile, attr):
                setattr(profile, attr, value)

        profile = await self.repository.update_user_profile(profile)

        return profile

    async def _update_user_status(self, id: int, is_active: bool) -> User:
        user = await self.repository.get_user(id)
        if not user:
            raise UserNotFound()

        user.is_active = is_active

        user = await self.repository.update_user(user)

        return user

    async def activate_user(self, id: int) -> User:
        return await self._update_user_status(id, True)

    async def deactivate_user(self, id: int) -> User:
        return await self._update_user_status(id, False)

    async def delete_user(self, id: int) -> None:
        await self.repository.delete_user(id)
