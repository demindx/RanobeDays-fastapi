from typing import TYPE_CHECKING, Any

from fastapi import status

if TYPE_CHECKING:
    from src.core.models import Base


class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message: str = message
        self.status_code: int = status_code

        super().__init__(self.message)


class AlreadyExists(AppException):
    def __init__(self, model: type["Base[Any, Any]"]):
        super().__init__(
            f"{model.__name__} already exists", status.HTTP_400_BAD_REQUEST
        )


class NotFound(AppException):
    def __init__(self, model: type["Base[Any, Any]"], cred_type: str, cred: Any):
        super().__init__(
            f"{model.__name__} was not found by {cred_type}: {cred}",
            status.HTTP_404_NOT_FOUND,
        )


class NoneObjectEncoutered(AppException):
    def __init__(self):
        super().__init__(
            "None object was encountered", status.HTTP_500_INTERNAL_SERVER_ERROR
        )
