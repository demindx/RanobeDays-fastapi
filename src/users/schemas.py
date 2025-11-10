from pydantic import BaseModel, EmailStr, ValidationError, model_validator

from src.users.models import UserRoleEnum


class UserResponse(BaseModel):
    login: str
    email: EmailStr
    password_hash: str
    role: UserRoleEnum

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    password: str
    fingerprint: str


class UserRegister(BaseModel):
    login: str
    email: EmailStr
    password1: str
    password2: str

    @model_validator(mode="after")
    def validate_user(self) -> "UserRegister":
        if self.password1 != self.password2:
            raise ValidationError("Passwords mismatch")

        return self

    def get_password(self):
        return self.password1


class UserPasswordUpdate(BaseModel):
    password1: str
    password2: str

    @model_validator(mode="after")
    def validate_password(self) -> "UserPasswordUpdate":
        if self.password1 != self.password2:
            raise ValidationError("Passwords mismatch")

        return self


class UserProfileCreate(BaseModel):
    first_name: str
    last_name: str


class UserProfileUpdate(BaseModel):
    readed_chapters: int | None = None


class UserProfileResponse(BaseModel):
    readed_chapters: int

    class Config:
        from_attributes = True
