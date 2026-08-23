from pydantic import BaseModel, ConfigDict


class CountryCreate(BaseModel):
    name: str


class CountryResponse(CountryCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class CountryUpdate(BaseModel):
    name: str | None = None
