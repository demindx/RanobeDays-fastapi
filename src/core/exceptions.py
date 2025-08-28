from fastapi import status

from src.core.models import Base


class BaseException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message: str = message
        self.status_code: int = status_code

        super().__init__(self.message)


class AlreadyExists(BaseException):
    def __init__(self, model: type[Base]):
        super().__init__(f"{model.__name__} already exists", status.HTTP_400_BAD_REQUEST)


class NotFound(BaseException):
    def __init__(self, model: type[Base], cred_type: str, cred: any):
        super().__init__(f"{model.__name__} was not found by {cred_type}: {cred}", status.HTTP_404_NOT_FOUND)
