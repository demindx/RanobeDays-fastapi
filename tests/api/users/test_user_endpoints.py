"""API тесты для user endpoints."""

import pytest
from httpx import AsyncClient

from src.users.models import UserModel, UserProfileModel, UserRoleEnum
from src.users.repository import UserRepository


@pytest.mark.api
class TestUserEndpoints:
    """Тесты для API endpoints пользователей."""

    async def test_get_users_empty(
        self, async_test_client: AsyncClient, override_get_db_session
    ):
        """Тест получения пустого списка пользователей."""
        # Act
        response = await async_test_client.get("/api/v1/users/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["message"] == "success"
        assert data["data"] == []

    async def test_get_users_with_data(
        self, async_test_client: AsyncClient, test_session, override_get_db_session
    ):
        """Тест получения списка пользователей с данными."""
        # Arrange - создаем пользователей в БД
        repo = UserRepository(test_session)

        user1 = UserModel(
            login="user1",
            email="user1@test.com",
            password_hash="hash1",
            role=UserRoleEnum.COMMON,
        )
        user2 = UserModel(
            login="user2",
            email="user2@test.com",
            password_hash="hash2",
            role=UserRoleEnum.ADMIN,
        )

        await repo.create_user(user1)
        await repo.create_user(user2)

        # Act
        response = await async_test_client.get("/api/v1/users/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert len(data["data"]) == 2

        logins = [user["login"] for user in data["data"]]
        assert "user1" in logins
        assert "user2" in logins

    async def test_get_user_by_id_success(
        self, async_test_client: AsyncClient, test_session, override_get_db_session
    ):
        """Тест успешного получения пользователя по ID."""
        # Arrange
        repo = UserRepository(test_session)
        user = UserModel(
            login="testuser",
            email="test@test.com",
            password_hash="testhash",
            role=UserRoleEnum.COMMON,
        )
        created_user = await repo.create_user(user)

        # Act
        response = await async_test_client.get(f"/api/v1/users/{created_user.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["login"] == "testuser"
        assert data["data"]["email"] == "test@test.com"
        assert data["data"]["role"] == "common"

    async def test_get_user_by_id_not_found(
        self, async_test_client: AsyncClient, override_get_db_session
    ):
        """Тест получения несуществующего пользователя."""
        # Act
        response = await async_test_client.get("/api/v1/users/999")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == 404
        assert "not found" in data["message"].lower()

    async def test_get_user_profile_success(
        self, async_test_client: AsyncClient, test_session, override_get_db_session
    ):
        """Тест успешного получения профиля пользователя."""
        # Arrange
        repo = UserRepository(test_session)

        user = UserModel(
            login="testuser", email="test@test.com", password_hash="testhash"
        )
        created_user = await repo.create_user(user)

        profile = UserProfileModel(user_id=created_user.id, readed_chapters=42)
        await repo.create_user_profile(profile)

        # Act
        response = await async_test_client.get(
            f"/api/v1/users/{created_user.id}/profile"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["readed_chapters"] == 42

    async def test_get_user_profile_not_found(
        self, async_test_client: AsyncClient, override_get_db_session
    ):
        """Тест получения профиля несуществующего пользователя."""
        # Act
        response = await async_test_client.get("/api/v1/users/999/profile")

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert data["code"] == 404

    async def test_update_user_profile_success(
        self, async_test_client: AsyncClient, test_session, override_get_db_session
    ):
        """Тест успешного обновления профиля пользователя."""
        # Arrange
        repo = UserRepository(test_session)

        user = UserModel(
            login="testuser", email="test@test.com", password_hash="testhash"
        )
        created_user = await repo.create_user(user)

        profile = UserProfileModel(user_id=created_user.id, readed_chapters=10)
        await repo.create_user_profile(profile)

        update_data = {"readed_chapters": 25}

        # Act
        response = await async_test_client.patch(
            f"/api/v1/users/{created_user.id}/profile", json=update_data
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == 200
        assert data["data"]["readed_chapters"] == 25

    async def test_update_user_profile_not_found(
        self, async_test_client: AsyncClient, override_get_db_session
    ):
        """Тест обновления профиля несуществующего пользователя."""
        # Arrange
        update_data = {"readed_chapters": 25}

        # Act
        response = await async_test_client.patch(
            "/api/v1/users/999/profile", json=update_data
        )

        # Assert
        assert response.status_code == 404

    async def test_update_user_profile_partial_update(
        self, async_test_client: AsyncClient, test_session, override_get_db_session
    ):
        """Тест частичного обновления профиля (только некоторые поля)."""
        # Arrange
        repo = UserRepository(test_session)

        user = UserModel(
            login="testuser", email="test@test.com", password_hash="testhash"
        )
        created_user = await repo.create_user(user)

        profile = UserProfileModel(user_id=created_user.id, readed_chapters=15)
        await repo.create_user_profile(profile)

        # Обновляем только readed_chapters
        update_data = {"readed_chapters": 50}

        # Act
        response = await async_test_client.patch(
            f"/api/v1/users/{created_user.id}/profile", json=update_data
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["readed_chapters"] == 50

    async def test_api_response_format(
        self, async_test_client: AsyncClient, override_get_db_session
    ):
        """Тест формата ответа API."""
        # Act
        response = await async_test_client.get("/api/v1/users/")

        # Assert
        data = response.json()
        assert "code" in data
        assert "message" in data
        assert "data" in data
        assert isinstance(data["code"], int)
        assert isinstance(data["message"], str)

    async def test_invalid_user_id_format(
        self, async_test_client: AsyncClient, override_get_db_session
    ):
        """Тест с невалидным форматом ID пользователя."""
        # Act
        response = await async_test_client.get("/api/v1/users/invalid_id")

        # Assert
        assert response.status_code == 422  # Unprocessable Entity

    async def test_empty_profile_update(
        self, async_test_client: AsyncClient, test_session, override_get_db_session
    ):
        """Тест обновления профиля с пустыми данными."""
        # Arrange
        repo = UserRepository(test_session)

        user = UserModel(
            login="testuser", email="test@test.com", password_hash="testhash"
        )
        created_user = await repo.create_user(user)

        profile = UserProfileModel(user_id=created_user.id, readed_chapters=20)
        await repo.create_user_profile(profile)

        # Act - пустое обновление
        response = await async_test_client.patch(
            f"/api/v1/users/{created_user.id}/profile", json={}
        )

        # Assert - должно пройти без изменений
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["readed_chapters"] == 20  # Значение не изменилось

    async def test_multiple_users_different_roles(
        self, async_test_client: AsyncClient, test_session, override_get_db_session
    ):
        """Тест API с пользователями разных ролей."""
        # Arrange
        repo = UserRepository(test_session)

        admin = UserModel(
            login="admin",
            email="admin@test.com",
            password_hash="adminhash",
            role=UserRoleEnum.ADMIN,
        )
        manager = UserModel(
            login="manager",
            email="manager@test.com",
            password_hash="managerhash",
            role=UserRoleEnum.MANAGER,
        )

        await repo.create_user(admin)
        await repo.create_user(manager)

        # Act
        response = await async_test_client.get("/api/v1/users/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 2

        roles = [user["role"] for user in data["data"]]
        assert "admin" in roles
        assert "manager" in roles
