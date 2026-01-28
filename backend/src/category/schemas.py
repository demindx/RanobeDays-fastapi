from pydantic import BaseModel

from src.category.model import CategoryTypeEnum


class CategoryCreate(BaseModel):
    name: str
    type: CategoryTypeEnum


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: CategoryTypeEnum | None = None


class CategoryReponse(CategoryCreate):
    class Config:
        from_attributes = True
