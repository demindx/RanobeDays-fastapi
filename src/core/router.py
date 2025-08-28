from fastapi import APIRouter

from src.auth.router import router as auth_router
from src.teams.router import router as team_router
from src.users.router import router as user_router

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(user_router)
api_v1.include_router(auth_router)
api_v1.include_router(team_router)
