from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session

DbSession = Annotated[AsyncSession, get_db_session]
