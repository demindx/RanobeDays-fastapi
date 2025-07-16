from fastapi import APIRouter

from src.core.schemas import GenericResponse
from src.users.dependencies import UserServiceDep
from src.users.schemas import (
    UserProfileResponse,
    UserProfileUpdateRequest,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users_handler(
    service: UserServiceDep,
) -> GenericResponse[list[UserResponse]]:
    """Get all users"""
    users = await service.get_all_users()

    data = [UserResponse.model_validate(user) for user in users]

    return GenericResponse[list[UserResponse]](data=data)


@router.get("/{id}")
async def get_user_handler(
    service: UserServiceDep, id: int
) -> GenericResponse[UserResponse]:
    """Get user by id"""
    user = await service.get_user(id)

    data = UserResponse.model_validate(user)

    return GenericResponse[UserResponse](data=data)


@router.get("/{id}/profile")
async def get_user_profile_handler(
    service: UserServiceDep, id: int
) -> GenericResponse[UserProfileResponse]:
    """Get user profile"""
    profile = await service.get_user_profile(id)

    data = UserProfileResponse.model_validate(profile)

    return GenericResponse[UserProfileResponse](data=data)


@router.patch("/{id}/profile")
async def update_user_profile_handler(
    service: UserServiceDep, id: int, data: UserProfileUpdateRequest
) -> GenericResponse[UserProfileResponse]:
    """Update user profile"""
    profile = await service.update_user_profile(id, data)

    profile = UserProfileResponse.model_validate(profile)

    return GenericResponse[UserProfileResponse](data=profile)
