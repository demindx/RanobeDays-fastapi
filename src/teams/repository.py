from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository import BaseRepository
from src.teams.models import Team, TeamUsers
from src.teams.schemas import TeamUpdate


class TeamRepository(BaseRepository[Team, TeamUpdate]):
    def __init__(self, session: AsyncSession, model: type[Team]):
        super().__init__(session, model)

    async def get_by_creator_id(self, id: int) -> list[Team]:
        stmt = select(Team).where(Team.creator_id == id)

        result = await self.session.scalars(stmt)

        return list(result.all())

    async def get_user_teams(self, id: int) -> list[Team]:
        stmt = select(Team).join(TeamUsers, Team.id == TeamUsers.team_id).where(TeamUsers.user_id == id)

        result = await self.session.scalars(stmt)

        return list(result.all())
