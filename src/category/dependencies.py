from typing import Annotated

from fastapi import Depends

from src.category.model import Category
from src.category.repository import CategoryRepository
from src.category.service import CategoryService
from src.core.dependencies import DbSession


def get_category_repo(session: DbSession) -> CategoryRepository:
    return CategoryRepository(session, Category)


def get_category_service(
    repo: Annotated[CategoryRepository, Depends(get_category_repo)],
) -> CategoryService:
    return CategoryService(repo)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
