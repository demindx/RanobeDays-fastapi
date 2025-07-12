from fastapi import status

from src.core.exceptions import BaseException


class UserNotFound(BaseException):
    def __init__(self):
        super().__init__("User not found", status.HTTP_404_NOT_FOUND)


class UserProfileNotFound(BaseException):
    def __init__(self):
        super().__init__("User profile not found", status.HTTP_404_NOT_FOUND)


class UserAlreadyExists(BaseException):
    def __init__(self):
        super().__init__("User with this login or email already exists", status.HTTP_404_NOT_FOUND)
