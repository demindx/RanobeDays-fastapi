from pydantic import BaseModel, EmailStr, ValidationError, model_validator

from src.users.models import UserRoleEnum


class UserResponse(BaseModel):
    login: str
    email: EmailStr
    password_hash: str
    role: UserRoleEnum

    class Config:
        from_attributes = True


class UserLoginRequest(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    password: str
    fingerprint: str


class UserRegisterRequest(BaseModel):
    login: str
    email: EmailStr
    password1: str
    password2: str

    @model_validator(mode="after")
    def validate_user(self) -> "UserRegisterRequest":
        if self.password1 != self.password2:
            raise ValidationError("Passwords mismatch")

        return self

    def get_password(self):
        return self.password1


class UserPasswordUpdateRequest(BaseModel):
    password1: str
    password2: str

    @model_validator(mode="after")
    def validate_password(self) -> "UserPasswordUpdateRequest":
        if self.password1 != self.password2:
            raise ValidationError("Passwords mismatch")

        return self


class UserProfileCreateRequest(BaseModel):
    first_name: str
    last_name: str


class UserProfileUpdateRequest(BaseModel):
    readed_chapters: int | None = None


class UserProfileResponse(BaseModel):
    readed_chapters: int

    class Config:
        from_attributes = True
