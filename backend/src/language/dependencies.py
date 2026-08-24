from typing import Annotated

from fastapi import Depends

from src.core.dependencies import DbSession
from src.language.repository import LanguageRepository
from src.language.service import LanguageService


def get_language_repo(session: DbSession) -> LanguageRepository:
    return LanguageRepository(session)


def get_language_service(
    repo: Annotated[LanguageRepository, Depends(get_language_repo)],
) -> LanguageService:
    return LanguageService(repo)


LanguageServiceDep = Annotated[LanguageService, Depends(get_language_service)]
