from src.core.service import AbstractService
from src.teams.models import Team, TeamUserRole, TeamUsers
from src.teams.repository import TeamRepository
from src.teams.schemas import TeamCreate, TeamUpdate


class TeamService(AbstractService[Team, TeamCreate, TeamUpdate, TeamRepository]):
    def __init__(self, repository: TeamRepository) -> None:
        super().__init__(repository)

    async def get_by_creator_id(self, id: int) -> list[Team]:
        return await self.repo.get_by_creator_id(id)

    async def get_user_teams(self, id: int) -> list[Team]:
        return await self.repo.get_user_teams(id)

    async def add_user(self, user_id: int, team_id: int, role: TeamUserRole):
        team_user_conn = TeamUsers(user_id=user_id, team_id=team_id, role=role)

        await self.repo.add_user(team_user_conn)
