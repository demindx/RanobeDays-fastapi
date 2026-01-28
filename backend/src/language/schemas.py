from pydantic import BaseModel


class LanguageCreate(BaseModel):
    name: str


class LanguageReponse(LanguageCreate):
    class Config:
        from_attributes = True


class LanguageUpdate(BaseModel):
    name: str | None = None
