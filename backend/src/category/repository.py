from sqlalchemy.ext.asyncio import AsyncSession

from src.category.model import Category
from src.category.schemas import CategoryUpdate
from src.core.repository import PostgresRepository


class CategoryRepository(PostgresRepository[Category, CategoryUpdate]):
    model: type[Category] = Category

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
