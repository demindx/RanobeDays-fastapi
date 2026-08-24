from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository import PostgresRepository
from src.country.models import Country
from src.country.schemas import CountryUpdate


class CountryRepository(PostgresRepository[Country, CountryUpdate]):
    model: type[Country] = Country

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
