from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.core.database import init_db
from src.core.exceptions import BaseException
from src.core.router import api_v1
from src.core.schemas import GenericResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1)


@app.exception_handler(BaseException)
async def base_exception_handler(request: Request, exc: BaseException):
    content = GenericResponse[str](
        code=exc.status_code, message=exc.message
    ).model_dump()
    return JSONResponse(status_code=exc.status_code, content=content)
