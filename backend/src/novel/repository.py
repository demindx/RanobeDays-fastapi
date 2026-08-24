from sqlalchemy.ext.asyncio import AsyncSession

from src.core.repository import PostgresRepository
from src.novel.models import Novel
from src.novel.schemas import NovelUpdate


class NovelRepository(PostgresRepository[Novel, NovelUpdate]):
    model: type[Novel] = Novel

    def __init__(self, session: AsyncSession):
        super().__init__(session)
