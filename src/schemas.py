from pydantic import BaseModel, Field


class GenericResponse[T](BaseModel):
    code: int = Field(default=200)
    message: str = Field(default="success")
    data: T | None = None
