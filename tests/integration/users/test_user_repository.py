import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.users.models import UserModel, UserProfileModel, UserRoleEnum
from src.users.repository import UserRepository


@pytest.mark.integration
class TestUserRepository:
    @pytest.fixture
    def user_repository(self, test_session: AsyncSession):
        return UserRepository(test_session)

    @pytest.fixture
    def sample_user_data(self):
        return {
            "login": "testuser",
            "email": "test@example.com",
            "password_hash": "hashed_password_123",
            "role": UserRoleEnum.COMMON,
            "is_active": True,
        }

    async def test_create_user(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)

        created_user = await user_repository.create_user(user)

        assert created_user.id is not None
        assert created_user.login == sample_user_data["login"]
        assert created_user.email == sample_user_data["email"]
        assert created_user.role == UserRoleEnum.COMMON
        assert created_user.is_active is True
        assert created_user.created_at is not None
        assert created_user.updated_at is not None

    async def test_get_user_by_id(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)
        created_user = await user_repository.create_user(user)

        found_user = await user_repository.get_user(created_user.id)

        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.login == sample_user_data["login"]

    async def test_get_user_not_found(self, user_repository):
        found_user = await user_repository.get_user(999)

        assert found_user is None

    async def test_get_user_by_login(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)
        await user_repository.create_user(user)

        found_user = await user_repository.get_user_by_login(sample_user_data["login"])

        assert found_user is not None
        assert found_user.login == sample_user_data["login"]

    async def test_get_user_by_login_not_found(self, user_repository):
        found_user = await user_repository.get_user_by_login("nonexistent")

        assert found_user is None

    async def test_get_all_users(self, user_repository):
        users_data = [
            {"login": "user1", "email": "user1@test.com", "password_hash": "hash1"},
            {"login": "user2", "email": "user2@test.com", "password_hash": "hash2"},
            {"login": "user3", "email": "user3@test.com", "password_hash": "hash3"},
        ]

        for user_data in users_data:
            user = UserModel(**user_data)
            await user_repository.create_user(user)

        all_users = await user_repository.get_all_users()

        assert len(all_users) == 3
        logins = [user.login for user in all_users]
        assert "user1" in logins
        assert "user2" in logins
        assert "user3" in logins

    async def test_update_user(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)
        created_user = await user_repository.create_user(user)

        created_user.is_active = False
        created_user.role = UserRoleEnum.ADMIN

        updated_user = await user_repository.update_user(created_user)

        assert updated_user.is_active is False
        assert updated_user.role == UserRoleEnum.ADMIN
        assert updated_user.id == created_user.id

    async def test_delete_user(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)
        created_user = await user_repository.create_user(user)
        user_id = created_user.id

        await user_repository.delete_user(user_id)

        found_user = await user_repository.get_user(user_id)
        assert found_user is None

    async def test_create_user_profile(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)
        created_user = await user_repository.create_user(user)

        profile = UserProfileModel(user_id=created_user.id, readed_chapters=10)

        created_profile = await user_repository.create_user_profile(profile)

        assert created_profile.id is not None
        assert created_profile.user_id == created_user.id
        assert created_profile.readed_chapters == 10
        assert created_profile.created_at is not None

    async def test_get_user_profile(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)
        created_user = await user_repository.create_user(user)

        profile = UserProfileModel(user_id=created_user.id, readed_chapters=25)
        await user_repository.create_user_profile(profile)

        found_profile = await user_repository.get_user_profile(created_user.id)

        assert found_profile is not None
        assert found_profile.user_id == created_user.id
        assert found_profile.readed_chapters == 25

    async def test_get_user_profile_not_found(self, user_repository):
        found_profile = await user_repository.get_user_profile(999)

        assert found_profile is None

    async def test_update_user_profile(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)
        created_user = await user_repository.create_user(user)

        profile = UserProfileModel(user_id=created_user.id, readed_chapters=5)
        created_profile = await user_repository.create_user_profile(profile)

        created_profile.readed_chapters = 100

        updated_profile = await user_repository.update_user_profile(created_profile)

        assert updated_profile.readed_chapters == 100
        assert updated_profile.id == created_profile.id

    async def test_user_profile_cascade_delete(self, user_repository, sample_user_data):
        user = UserModel(**sample_user_data)
        created_user = await user_repository.create_user(user)

        profile = UserProfileModel(user_id=created_user.id, readed_chapters=15)
        await user_repository.create_user_profile(profile)

        await user_repository.delete_user(created_user.id)

        found_user = await user_repository.get_user(created_user.id)
        assert found_user is None

    async def test_unique_constraints(self, user_repository, sample_user_data):
        user1 = UserModel(**sample_user_data)
        await user_repository.create_user(user1)

        user2_data = sample_user_data.copy()
        user2_data["email"] = "different@email.com"
        user2 = UserModel(**user2_data)

        from sqlalchemy.exc import IntegrityError

        with pytest.raises(IntegrityError):
            await user_repository.create_user(user2)

    async def test_different_user_roles(self, user_repository):
        admin = UserModel(
            login="admin",
            email="admin@test.com",
            password_hash="hash",
            role=UserRoleEnum.ADMIN,
        )
        manager = UserModel(
            login="manager",
            email="manager@test.com",
            password_hash="hash",
            role=UserRoleEnum.MANAGER,
        )
        common = UserModel(
            login="common",
            email="common@test.com",
            password_hash="hash",
            role=UserRoleEnum.COMMON,
        )

        created_admin = await user_repository.create_user(admin)
        created_manager = await user_repository.create_user(manager)
        created_common = await user_repository.create_user(common)

        assert created_admin.role == UserRoleEnum.ADMIN
        assert created_manager.role == UserRoleEnum.MANAGER
        assert created_common.role == UserRoleEnum.COMMON
