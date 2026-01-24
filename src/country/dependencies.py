from typing import Annotated

from fastapi import Depends

from src.core.dependencies import DbSession
from src.country.models import Country
from src.country.repository import CountryRepository
from src.country.service import CountryService


def get_country_repo(session: DbSession) -> CountryRepository:
    return CountryRepository(session, Country)


def get_country_service(
    repo: Annotated[CountryRepository, Depends(get_country_repo)],
) -> CountryService:
    return CountryService(repo)


CountryServiceDep = Annotated[CountryService, Depends(get_country_service)]
