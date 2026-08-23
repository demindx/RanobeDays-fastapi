from typing import Annotated

from fastapi import Depends

from src.core.dependencies import DbSession
from src.teams.models import Team
from src.teams.repository import TeamRepository
from src.teams.service import TeamService
from src.users.dependencies import get_user_repo
from src.users.repository import UserRepository


def get_team_repo(session: DbSession) -> TeamRepository:
    return TeamRepository(session, Team)


def get_team_service(
    team_repo: Annotated[TeamRepository, Depends(get_team_repo)],
    user_repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> TeamService:
    return TeamService(team_repo, user_repo)


TeamServiceDep = Annotated[TeamService, Depends(get_team_service)]
