import uuid
from datetime import UTC, datetime, timedelta

from src.auth.exceptions import (
    CookieError,
    InvalidRefreshToken,
    RefreshSessionNotFound,
    TokenExpired,
    UserAuthDenied,
)
from src.auth.repository import AuthRepository
from src.auth.schemas import RefreshSessionCreate, RefreshSessionUpdate, Tokens
from src.auth.utils import generate_jwt_token
from src.core.exceptions import NotFound
from src.users.models import User
from src.users.schemas import UserLogin, UserProfileCreate, UserRegister
from src.users.service import UserProfileService, UserService
from src.users.utils import is_valid_password


class AuthService:
    def __init__(
        self,
        repo: AuthRepository,
        user_service: UserService,
        user_profile_service: UserProfileService,
    ):
        self.user_service: UserService = user_service
        self.user_profile_service: UserProfileService = user_profile_service
        self.repository: AuthRepository = repo

    async def register(self, data: UserRegister):
        user = await self.user_service.create(data)

        profile_data = UserProfileCreate(nickname=data.nickname, user_id=user.id)

        _ = await self.user_profile_service.create(profile_data)

    async def _user_auth(self, data: UserLogin) -> User:
        user: User | None = None

        if data.login:
            user = await self.user_service.get_by_login(data.login)
        elif data.email:
            user = await self.user_service.get_by_email(data.email)

        if not user:
            raise NotFound(
                User, self._user_auth.__name__, data.login if data.login else data.email
            )

        if not is_valid_password(data.password, user.password_hash):
            raise UserAuthDenied(
                f"{'Login' if data.login else 'Email'} or password are is incorrect"
            )

        return user

    async def login(self, data: UserLogin) -> Tokens:
        user = await self._user_auth(data)

        expires_in = int((datetime.now(UTC) + timedelta(weeks=4)).timestamp())
        refresh_session = await self.repository.create_refresh_session(
            RefreshSessionCreate(
                user_id=user.id,
                refresh_token=uuid.uuid4(),
                fingerprint=data.fingerprint,
                expires_in=expires_in,
            )
        )

        access_token = generate_jwt_token(user.id)

        return Tokens(
            access_token=access_token, refresh_token=refresh_session.refresh_token
        )

    async def refresh_token(self, data: RefreshSessionUpdate) -> Tokens:
        try:
            session = await self.repository.get_refresh_session(data.refresh_token)
        except RefreshSessionNotFound:
            raise InvalidRefreshToken

        if session.fingerprint != data.fingerprint:
            raise InvalidRefreshToken

        await self.repository.delete(session)

        if datetime.now(UTC).timestamp() >= session.expires_in:
            raise InvalidRefreshToken

        expires_in = int((datetime.now(UTC) + timedelta(weeks=4)).timestamp())

        new_session = await self.repository.create_refresh_session(
            RefreshSessionCreate(
                user_id=session.user_id,
                refresh_token=uuid.uuid4(),
                fingerprint=session.fingerprint,
                expires_in=expires_in,
            )
        )

        access_token = generate_jwt_token(new_session.user_id)

        return Tokens(
            access_token=access_token, refresh_token=new_session.refresh_token
        )

    async def logout(self, refresh_token: str):
        session = await self.repository.get_refresh_session(
            uuid.UUID(hex=refresh_token)
        )
        await self.repository.delete(session)
