from sqlalchemy.ext.asyncio import AsyncSession

from src.bookmark.models import Bookmark
from src.bookmark.schemas import BookmarkUpdate
from src.core.repository import PostgresRepository


class BookmarkRepository(PostgresRepository[Bookmark, BookmarkUpdate]):
    model: type[Bookmark] = Bookmark

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
