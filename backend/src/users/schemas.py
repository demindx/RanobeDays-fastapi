from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    ValidationError,
    model_validator,
)

from src.config import config
from src.users.models import UserRoleEnum

Login = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$"
    ),
]

Nickname = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2)]

UserEmail = Annotated[EmailStr, Field(max_length=100)]


def validate_bcrypt_password(value: str) -> str:
    if len(value.encode("utf-8")) > 72:
        raise ValueError("Password must not exceed 72 bytes")

    return value


def validate_new_password(value: str) -> str:
    if len(value) < config.MIN_PASSWORD_LEN:
        raise ValueError(f"Password must contain at least {config.MIN_PASSWORD_LEN}")

    return validate_bcrypt_password(value)


PasswordInput = Annotated[str, AfterValidator(validate_bcrypt_password)]
NewPassword = Annotated[str, AfterValidator(validate_new_password)]


class UserResponse(BaseModel):
    email: UserEmail
    role: UserRoleEnum
    user_profile: UserProfileResponse

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    login: Login | None = None
    email: UserEmail | None = None
    password: PasswordInput

    @model_validator(mode="after")
    def validate_user_login(self) -> UserLogin:
        if self.login is not None and self.email is not None:
            raise ValueError(
                "In login request cannot be provided email and login simultaneously"
            )

        if self.login is None and self.email is None:
            raise ValueError("Must be provided login or email")
        return self


class UserRegister(BaseModel):
    login: Login
    email: UserEmail
    nickname: Nickname

    password1: NewPassword
    password2: NewPassword

    @model_validator(mode="after")
    def validate_user(self) -> UserRegister:
        if self.password1 != self.password2:
            raise ValueError("Passwords mismatch")

        return self

    def get_password(self):
        return self.password1


class UserPasswordUpdate(BaseModel):
    password1: NewPassword
    password2: NewPassword

    @model_validator(mode="after")
    def validate_password(self) -> UserPasswordUpdate:
        if self.password1 != self.password2:
            raise ValidationError("Passwords mismatch")

        return self


class UserProfileCreate(BaseModel):
    user_id: int
    nickname: Nickname
    readed_chapters: int = 0


class UserProfileUpdate(BaseModel):
    nickname: Nickname | None = None
    readed_chapters: int | None = None


class UserProfileResponse(BaseModel):
    nickname: Nickname
    readed_chapters: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)
