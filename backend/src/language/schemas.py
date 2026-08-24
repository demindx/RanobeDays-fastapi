from pydantic import BaseModel, ConfigDict


class LanguageCreate(BaseModel):
    name: str


class LanguageResponse(LanguageCreate):
    id: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class LanguageUpdate(BaseModel):
    name: str | None = None
