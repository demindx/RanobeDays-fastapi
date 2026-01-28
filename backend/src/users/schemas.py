from pydantic import BaseModel, EmailStr, ValidationError, model_validator

from src.teams.models import TeamUserRole
from src.users.models import UserRoleEnum


class UserResponse(BaseModel):
    email: EmailStr
    role: UserRoleEnum
    user_profile: UserProfileResponse

    class Config:
        from_attributes = True


class UserTeamResponse(BaseModel):
    role: TeamUserRole
    nickname: str

    @staticmethod
    def from_tuple(data: tuple) -> UserTeamResponse:
        return UserTeamResponse(nickname=data[0], role=data[1])


class UserLogin(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    password: str
    fingerprint: str


class UserRegister(BaseModel):
    login: str
    email: EmailStr
    nickname: str
    password1: str
    password2: str

    @model_validator(mode="after")
    def validate_user(self) -> UserRegister:
        if self.password1 != self.password2:
            raise ValidationError("Passwords mismatch")

        return self

    def get_password(self):
        return self.password1


class UserPasswordUpdate(BaseModel):
    password1: str
    password2: str

    @model_validator(mode="after")
    def validate_password(self) -> UserPasswordUpdate:
        if self.password1 != self.password2:
            raise ValidationError("Passwords mismatch")

        return self


class UserProfileCreate(BaseModel):
    user_id: int
    nickname: str
    readed_chapters: int = 0


class UserProfileUpdate(BaseModel):
    nickname: str | None = None
    readed_chapters: int | None = None


class UserProfileResponse(BaseModel):
    nickname: str
    readed_chapters: int

    class Config:
        from_attributes = True
