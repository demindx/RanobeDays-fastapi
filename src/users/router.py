from fastapi import APIRouter

from src.dependencies import DbSession
from src.schemas import GenericResponse
from src.users.schemas import UserResponse
from src.users.selectors import get_users

router = APIRouter(prefix="/users")


@router.get("/")
async def get_users_handler(session: DbSession) -> GenericResponse[list[UserResponse]]:
    users = await get_users(session)

    data = [UserResponse.from_orm(user) for user in users]

    return GenericResponse[list[UserResponse]](data=data)
