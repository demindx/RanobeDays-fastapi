from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.auth.exceptions import NotAuthenticated


class JwtHeaderBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(
            request
        )
        if credentials:
            if not credentials.scheme.lower() == "bearer":
                raise NotAuthenticated

            return credentials.credentials
