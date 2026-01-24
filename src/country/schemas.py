from pydantic import BaseModel


class CountryCreate(BaseModel):
    name: str


class CountryResponse(CountryCreate):
    class Config:
        from_attributes = True


class CountryUpdate(BaseModel):
    name: str | None = None
