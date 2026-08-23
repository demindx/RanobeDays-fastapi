from typing import Annotated

from fastapi import Depends

from src.core.dependencies import DbSession
from src.novel.models import Novel
from src.novel.repository import NovelRepository
from src.novel.service import NovelService
from src.teams.dependencies import get_team_repo
from src.teams.repository import TeamRepository


def get_novel_repo(session: DbSession) -> NovelRepository:
    return NovelRepository(session, Novel)


def get_novel_service(
    novel_repo: Annotated[NovelRepository, Depends(get_novel_repo)],
    team_repo: Annotated[TeamRepository, Depends(get_team_repo)],
) -> NovelService:
    return NovelService(novel_repo, team_repo)


NovelServiceDep = Annotated[NovelService, Depends(get_novel_service)]
