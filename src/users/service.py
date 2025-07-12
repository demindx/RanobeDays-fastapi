import bcrypt

from src.users.exceptions import UserAlreadyExists, UserNotFound, UserProfileNotFound
from src.users.models import UserModel, UserProfileModel
from src.users.repository import UserRepository
from src.users.schemas import UserCreateRequest, UserProfileResponse, UserProfileUpdateRequest, UserResponse


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository: UserRepository = repository

    def _get_password_hash(self, password: str) -> str:
        return bcrypt.hashpw(salt=bcrypt.gensalt(), password=password.encode("utf-8")).decode("utf-8")

    async def create_user(self, data: UserCreateRequest) -> UserResponse:
        user_exists = await self.repository.get_user_by_login(data.login)

        if user_exists:
            raise UserAlreadyExists()

        user = UserModel(login=data.login, email=data.email, password_hash=self._get_password_hash(data.get_password()))

        await self.repository.create_user(user)

        profile = UserProfileModel(user_id=user.id)

        await self.repository.create_user_profile(profile)

        return UserResponse.model_validate(user)

    async def get_user(self, id: int) -> UserResponse:
        user = await self.repository.get_user(id)

        if not user:
            raise UserNotFound()

        return UserResponse.model_validate(user)

    async def get_all_users(self) -> list[UserResponse]:
        users = await self.repository.get_all_users()

        if not users:
            return []

        return [UserResponse.model_validate(user) for user in users]

    async def get_user_profile(self, user_id: int) -> UserProfileResponse:
        profile = await self.repository.get_user_profile(user_id)

        if not profile:
            raise UserProfileNotFound()

        return UserProfileResponse.model_validate(profile)

    async def update_user_profile(self, user_id: int, data: UserProfileUpdateRequest) -> UserProfileResponse:
        profile = await self.repository.get_user_profile(user_id)
        if not profile:
            raise UserProfileNotFound()

        for attr, value in data.model_dump(exclude_unset=True, exclude_none=True).items():
            if hasattr(profile, attr):
                setattr(profile, attr, value)

        profile = await self.repository.update_user_profile(profile)

        return UserProfileResponse.model_validate(profile)

    async def _update_user_status(self, id: int, is_active: bool) -> UserResponse:
        user = await self.repository.get_user(id)
        if not user:
            raise UserNotFound()

        user.is_active = is_active

        user = await self.repository.update_user(user)

        return UserResponse.model_validate(user)

    async def activate_user(self, id: int) -> UserResponse:
        return await self._update_user_status(id, True)

    async def deactivate_user(self, id: int) -> UserResponse:
        return await self._update_user_status(id, False)

    async def delete_user(self, id: int) -> None:
        await self.repository.delete_user(id)
