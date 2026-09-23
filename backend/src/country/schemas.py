from typing import Annotated

from pydantic import ConfigDict, StringConstraints

from src.core.schemas import SchemaBase

CountryName = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]


class CountryCreate(SchemaBase):
    name: CountryName

class CountryResponse(CountryCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class CountryUpdate(SchemaBase):
    name: CountryName | None = None
