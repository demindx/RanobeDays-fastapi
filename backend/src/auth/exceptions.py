from fastapi import status

from src.core.exceptions import AppException


class UserAuthDenied(AppException):
    def __init__(self, message: str, status: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status)


class TokenError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)


class TokenExpired(AppException):
    def __init__(self):
        super().__init__("Token has been expired", status.HTTP_401_UNAUTHORIZED)


class CookieError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED):
        super().__init__(message, status_code)


class InvalidTokenError(TokenError): ...


class RefreshSessionCreationError(AppException):
    def __init__(self):
        super().__init__("Failed to create session", status.HTTP_401_UNAUTHORIZED)


class RefreshSessionNotFound(AppException):
    def __init__(self):
        super().__init__("Refresh session not found", status.HTTP_404_NOT_FOUND)


class NotAuthenticated(AppException):
    def __init__(self):
        super().__init__("Not authenticated", status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppException):
    def __init__(self):
        super().__init__("Not allowed", status.HTTP_403_FORBIDDEN)


class InvalidRefreshToken(AppException):
    def __init__(self):
        super().__init__("Invalid refresh token", status.HTTP_401_UNAUTHORIZED)


class RefreshSessionError(AppException):
    def __init__(self):
        super().__init__(
            "Something wrong with refresh session", status.HTTP_401_UNAUTHORIZED
        )
