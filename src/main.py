from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import api_v1
from src.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1)
