from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from src.category.schemas import CategoryResponse
from src.country.schemas import CountryResponse
from src.language.schemas import LanguageResponse
from src.novel.models import NovelStatus, NovelType

NovelTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
]
NovelSlug = Annotated[str, StringConstraints(min_length=1, max_length=255)]
CoverPath = Annotated[str, StringConstraints(min_length=1, max_length=255)]
NovelDescription = Annotated[str, StringConstraints(min_length=1)]


class NovelCreate(BaseModel):
    title: NovelTitle
    age_limit: int
    team_id: int
    language_id: int
    country_id: int
    description: NovelDescription
    publish_date: datetime
    type: NovelType


class NovelUpdate(BaseModel):
    title: NovelTitle | None = None
    age_limit: int | None = None
    language_id: int | None = None
    country_id: int | None = None
    description: NovelDescription | None = None
    publish_date: datetime | None = None
    type: NovelType | None = None
    status: NovelStatus | None = None


class NovelResponse(BaseModel):
    id: int
    title: NovelTitle
    slug: NovelSlug
    description: NovelDescription
    type: NovelType
    status: NovelStatus
    publish_date: datetime
    age_limit: int
    cover_path: CoverPath
    language: LanguageResponse
    country: CountryResponse
    categories: list[CategoryResponse]

    model_config: ConfigDict = ConfigDict(from_attributes=True)
