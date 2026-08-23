import os
from collections.abc import AsyncGenerator, AsyncIterator
from datetime import UTC, datetime

import httpx
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.category.model import Category, CategoryTypeEnum
from src.chapter.models import Chapter
from src.core.database import get_db_session
from src.core.models import Base
from src.country.models import Country
from src.language.models import Language
from src.main import app
from src.novel.models import Novel, NovelType
from src.teams.models import Team, TeamType, TeamUserRole, TeamUsers
from src.users.models import User, UserProfile
from src.users.utils import get_password_hash

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://admin:qwdqwd@localhost:5432/ranobedays_test",
)
MAINTENANCE_DATABASE_URL = os.environ.get(
    "TEST_MAINTENANCE_DATABASE_URL",
    "postgresql+asyncpg://admin:qwdqwd@localhost:5432/postgres",
)


def _db_name(url: str) -> str:
    return url.rsplit("/", 1)[-1]


@pytest_asyncio.fixture(scope="session")
async def _prepare_database():
    db_name = _db_name(TEST_DATABASE_URL)
    maint_engine = create_async_engine(
        MAINTENANCE_DATABASE_URL, isolation_level="AUTOCOMMIT"
    )
    async with maint_engine.connect() as conn:
        exists = await conn.scalar(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": db_name},
        )
        if not exists:
            await conn.execute(text(f'CREATE DATABASE "{db_name}"'))
    await maint_engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def engine(_prepare_database):
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def session_factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def client(session_factory) -> AsyncIterator[httpx.AsyncClient]:
    async def override_get_db_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    app.dependency_overrides[get_db_session] = override_get_db_session

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

    app.dependency_overrides.pop(get_db_session, None)


@pytest_asyncio.fixture
async def db_session(session_factory) -> AsyncIterator[AsyncSession]:
    async with session_factory() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def _cleanup(session_factory):
    yield
    async with session_factory() as session:
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(
                text(f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE')
            )
        await session.commit()


class Seed:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def user(
        self,
        login: str = "user1",
        email: str = "user1@example.com",
        password: str = "password123",
        nickname: str = "User One",
    ) -> tuple[User, UserProfile]:
        user = User(
            login=login, email=email, password_hash=get_password_hash(password)
        )
        self.session.add(user)
        await self.session.flush()
        profile = UserProfile(user_id=user.id, nickname=nickname)
        self.session.add(profile)
        await self.session.commit()
        return user, profile

    async def team(
        self, creator_id: int, name: str = "Team", type_: TeamType = TeamType.TRANSLATORS
    ) -> Team:
        team = Team(name=name, type=type_, creator_id=creator_id)
        self.session.add(team)
        await self.session.commit()
        return team

    async def language(self, name: str = "Chinese") -> Language:
        language = Language(name=name)
        self.session.add(language)
        await self.session.commit()
        return language

    async def country(self, name: str = "Russian") -> Country:
        country = Country(name=name)
        self.session.add(country)
        await self.session.commit()
        return country

    async def category(
        self, name: str = "Fantasy", type_: CategoryTypeEnum = CategoryTypeEnum.GENRE
    ) -> Category:
        category = Category(name=name, type=type_)
        self.session.add(category)
        await self.session.commit()
        return category

    async def novel(
        self,
        team_id: int,
        language_id: int,
        country_id: int,
        title: str = "Test Novel",
        age_limit: int = 16,
    ) -> Novel:
        novel = Novel(
            title=title,
            age_limit=age_limit,
            team_id=team_id,
            language_id=language_id,
            country_id=country_id,
            description="Description",
            publish_date=datetime.now(UTC),
            type=NovelType.ORIGINAL,
        )
        self.session.add(novel)
        await self.session.commit()
        return novel

    async def chapter(
        self,
        novel_id: int,
        team_id: int,
        title: str = "Chapter 1",
        number: int = 1,
        content: str = "Hello",
    ) -> Chapter:
        chapter = Chapter(
            title=title,
            number=number,
            content=content,
            novel_id=novel_id,
            team_id=team_id,
        )
        self.session.add(chapter)
        await self.session.commit()
        return chapter

    async def membership(
        self, team_id: int, user_id: int, role: TeamUserRole = TeamUserRole.MANAGER
    ) -> TeamUsers:
        membership = TeamUsers(team_id=team_id, user_id=user_id, role=role)
        self.session.add(membership)
        await self.session.commit()
        return membership


@pytest_asyncio.fixture
async def seed(db_session) -> AsyncIterator[Seed]:
    yield Seed(db_session)
