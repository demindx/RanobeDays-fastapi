from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from src.category.model import CategoryTypeEnum

CategoryName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class CategoryCreate(BaseModel):
    name: CategoryName
    type: CategoryTypeEnum

    model_config = ConfigDict(extra="forbid")


class CategoryUpdate(BaseModel):
    name: CategoryName | None = None
    type: CategoryTypeEnum | None = None

    model_config = ConfigDict(extra="forbid")


class CategoryResponse(CategoryCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True, extra="forbid")
