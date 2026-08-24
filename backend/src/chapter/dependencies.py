from typing import Annotated

from fastapi import Depends

from src.chapter.repository import ChapterRepository
from src.chapter.service import ChapterService
from src.core.dependencies import DbSession


def get_chapter_repo(session: DbSession) -> ChapterRepository:
    return ChapterRepository(session)


def get_chapter_service(
    repo: Annotated[ChapterRepository, Depends(get_chapter_repo)],
) -> ChapterService:
    return ChapterService(repo)


ChapterServiceDep = Annotated[ChapterService, Depends(get_chapter_service)]
