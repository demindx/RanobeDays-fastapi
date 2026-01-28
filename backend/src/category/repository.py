from sqlalchemy.ext.asyncio import AsyncSession

from src.category.model import Category
from src.category.schemas import CategoryUpdate
from src.core.repository import PostgresRepository


class CategoryRepository(PostgresRepository[Category, CategoryUpdate]):
    def __init__(self, session: AsyncSession, model: type[Category]) -> None:
        super().__init__(session, model)
