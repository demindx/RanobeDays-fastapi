from fastapi import status
from pydantic import BaseModel, Field


class GenericResponse[T](BaseModel):
    code: int = Field(default=status.HTTP_200_OK)
    message: str = Field(default="success")
    data: T | None = None
