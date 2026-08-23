from typing import override

from src.config import config
from src.core.exceptions import InvalidReference, NotFound
from src.core.service import AbstractService
from src.novel.models import Novel
from src.teams.models import Team, TeamUserRole, TeamUsers
from src.teams.repository import TeamRepository
from src.teams.schemas import TeamAddUser, TeamCreate, TeamUpdate
from src.users.models import User
from src.users.repository import UserRepository


class TeamService(AbstractService[Team, TeamCreate, TeamUpdate, TeamRepository]):
    def __init__(self, team_repo: TeamRepository, user_repo: UserRepository) -> None:
        super().__init__(team_repo)

        self._user_repo: UserRepository = user_repo

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
        try:
            _ = await self._user_repo.get_by_id(data.creator_id)
        except NotFound:
            raise InvalidReference(User, "creator_id", data.creator_id)

        team = await super().create(data)

        team_add_user = TeamAddUser(role=TeamUserRole.CREATOR, user_id=data.creator_id)

        await self.repo.add_user(team.id, team_add_user)

        return team
