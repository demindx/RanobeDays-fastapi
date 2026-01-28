import uuid
from typing import override

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.core.exceptions import AlreadyExists, NotFound
from src.core.repository import PostgresRepository
from src.users.models import User, UserProfile
from src.users.schemas import UserPasswordUpdate, UserProfileUpdate
from src.users.utils import get_password_hash


class UserRepository(PostgresRepository[User, UserPasswordUpdate]):
    @override
    async def update(self, id: int | uuid.UUID, data: UserPasswordUpdate) -> User:
        instance: User = await self.get_by_id(id)

        instance.password_hash = get_password_hash(data.password1)

        try:
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
        except IntegrityError as e:
            err = str(e)

            if "unique" in err:
                raise AlreadyExists(self.model)

            raise

        return instance

    async def get_by_login(self, login: str) -> User:
        stmt = select(self.model).where(self.model.login == login)

        try:
            result = (await self.session.execute(stmt)).scalar_one()
        except NoResultFound:
            raise NotFound(self.model, self.get_by_login.__name__, id)

        return result

    async def get_by_email(self, email: str) -> User:
        stmt = select(self.model).where(self.model.email == email)

        try:
            result = (await self.session.execute(stmt)).scalar_one()
        except NoResultFound:
            raise NotFound(self.model, self.get_by_email.__name__, id)

        return result


class UserProfileRepository(PostgresRepository[UserProfile, UserProfileUpdate]):
    async def get_by_user_id(self, user_id: int) -> UserProfile:
        stmt = select(self.model).where(self.model.user_id == user_id)

        try:
            result = (await self.session.execute(stmt)).scalar_one()
        except NoResultFound:
            raise NotFound(self.model, self.get_by_user_id.__name__, user_id)

        return result
