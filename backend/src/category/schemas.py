from typing import Annotated

from pydantic import ConfigDict, StringConstraints

from src.category.model import CategoryTypeEnum
from src.core.schemas import SchemaBase

CategoryName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class CategoryCreate(SchemaBase):
    name: CategoryName
    type: CategoryTypeEnum

class CategoryUpdate(SchemaBase):
    name: CategoryName | None = None
    type: CategoryTypeEnum | None = None

class CategoryResponse(CategoryCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)
