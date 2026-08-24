from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.chapter.models import Chapter
from src.core.repository import PostgresRepository


class ChapterRepository(PostgresRepository[Chapter, BaseModel]):
    model: type[Chapter] = Chapter

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
