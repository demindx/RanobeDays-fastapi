from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserModel, UserProfileModel


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: UserModel) -> UserModel:
        self.session.add(user)

        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def create_user_profile(self, profile: UserProfileModel) -> UserProfileModel:
        self.session.add(profile)

        await self.session.flush()
        await self.session.refresh(profile)

        return profile

    async def get_all_users(self) -> Sequence[UserModel] | None:
        stmt = select(UserModel)

        result = await self.session.scalars(stmt)

        return result.all()

    async def get_user(self, id: int) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.id == id)

        result = await self.session.scalar(stmt)

        return result

    async def get_user_by_login(self, login: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.login == login)

        result = await self.session.scalar(stmt)

        return result

    async def get_user_profile(self, user_id: int) -> UserProfileModel | None:
        stmt = select(UserProfileModel).where(UserProfileModel.user_id == user_id)

        result = await self.session.scalar(stmt)

        return result

    async def update_user(self, user: UserModel) -> UserModel:
        self.session.add(user)

        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def update_user_profile(self, profile: UserProfileModel) -> UserProfileModel:
        self.session.add(profile)

        await self.session.flush()
        await self.session.refresh(profile)

        return profile

    async def delete_user(self, id: int) -> None:
        stmt = delete(UserModel).where(UserModel.id == id)

        await self.session.execute(stmt)
