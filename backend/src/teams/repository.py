from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExists
from src.core.repository import PostgresRepository
from src.core.schemas import Pagination
from src.novel.models import Novel
from src.teams.models import Team, TeamUsers
from src.teams.schemas import TeamAddUser, TeamUpdate


class TeamRepository(PostgresRepository[Team, TeamUpdate]):
    model: type[Team] = Team

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_creator_id(self, id: int, pagination: Pagination) -> list[Team]:
        stmt = (
            select(Team)
            .where(Team.creator_id == id)
            .order_by(Team.id)
            .offset(pagination.offset)
            .limit(pagination.limit)
        )

        result = await self.session.scalars(stmt)

        return list(result.all())

    async def get_user_teams(self, id: int, pagination: Pagination) -> list[Team]:
        stmt = (
            select(Team)
            .join(TeamUsers, Team.id == TeamUsers.team_id)
            .order_by(Team.id)
            .where(TeamUsers.user_id == id)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        result = await self.session.scalars(stmt)

        return list(result.all())

    async def get_team_users(self, id: int, pagination: Pagination) -> list[TeamUsers]:
        stmt = (
            select(TeamUsers)
            .where(TeamUsers.team_id == id)
            .order_by(TeamUsers.user_id)
            .limit(pagination.limit)
            .offset(pagination.offset)
        )

        return list((await self.session.scalars(stmt)).all())

    async def add_user(self, id: int, data: TeamAddUser) -> None:
        connection = TeamUsers(team_id=id, user_id=data.user_id, role=data.role)
        try:
            self.session.add(connection)
            await self.session.flush()
        except IntegrityError as e:
            err = str(e)

            if "unique" in err:
                raise AlreadyExists(TeamUsers)

            raise

    async def remove_user(self, id: int, user_id: int) -> None:
        stmt = (
            delete(TeamUsers)
            .where(TeamUsers.team_id == id)
            .where(TeamUsers.user_id == user_id)
        )

        _ = await self.session.execute(stmt)
        await self.session.flush()

    async def get_novels(self, id: int, pagination: Pagination) -> list[Novel]:
        stmt = (
            select(Novel)
            .where(Novel.team_id == id)
            .order_by(Novel.id)
            .offset(pagination.offset)
            .limit(pagination.limit)
        )
        novels = await self.session.scalars(stmt)

        return list(novels.all())
