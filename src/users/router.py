from fastapi import APIRouter

from src.core.schemas import GenericResponse
from src.users.dependencies import UserServiceDep
from src.users.schemas import UserProfileResponse, UserProfileUpdateRequest, UserResponse

router = APIRouter(prefix="/users")


@router.get("/")
async def get_users_handler(service: UserServiceDep) -> GenericResponse[list[UserResponse]]:
    """Get all users"""
    users = await service.get_all_users()

    return GenericResponse[list[UserResponse]](data=users)


@router.get("/{id}")
async def get_user_handler(service: UserServiceDep, id: int) -> GenericResponse[UserResponse]:
    """Get user by id"""
    user = await service.get_user(id)

    return GenericResponse[UserResponse](data=user)


@router.get("/{id}/profile")
async def get_user_profile_handler(service: UserServiceDep, id: int) -> GenericResponse[UserProfileResponse]:
    """Get user profile"""
    profile = await service.get_user_profile(id)

    return GenericResponse[UserProfileResponse](data=profile)


@router.patch("/{id}/profile")
async def update_user_profile_handler(
    service: UserServiceDep, id: int, data: UserProfileUpdateRequest
) -> GenericResponse[UserProfileResponse]:
    profile = await service.update_user_profile(id, data)

    return GenericResponse[UserProfileResponse](data=profile)
