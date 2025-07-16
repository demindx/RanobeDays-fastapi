"""Общие фикстуры для всех тестов."""

import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# Устанавливаем тестовые переменные окружения перед импортом
os.environ.setdefault("POSTGRES_DB_HOST_PORT", "5433")
os.environ.setdefault("POSTGRES_USER", "test_user")
os.environ.setdefault("POSTGRES_PASSWORD", "test_password")
os.environ.setdefault("POSTGRES_DB", "test_db")
os.environ.setdefault("POSTGRES_PORT", "5432")
os.environ.setdefault(
    "SECRET_KEY", "test_secret_key_for_jwt_tokens_very_long_and_secure_key_123456789"
)

from src.config import Config
from src.core.database import get_db_session
from src.core.models import Base
from src.main import app


@pytest.fixture(scope="session")
def test_config() -> Config:
    """Конфигурация для тестов."""
    return Config(
        POSTGRES_DB_HOST_PORT=5433,
        POSTGRES_USER="test_user",
        POSTGRES_PASSWORD="test_password",
        POSTGRES_DB="test_db",
        POSTGRES_PORT=5432,
        POSTGRES_URL="postgresql+asyncpg://test_user:test_password@localhost:5432/test_db",
    )


# Test database setup
@pytest.fixture(scope="session")
def test_engine():
    """Создаем тестовый движок БД в памяти."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine


@pytest.fixture(scope="session")
def test_async_engine():
    """Создаем асинхронный тестовый движок БД."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    return engine


@pytest_asyncio.fixture(scope="function")
async def test_session(test_async_engine) -> AsyncGenerator[AsyncSession]:
    """Создаем тестовую сессию БД для каждого теста."""
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        test_async_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture
def test_client() -> TestClient:
    """Синхронный тест-клиент FastAPI."""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_test_client() -> AsyncGenerator[AsyncClient]:
    """Асинхронный тест-клиент FastAPI."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture
def override_get_db_session(test_session):
    """Переопределяем зависимость БД для тестов."""

    async def _override_get_db_session():
        yield test_session

    app.dependency_overrides[get_db_session] = _override_get_db_session
    yield
    app.dependency_overrides.clear()
