import pytest
from sqlalchemy import event

from src.core.exceptions import AlreadyExists
from src.core.schemas import Pagination
from src.teams.models import TeamUserRole
from src.teams.repository import TeamRepository
from src.teams.schemas import TeamAddUser
from src.users.models import User
from src.users.repository import UserRepository


async def test_get_all_uses_stable_order_and_returns_disjoint_pages(db_session, seed):
    users = []
    for index in range(4):
        user, _ = await seed.user(
            login=f"user{index}", email=f"user{index}@example.com"
        )
        users.append(user)

    repository = UserRepository(db_session)
    first_page = await repository.get_all(Pagination(limit=2, offset=0))
    second_page = await repository.get_all(Pagination(limit=2, offset=2))

    first_ids = [user.id for user in first_page]
    second_ids = [user.id for user in second_page]

    assert first_ids == sorted(first_ids)
    assert second_ids == sorted(second_ids)
    assert set(first_ids).isdisjoint(second_ids)
    assert first_ids + second_ids == [user.id for user in users]


async def test_get_all_applies_limit_offset_and_order_in_sql(db_session, seed):
    for index in range(3):
        await seed.user(login=f"user{index}", email=f"user{index}@example.com")

    statements = []

    def record_statement(
        connection, cursor, statement, parameters, context, executemany
    ):
        if "FROM users" in statement:
            statements.append(statement.lower())

    engine = db_session.get_bind()
    event.listen(engine, "before_cursor_execute", record_statement)
    try:
        await UserRepository(db_session).get_all(Pagination(limit=1, offset=1))
    finally:
        event.remove(engine, "before_cursor_execute", record_statement)

    paginated_statement = next(
        statement for statement in statements if "order by users.id" in statement
    )
    assert "limit" in paginated_statement
    assert "offset" in paginated_statement


async def test_create_translates_unique_violation_to_conflict(db_session, seed):
    await seed.user(login="duplicate", email="duplicate@example.com")
    duplicate = User(
        login="duplicate",
        email="another@example.com",
        password_hash="password-hash",
    )

    with pytest.raises(AlreadyExists) as error:
        await UserRepository(db_session).create(duplicate)

    assert error.value.status_code == 409
    await db_session.rollback()


async def test_add_duplicate_team_member_raises_conflict(db_session, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    await seed.membership(team.id, user.id)
    repository = TeamRepository(db_session)

    with pytest.raises(AlreadyExists) as error:
        await repository.add_user(
            team.id, TeamAddUser(user_id=user.id, role=TeamUserRole.MANAGER)
        )

    assert error.value.status_code == 409
    await db_session.rollback()


async def test_delete_missing_record_is_idempotent(db_session):
    repository = UserRepository(db_session)

    await repository.delete(-1)
    await repository.delete(-1)


async def test_team_repository_delete_missing_record_is_idempotent(db_session):
    repository = TeamRepository(db_session)

    await repository.delete(-1)
    await repository.delete(-1)
