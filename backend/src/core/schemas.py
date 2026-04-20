from fastapi import status
from pydantic import BaseModel, Field

from config import config


class GenericResponse[T](BaseModel):
    code: int = Field(default=status.HTTP_200_OK)
    message: str = Field(default="success")
    data: T | None = None


class GenericPaginationResponse[T](GenericResponse[list[T]]):
    offset: int = Field(default=0)
    limit: int = Field(default=config.DEFAULT_PAGINATION_LIMIT)
