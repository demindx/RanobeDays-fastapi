from typing import Annotated

from fastapi import Depends

from src.core.dependencies import DbSession
from src.teams.models import Team
from src.teams.repository import TeamRepository
from src.teams.service import TeamService


def get_team_repo(session: DbSession) -> TeamRepository:
    return TeamRepository(session, Team)


def get_team_service(repo: Annotated[TeamRepository, Depends(get_team_repo)]) -> TeamService:
    return TeamService(repo)


TeamServiceDep = Annotated[TeamService, Depends(get_team_service)]
