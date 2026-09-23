from fastapi import status
from pydantic import BaseModel, ConfigDict, Field

from src.config import config


class SchemaBase(BaseModel):
    """Common API schema defaults."""

    model_config = ConfigDict(extra="forbid")


def is_not_whitespaces(value: str | None):
    if value is None:
        return value

    if len(value) == 0 or value.isspace():
        raise ValueError("string cannot be empty of whitespaces")

    return value


class Pagination(SchemaBase):
    limit: int = Field(default=config.DEFAULT_PAGINATION_LIMIT, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class GenericResponse[T](SchemaBase):
    code: int = Field(default=status.HTTP_200_OK)
    message: str = Field(default="success")
    data: T | None = None

class GenericPaginationResponse[T](GenericResponse[list[T]]):
    offset: int = Field(default=0)
    limit: int = Field(default=config.DEFAULT_PAGINATION_LIMIT)
