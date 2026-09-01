from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

CountryName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class CountryCreate(BaseModel):
    name: CountryName


class CountryResponse(CountryCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class CountryUpdate(BaseModel):
    name: CountryName | None = None
