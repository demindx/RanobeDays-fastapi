from typing import TYPE_CHECKING, Any

from fastapi import status

if TYPE_CHECKING:
    from src.core.models import Base


class AppException(Exception):
    def __init__(
        self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        self.message: str = message
        self.status_code: int = status_code

        super().__init__(self.message)


class AlreadyExists(AppException):
    def __init__(self, model: type[Base[Any]]):
        super().__init__(
            f"{model.__name__} already exists", status.HTTP_400_BAD_REQUEST
        )


class NotFound(AppException):
    def __init__(self, model: type[Base[Any]], field: str, value: Any):
        super().__init__(
            f"{model.__name__} was not found by {field}: {value}",
            status.HTTP_404_NOT_FOUND,
        )


class NoneObjectEncoutered(AppException):
    def __init__(self):
        super().__init__(
            "None object was encountered", status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class InvalidReference(AppException):
    def __init__(
        self,
        model: type[Base[Any]],
        field: str,
        value: Any,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        super().__init__(
            f"{model.__name__} with {field}={value} does not exists", status_code
        )
