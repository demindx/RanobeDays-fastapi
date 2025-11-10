from fastapi import APIRouter

from src.core.schemas import GenericResponse
from src.users.dependencies import UserProfileServiceDep, UserServiceDep
from src.users.schemas import (
    UserProfileResponse,
    UserProfileUpdate,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users_handler(
    service: UserServiceDep,
) -> GenericResponse[list[UserResponse]]:
    """Get all users"""
    users = await service.get_all()

    data = [UserResponse.model_validate(user) for user in users]

    return GenericResponse[list[UserResponse]](data=data)


@router.get("/{id}")
async def get_user_handler(
    service: UserServiceDep, id: int
) -> GenericResponse[UserResponse]:
    """Get user by id"""
    user = await service.get_by_id(id)

    data = UserResponse.model_validate(user)

    return GenericResponse[UserResponse](data=data)


@router.get("/{id}/profile")
async def get_user_profile_handler(
    service: UserProfileServiceDep, id: int
) -> GenericResponse[UserProfileResponse]:
    """Get user profile"""
    profile = await service.get_by_id(id)

    data = UserProfileResponse.model_validate(profile)

    return GenericResponse[UserProfileResponse](data=data)


@router.patch("/{id}/profile")
async def update_user_profile_handler(
    service: UserProfileServiceDep, id: int, data: UserProfileUpdate
) -> GenericResponse[UserProfileResponse]:
    """Update user profile"""
    profile = await service.update(id, data)

    profile = UserProfileResponse.model_validate(profile)

    return GenericResponse[UserProfileResponse](data=profile)
