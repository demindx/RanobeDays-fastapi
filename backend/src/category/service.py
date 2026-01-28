from src.category.model import Category
from src.category.repository import CategoryRepository
from src.category.schemas import CategoryCreate, CategoryUpdate
from src.core.service import AbstractService


class CategoryService(
    AbstractService[Category, CategoryCreate, CategoryUpdate, CategoryRepository]
):
    def __init__(self, repository: CategoryRepository) -> None:
        super().__init__(repository)
