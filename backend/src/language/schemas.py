from typing import Annotated

from pydantic import ConfigDict, StringConstraints

from src.core.schemas import SchemaBase

LanguageName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class LanguageCreate(SchemaBase):
    name: LanguageName


class LanguageResponse(LanguageCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class LanguageUpdate(SchemaBase):
    name: LanguageName | None = None
