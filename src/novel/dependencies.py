from typing import Annotated

from fastapi import Depends

from src.core.dependencies import DbSession
from src.novel.models import Novel
from src.novel.repository import NovelRepository
from src.novel.service import NovelService


def get_novel_repo(session: DbSession) -> NovelRepository:
    return NovelRepository(session, Novel)


def get_novel_service(
    repo: Annotated[NovelRepository, Depends(get_novel_repo)],
) -> NovelService:
    return NovelService(repo)


NovelServiceDep = Annotated[NovelService, Depends(get_novel_service)]
