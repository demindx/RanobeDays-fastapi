import uuid

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions import RefreshSessionCreationError, RefreshSessionNotFound
from src.auth.models import RefreshSession
from src.auth.schemas import RefreshSessionCreate


class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_refresh_session(self, refresh_token: uuid.UUID) -> RefreshSession:
        stmt = select(RefreshSession).where(
            RefreshSession.refresh_token == refresh_token
        )

        session = (await self.session.execute(stmt)).scalar_one()

        if not session:
            raise RefreshSessionNotFound

        return session

    async def delete(self, refresh_session: RefreshSession):
        await self.session.delete(refresh_session)

    async def create_refresh_session(
        self, data: RefreshSessionCreate
    ) -> RefreshSession:
        stmt = (
            insert(RefreshSession).values(**data.model_dump()).returning(RefreshSession)
        )

        result = await self.session.execute(stmt)

        result = result.scalar()

        if not result:
            raise RefreshSessionCreationError

        return result
