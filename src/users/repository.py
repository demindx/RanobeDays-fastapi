from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User, UserProfile


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User:
        self.session.add(user)

        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def create_user_profile(self, profile: UserProfile) -> UserProfile:
        self.session.add(profile)

        await self.session.flush()
        await self.session.refresh(profile)

        return profile

    async def get_all_users(self) -> Sequence[User]:
        stmt = select(User)

        result = await self.session.scalars(stmt)

        return result.all()

    async def get_user(self, id: int) -> User | None:
        stmt = select(User).where(User.id == id)

        result = await self.session.scalar(stmt)

        return result

    async def get_user_by_login(self, login: str) -> User | None:
        stmt = select(User).where(User.login == login)

        result = await self.session.scalar(stmt)

        return result

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)

        result = await self.session.scalar(stmt)

        return result

    async def get_user_profile(self, user_id: int) -> UserProfile | None:
        stmt = select(UserProfile).where(UserProfile.user_id == user_id)

        result = await self.session.scalar(stmt)

        return result

    async def update_user(self, user: User) -> User:
        self.session.add(user)

        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def update_user_profile(self, profile: UserProfile) -> UserProfile:
        self.session.add(profile)

        await self.session.flush()
        await self.session.refresh(profile)

        return profile

    async def delete_user(self, id: int) -> None:
        stmt = delete(User).where(User.id == id)

        await self.session.execute(stmt)
