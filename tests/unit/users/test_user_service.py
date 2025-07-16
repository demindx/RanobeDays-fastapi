"""Unit тесты для UserService."""

from unittest.mock import AsyncMock

import bcrypt
import pytest

from src.users.exceptions import UserAlreadyExists, UserNotFound, UserProfileNotFound
from src.users.models import UserRoleEnum
from src.users.repository import UserRepository
from src.users.schemas import (
    UserProfileResponse,
    UserProfileUpdateRequest,
    UserRegisterRequest,
    UserResponse,
)
from src.users.service import UserService
from tests.factories import UserModelFactory, UserProfileModelFactory


@pytest.mark.unit
class TestUserService:
    """Тесты для UserService."""

    @pytest.fixture
    def mock_repository(self):
        """Мок-репозиторий для тестов."""
        return AsyncMock(spec=UserRepository)

    @pytest.fixture
    def user_service(self, mock_repository):
        """Сервис пользователей с мок-репозиторием."""
        return UserService(mock_repository)

    @pytest.fixture
    def sample_user(self):
        """Образец пользователя для тестов."""
        return UserModelFactory.build()

    @pytest.fixture
    def sample_profile(self):
        """Образец профиля для тестов."""
        return UserProfileModelFactory.build()

    async def test_create_user_success(self, user_service, mock_repository):
        """Тест успешного создания пользователя."""
        # Arrange
        request_data = UserRegisterRequest(
            login="newuser",
            email="newuser@example.com",
            password1="password123",
            password2="password123",
        )

        # Пользователь не существует
        mock_repository.get_user_by_login.return_value = None

        # Мокаем создание пользователя - имитируем что БД присваивает ID и default значения
        def mock_create_user(user_obj):
            user_obj.id = 1  # Имитируем присваивание ID от БД
            user_obj.role = UserRoleEnum.COMMON  # Имитируем default значение
            return user_obj

        mock_repository.create_user.side_effect = mock_create_user
        mock_repository.create_user_profile.return_value = (
            UserProfileModelFactory.build()
        )

        # Act
        result = await user_service.create_user(request_data)

        # Assert
        assert isinstance(result, UserResponse)
        assert result.login == request_data.login
        assert result.email == request_data.email

        # Проверяем вызовы репозитория
        mock_repository.get_user_by_login.assert_called_once_with(request_data.login)
        mock_repository.create_user.assert_called_once()
        mock_repository.create_user_profile.assert_called_once()

        # Проверяем, что пароль захеширован
        user_call_args = mock_repository.create_user.call_args[0][0]
        assert user_call_args.password_hash != request_data.password1
        assert bcrypt.checkpw(
            request_data.password1.encode("utf-8"),
            user_call_args.password_hash.encode("utf-8"),
        )

    async def test_create_user_already_exists(self, user_service, mock_repository):
        """Тест создания пользователя, который уже существует."""
        # Arrange
        request_data = UserRegisterRequest(
            login="existinguser",
            email="existing@example.com",
            password1="password123",
            password2="password123",
        )

        # Пользователь уже существует
        existing_user = UserModelFactory.build(login=request_data.login)
        mock_repository.get_user_by_login.return_value = existing_user

        # Act & Assert
        with pytest.raises(UserAlreadyExists):
            await user_service.create_user(request_data)

        # Проверяем, что репозиторий не вызывался для создания
        mock_repository.create_user.assert_not_called()
        mock_repository.create_user_profile.assert_not_called()

    async def test_get_user_success(self, user_service, mock_repository, sample_user):
        """Тест успешного получения пользователя."""
        # Arrange
        user_id = 1
        mock_repository.get_user.return_value = sample_user

        # Act
        result = await user_service.get_user(user_id)

        # Assert
        assert isinstance(result, UserResponse)
        assert result.login == sample_user.login
        mock_repository.get_user.assert_called_once_with(user_id)

    async def test_get_user_not_found(self, user_service, mock_repository):
        """Тест получения несуществующего пользователя."""
        # Arrange
        user_id = 999
        mock_repository.get_user.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFound):
            await user_service.get_user(user_id)

    async def test_get_all_users_success(self, user_service, mock_repository):
        """Тест получения всех пользователей."""
        # Arrange
        users = [UserModelFactory.build() for _ in range(3)]
        mock_repository.get_all_users.return_value = users

        # Act
        result = await user_service.get_all_users()

        # Assert
        assert len(result) == 3
        assert all(isinstance(user, UserResponse) for user in result)
        mock_repository.get_all_users.assert_called_once()

    async def test_get_all_users_empty(self, user_service, mock_repository):
        """Тест получения пустого списка пользователей."""
        # Arrange
        mock_repository.get_all_users.return_value = []

        # Act
        result = await user_service.get_all_users()

        # Assert
        assert result == []
        mock_repository.get_all_users.assert_called_once()

    async def test_get_user_profile_success(
        self, user_service, mock_repository, sample_profile
    ):
        """Тест успешного получения профиля пользователя."""
        # Arrange
        user_id = 1
        mock_repository.get_user_profile.return_value = sample_profile

        # Act
        result = await user_service.get_user_profile(user_id)

        # Assert
        assert isinstance(result, UserProfileResponse)
        assert result.readed_chapters == sample_profile.readed_chapters
        mock_repository.get_user_profile.assert_called_once_with(user_id)

    async def test_get_user_profile_not_found(self, user_service, mock_repository):
        """Тест получения несуществующего профиля."""
        # Arrange
        user_id = 999
        mock_repository.get_user_profile.return_value = None

        # Act & Assert
        with pytest.raises(UserProfileNotFound):
            await user_service.get_user_profile(user_id)

    async def test_update_user_profile_success(
        self, user_service, mock_repository, sample_profile
    ):
        """Тест успешного обновления профиля пользователя."""
        # Arrange
        user_id = 1
        update_data = UserProfileUpdateRequest(readed_chapters=50)

        mock_repository.get_user_profile.return_value = sample_profile
        updated_profile = UserProfileModelFactory.build(readed_chapters=50)
        mock_repository.update_user_profile.return_value = updated_profile

        # Act
        result = await user_service.update_user_profile(user_id, update_data)

        # Assert
        assert isinstance(result, UserProfileResponse)
        assert result.readed_chapters == 50
        mock_repository.get_user_profile.assert_called_once_with(user_id)
        mock_repository.update_user_profile.assert_called_once()

    async def test_activate_user_success(
        self, user_service, mock_repository, sample_user
    ):
        """Тест активации пользователя."""
        # Arrange
        user_id = 1
        sample_user.is_active = False
        mock_repository.get_user.return_value = sample_user

        activated_user = UserModelFactory.build(is_active=True)
        mock_repository.update_user.return_value = activated_user

        # Act
        result = await user_service.activate_user(user_id)

        # Assert
        assert isinstance(result, UserResponse)
        mock_repository.get_user.assert_called_once_with(user_id)
        mock_repository.update_user.assert_called_once()

    async def test_deactivate_user_success(
        self, user_service, mock_repository, sample_user
    ):
        """Тест деактивации пользователя."""
        # Arrange
        user_id = 1
        sample_user.is_active = True
        mock_repository.get_user.return_value = sample_user

        deactivated_user = UserModelFactory.build(is_active=False)
        mock_repository.update_user.return_value = deactivated_user

        # Act
        result = await user_service.deactivate_user(user_id)

        # Assert
        assert isinstance(result, UserResponse)
        mock_repository.get_user.assert_called_once_with(user_id)
        mock_repository.update_user.assert_called_once()

    async def test_delete_user_success(self, user_service, mock_repository):
        """Тест удаления пользователя."""
        # Arrange
        user_id = 1
        mock_repository.delete_user.return_value = None

        # Act
        await user_service.delete_user(user_id)

        # Assert
        mock_repository.delete_user.assert_called_once_with(user_id)

    def test_get_password_hash(self, user_service):
        """Тест хеширования пароля."""
        # Arrange
        password = "testpassword123"

        # Act
        hashed = user_service._get_password_hash(password)

        # Assert
        assert hashed != password
        assert bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
