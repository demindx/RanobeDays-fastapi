import asyncio
import os
from collections.abc import AsyncIterator
from uuid import uuid4

import pytest_asyncio
from sqlalchemy import inspect, text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

MAINTENANCE_DATABASE_URL = os.environ.get(
    "TEST_MAINTENANCE_DATABASE_URL",
    "postgresql+asyncpg://admin:qwdqwd@localhost:5432/postgres",
)

EXPECTED_TABLES = {
    "alembic_version",
    "categories",
    "chapters",
    "countries",
    "languages",
    "novel_categories",
    "novels",
    "refresh_sessions",
    "team_users",
    "teams",
    "user_profiles",
    "users",
}


def _alembic_config(database_url: str) -> Config:
    config = Config("alembic.ini", toml_file="pyproject.toml")
    config.attributes["database_url"] = database_url
    return config


async def _schema_state(database_url: str) -> tuple[set[str], str | None]:
    engine = create_async_engine(database_url)
    try:
        async with engine.connect() as connection:
            tables = await connection.run_sync(
                lambda sync_connection: set(inspect(sync_connection).get_table_names())
            )
            revision = None
            if "alembic_version" in tables:
                revision = await connection.scalar(
                    text("SELECT version_num FROM alembic_version")
                )
            return tables, revision
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def migration_database_url() -> AsyncIterator[str]:
    database_name = f"ranobedays_migration_{uuid4().hex}"
    maintenance_url = make_url(MAINTENANCE_DATABASE_URL)
    database_url = maintenance_url.set(database=database_name).render_as_string(
        hide_password=False
    )
    maintenance_engine = create_async_engine(
        maintenance_url, isolation_level="AUTOCOMMIT"
    )

    try:
        async with maintenance_engine.connect() as connection:
            await connection.execute(text(f'CREATE DATABASE "{database_name}"'))
        yield database_url
    finally:
        async with maintenance_engine.connect() as connection:
            await connection.execute(
                text(f'DROP DATABASE IF EXISTS "{database_name}" WITH (FORCE)')
            )
        await maintenance_engine.dispose()


async def test_upgrade_head_creates_schema_and_is_idempotent(
    migration_database_url: str,
) -> None:
    config = _alembic_config(migration_database_url)
    expected_head = ScriptDirectory.from_config(config).get_current_head()

    await asyncio.to_thread(command.upgrade, config, "head")
    first_state = await _schema_state(migration_database_url)

    assert first_state == (EXPECTED_TABLES, expected_head)

    await asyncio.to_thread(command.upgrade, config, "head")
    second_state = await _schema_state(migration_database_url)

    assert second_state == first_state


async def test_schema_can_be_recreated_after_downgrade_to_base(
    migration_database_url: str,
) -> None:
    config = _alembic_config(migration_database_url)
    expected_head = ScriptDirectory.from_config(config).get_current_head()

    await asyncio.to_thread(command.upgrade, config, "head")
    await asyncio.to_thread(command.downgrade, config, "base")

    tables_after_downgrade, revision_after_downgrade = await _schema_state(
        migration_database_url
    )
    assert tables_after_downgrade == {"alembic_version"}
    assert revision_after_downgrade is None

    await asyncio.to_thread(command.upgrade, config, "head")

    assert await _schema_state(migration_database_url) == (
        EXPECTED_TABLES,
        expected_head,
    )
