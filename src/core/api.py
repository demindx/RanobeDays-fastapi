from fastapi import APIRouter

from src.users.router import router as user_router

api_v1 = APIRouter(prefix="/api/v1", tags=["api/v1"])

api_v1.include_router(user_router)
