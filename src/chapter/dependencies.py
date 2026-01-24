from typing import Annotated

from fastapi import Depends

from src.chapter.models import Chapter
from src.chapter.repository import ChapterRepository
from src.chapter.service import ChapterService
from src.core.dependencies import DbSession


def get_chapter_repo(session: DbSession) -> ChapterRepository:
    return ChapterRepository(session, Chapter)


def get_chapter_service(
    repo: Annotated[ChapterRepository, Depends(get_chapter_repo)],
) -> ChapterService:
    return ChapterService(repo)


ChapterServiceDep = Annotated[ChapterService, Depends(get_chapter_service)]
