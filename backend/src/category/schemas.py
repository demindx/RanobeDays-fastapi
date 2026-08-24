from pydantic import BaseModel, ConfigDict

from src.category.model import CategoryTypeEnum


class CategoryCreate(BaseModel):
    name: str
    type: CategoryTypeEnum


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: CategoryTypeEnum | None = None


class CategoryResponse(CategoryCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)
