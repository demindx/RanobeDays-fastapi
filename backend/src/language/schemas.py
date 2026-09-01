from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

LanguageName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class LanguageCreate(BaseModel):
    name: LanguageName


class LanguageResponse(LanguageCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class LanguageUpdate(BaseModel):
    name: LanguageName | None = None
