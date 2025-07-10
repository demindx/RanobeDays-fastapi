from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import config
from src.models import Base

engine = create_async_engine(config.POSTGRES_URL)

sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncSession:
    async with sessionmaker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.execute(text("create extension if not exists vector;"))
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
