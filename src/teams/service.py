from src.teams.models import Team, TeamUserRole, TeamUsers
from src.teams.repository import TeamRepository
from src.teams.schemas import TeamCreate, TeamUpdate


class TeamService:
    def __init__(self, repository: TeamRepository) -> None:
        self.repository = repository

    async def get_by_id(self, id: int) -> Team:
        return await self.repository.get_by_id(id)

    async def get_all(self, limit: int = 50, offset: int = 0) -> list[Team]:
        return await self.repository.get_all(limit, offset)

    async def get_by_creator_id(self, id: int) -> list[Team]:
        return await self.repository.get_by_creator_id(id)

    async def get_user_teams(self, id: int) -> list[Team]:
        return await self.repository.get_user_teams(id)

    async def create(self, data: TeamCreate) -> Team:
        team = Team(
            name=data.name,
            type=data.type,
            creator_id=data.creator_id,
        )

        team = await self.repository.create(team)

        await self.add_user(team.creator_id, team.id, TeamUserRole.CREATOR)

        return team

    async def update(self, id: int, data: TeamUpdate) -> Team:
        return await self.repository.update(id, data)

    async def delete(self, id: int) -> None:
        await self.repository.delete(id)

    async def add_user(self, user_id: int, team_id: int, role: TeamUserRole):
        team_user_conn = TeamUsers(
            user_id = user_id,
            team_id = team_id,
            role = role
        )

        await self.repository.add_user(team_user_conn)
