from typing import override

from src.config import config
from src.core.service import AbstractService
from src.novel.models import Novel
from src.teams.models import Team, TeamUserRole, TeamUsers
from src.teams.repository import TeamRepository
from src.teams.schemas import TeamAddUser, TeamCreate, TeamUpdate


class TeamService(AbstractService[Team, TeamCreate, TeamUpdate, TeamRepository]):
    def __init__(self, repository: TeamRepository) -> None:
        super().__init__(repository)

    async def get_by_creator_id(self, id: int) -> list[Team]:
        return await self.repo.get_by_creator_id(id)

    async def get_user_teams(self, id: int) -> list[Team]:
        return await self.repo.get_user_teams(id)

    async def get_users(self, id: int) -> list[TeamUsers]:
        return await self.repo.get_team_users(id)

    async def add_user(self, id: int, data: TeamAddUser):
        await self.repo.add_user(id, data)

    async def remove_user(self, id: int, user_id: int) -> None:
        await self.repo.remove_user(id, user_id)

    async def get_novels(
        self, id: int, limit: int = config.DEFAULT_PAGINATION_LIMIT, offset: int = 0
    ) -> list[Novel]:
        return await self.repo.get_novels(id, limit=limit, offset=offset)

    @override
    async def create(self, data: TeamCreate) -> Team:
        team = await super().create(data)

        team_add_user = TeamAddUser(role=TeamUserRole.CREATOR, user_id=data.creator_id)

        await self.repo.add_user(team.id, team_add_user)

        return team
