from src.core.service import AbstractService
from src.country.models import Country
from src.country.repository import CountryRepository
from src.country.schemas import CountryCreate, CountryUpdate


class CountryService(
    AbstractService[Country, CountryCreate, CountryUpdate, CountryRepository]
):
    def __init__(self, repository: CountryRepository) -> None:
        super().__init__(repository)
