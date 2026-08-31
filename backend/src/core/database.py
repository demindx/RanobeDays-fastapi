from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import config
from src.core.models import Base

engine = create_async_engine(config.POSTGRES_URL, echo=config.DB_ECHO)

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    async with sessionmaker.begin() as session:
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        _ = await conn.execute(text("create extension if not exists vector;"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
