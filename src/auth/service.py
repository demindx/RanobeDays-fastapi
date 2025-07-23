import uuid
from datetime import UTC, datetime, timedelta

from src.auth.exceptions import TokenExpired, UserAuthDenied
from src.auth.repository import AuthRepository
from src.auth.schemas import RefreshSessionCreate, Tokens
from src.auth.utils import generate_jwt_token
from src.users.exceptions import UserNotFound
from src.users.models import User
from src.users.schemas import UserLoginRequest, UserRegisterRequest
from src.users.service import UserService
from src.users.utils import is_valid_password


class AuthService:
    def __init__(self, repo: AuthRepository, user_service: UserService):
        self.user_service: UserService = user_service
        self.repository: AuthRepository = repo

    async def register(self, data: UserRegisterRequest):
        await self.user_service.create_user(data)

    async def _user_auth(self, data: UserLoginRequest) -> User:
        user: User | None = None

        if data.login:
            user = await self.user_service.repository.get_user_by_login(data.login)
        elif data.email:
            user = await self.user_service.repository.get_user_by_email(data.email)

        if not user:
            raise UserNotFound

        if not is_valid_password(data.password, user.password_hash):
            raise UserAuthDenied(
                f"{'Login' if data.login else 'Email'} or password are is incorrect"
            )

        return user

    async def login(self, data: UserLoginRequest) -> Tokens:
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

    async def refresh_token(self, refresh_token: uuid.UUID) -> Tokens:
        session = await self.repository.get_refresh_session(refresh_token)

        await self.repository.delete(session)

        if datetime.now(UTC).timestamp() >= session.expires_in:
            raise TokenExpired

        expires_in = int((datetime.now(UTC) + timedelta(weeks=4)).timestamp())
        new_session = await self.repository.create_refresh_session(
            RefreshSessionCreate(
                user_id=session.user_id,
                refresh_token=uuid.uuid4(),
                fingerprint=str(uuid.uuid4()),
                expires_in=expires_in,
            )
        )

        access_token = generate_jwt_token(new_session.user_id)

        return Tokens(
            access_token=access_token, refresh_token=new_session.refresh_token
        )

    async def logout(self, refresh_token: uuid.UUID):
        session = await self.repository.get_refresh_session(refresh_token)
        await self.repository.delete(session)
