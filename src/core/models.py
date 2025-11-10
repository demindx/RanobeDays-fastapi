from datetime import UTC, datetime
from typing import Self

from pydantic import BaseModel
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.core.exceptions import NoneObjectEncoutered


class Base[T, Scheme: BaseModel | None](DeclarativeBase):
    __abstract__ = True
    id: Mapped[T]

    @classmethod
    def from_data(cls, data: Scheme) -> Self:
        if data is not None:
            return cls(**data.model_dump())

        raise NoneObjectEncoutered


class BaseTimestamps:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
