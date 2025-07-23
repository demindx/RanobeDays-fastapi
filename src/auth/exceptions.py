from fastapi import status

from src.core.exceptions import BaseException


class UserAuthDenied(BaseException):
    def __init__(self, message: str, status: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status)


class TokenError(BaseException):
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)


class TokenExpired(BaseException):
    def __init__(self):
        super().__init__("Token has been expired", status.HTTP_401_UNAUTHORIZED)


class CookieError(BaseException):
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)


class InvalidTokenError(TokenError): ...


class RefreshSessionCreationError(BaseException):
    def __init__(self):
        super().__init__("Failed to create session", status.HTTP_401_UNAUTHORIZED)


class RefreshSessionNotFound(BaseException):
    def __init__(self):
        super().__init__("Refresh session not found", status.HTTP_404_NOT_FOUND)


class NotAuthenticated(BaseException):
    def __init__(self):
        super().__init__("Not authenticated", status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(BaseException):
    def __init__(self):
        super().__init__("Not allowed", status.HTTP_403_FORBIDDEN)
