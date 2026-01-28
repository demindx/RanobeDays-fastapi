from typing import Any

from pydantic import BaseModel

from src.core.models import Base
from src.core.repository import AbstractRepository


class AbstractService[
    ModelType: Base[Any],
    CreateSchema: BaseModel,
    UpdateSchema: BaseModel,
    RepoType: AbstractRepository[Any, Any],
]:
    def __init__(self, repository: RepoType) -> None:
        self.__repo: RepoType = repository

    @property
    def repo(self) -> RepoType:
        return self.__repo

    async def get_by_id(self, id: Any) -> ModelType:
        return await self.repo.get_by_id(id)

    async def get_all(self, limit: int = 50, offset: int = 0) -> list[ModelType]:
        return await self.repo.get_all(limit, offset)

    async def create(self, data: CreateSchema) -> ModelType:
        instance = self.repo.model.from_data(data)

        return await self.repo.create(instance)

    async def update(self, id: Any, data: UpdateSchema) -> ModelType:
        return await self.repo.update(id, data)

    async def delete(self, id: Any) -> None:
        await self.repo.delete(id)
