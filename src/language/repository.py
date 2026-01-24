from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository import PostgresRepository
from src.language.models import Language
from src.language.schemas import LanguageUpdate


class LanguageRepository(PostgresRepository[Language, LanguageUpdate]):
    def __init__(self, session: AsyncSession, model: type[Language]) -> None:
        super().__init__(session, model)
