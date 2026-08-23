from typing import override

from src.core.exceptions import InvalidReference, NotFound
from src.core.service import AbstractService
from src.novel.models import Novel
from src.novel.repository import NovelRepository
from src.novel.schemas import NovelCreate, NovelUpdate
from src.teams.models import Team
from src.teams.repository import TeamRepository


class NovelService(AbstractService[Novel, NovelCreate, NovelUpdate, NovelRepository]):
    def __init__(self, novel_repo: NovelRepository, team_repo: TeamRepository) -> None:
        super().__init__(novel_repo)

        self._team_repo: TeamRepository = team_repo

    @override
    async def create(self, data: NovelCreate) -> Novel:
        try:
            _ = await self._team_repo.get_by_id(data.team_id)
        except NotFound:
            raise InvalidReference(Team, "team_id", data.team_id)

        return await super().create(data)
