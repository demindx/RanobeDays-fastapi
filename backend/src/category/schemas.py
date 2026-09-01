from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from src.category.model import CategoryTypeEnum

CategoryName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class CategoryCreate(BaseModel):
    name: CategoryName
    type: CategoryTypeEnum


class CategoryUpdate(BaseModel):
    name: CategoryName | None = None
    type: CategoryTypeEnum | None = None


class CategoryResponse(CategoryCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)
