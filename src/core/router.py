from fastapi import APIRouter

from src.auth.router import router as auth_router
from src.category.router import router as category_router
from src.chapter.router import router as chapter_router
from src.language.router import router as language_router
from src.novel.router import router as novel_router
from src.teams.router import router as team_router
from src.users.router import router as user_router

api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(user_router)
api_v1.include_router(auth_router)
api_v1.include_router(team_router)
api_v1.include_router(novel_router)
api_v1.include_router(chapter_router)
api_v1.include_router(category_router)
api_v1.include_router(language_router)
