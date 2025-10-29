from typing import Any
from fastapi import status

from src.core.models import Base


class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(self.message)

        self.message: str = message
        self.status_code: int = status_code


class AlreadyExists(AppException):
    def __init__(self, model: type[Base[Any]]):
        super().__init__(f"{model.__name__} already exists", status.HTTP_400_BAD_REQUEST)


class NotFound(AppException):
    def __init__(self, model: type[Base[Any]], cred_type: str, cred: Any):
        super().__init__(f"{model.__name__} was not found by {cred_type}: {cred}", status.HTTP_404_NOT_FOUND)
