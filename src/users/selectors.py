from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import User


async def get_users(session: AsyncSession) -> list[User]:
    result = await session.scalars(select(User))
    return result.all()
