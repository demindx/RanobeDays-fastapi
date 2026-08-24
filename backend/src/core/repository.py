import uuid
from abc import ABC, abstractmethod
from typing import Any, override

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import AlreadyExists, NotFound
from src.core.models import Base


class AbstractRepository[ModelType: Base[Any], UpdateSchema: BaseModel](ABC):
    model: type[ModelType]

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    @abstractmethod
    async def get_by_id(self, id: Any) -> ModelType: ...

    @abstractmethod
    async def get_all(self, limit: int, offset: int) -> list[ModelType]: ...

    @abstractmethod
    async def create(self, instance: ModelType) -> ModelType: ...

    @abstractmethod
    async def update(self, id: Any, data: UpdateSchema) -> ModelType: ...

    @abstractmethod
    async def delete(self, id: Any) -> None: ...


class PostgresRepository[ModelType: Base[Any], UpdateSchema: BaseModel](
    AbstractRepository[ModelType, UpdateSchema]
):
    @override
    async def get_by_id(self, id: int | uuid.UUID) -> ModelType:
        stmt = select(self.model).where(self.model.id == id)

        try:
            result = (await self.session.execute(stmt)).scalar_one()
        except NoResultFound:
            raise NotFound(self.model, self.get_by_id.__name__, id)

        return result

    @override
    async def get_all(self, limit: int, offset: int) -> list[ModelType]:
        stmt = select(self.model).limit(limit).offset(offset)

        result = (await self.session.execute(stmt)).scalars()

        return list(result)

    @override
    async def create(self, instance: ModelType) -> ModelType:
        try:
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
        except IntegrityError as e:
            err = str(e)

            if "unique" in err:
                raise AlreadyExists(self.model)

            raise

        return instance

    @override
    async def update(self, id: int | uuid.UUID, data: UpdateSchema) -> ModelType:
        instance = await self.get_by_id(id)

        for field, value in data.model_dump(
            exclude_none=True, exclude_unset=True
        ).items():
            if hasattr(instance, field):
                setattr(instance, field, value)

        try:
            self.session.add(instance)
            await self.session.flush()
            await self.session.refresh(instance)
        except IntegrityError as e:
            err = str(e)

            if "unique" in err:
                raise AlreadyExists(self.model)

            raise

        return instance

    @override
    async def delete(self, id: int | uuid.UUID) -> None:
        stmt = delete(self.model).where(self.model.id == id)

        await self.session.execute(stmt)
        await self.session.flush()
