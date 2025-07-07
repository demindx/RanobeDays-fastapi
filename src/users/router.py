from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users")


@router.get("/")
async def index():
    return JSONResponse({"message": "Hello from users!"})
