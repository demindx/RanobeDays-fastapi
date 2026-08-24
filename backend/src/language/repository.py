from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository import PostgresRepository
from src.language.models import Language
from src.language.schemas import LanguageUpdate


class LanguageRepository(PostgresRepository[Language, LanguageUpdate]):
    model: type[Language] = Language

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
