"""Фабрики для создания тестовых данных."""

import factory
from factory import Faker

from src.users.models import UserModel, UserProfileModel, UserRoleEnum


class UserModelFactory(factory.Factory):
    class Meta:
        model = UserModel

    id = factory.Sequence(lambda n: n)
    login = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.login}@example.com")
    password_hash = Faker("password", length=60)
    role = UserRoleEnum.COMMON
    is_active = True


class UserProfileModelFactory(factory.Factory):
    class Meta:
        model = UserProfileModel

    id = factory.Sequence(lambda n: n)
    user_id = factory.Sequence(lambda n: n)
    readed_chapters = 0


class AdminUserFactory(UserModelFactory):
    role = UserRoleEnum.ADMIN
    login = factory.Sequence(lambda n: f"admin{n}")


class ManagerUserFactory(UserModelFactory):
    role = UserRoleEnum.MANAGER
    login = factory.Sequence(lambda n: f"manager{n}")


class InactiveUserFactory(UserModelFactory):
    is_active = False
    login = factory.Sequence(lambda n: f"inactive{n}")
