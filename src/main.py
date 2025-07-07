from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from src.api import api_v1
from src.database import DbSession, db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api_v1)


@app.get("/")
async def index(db: DbSession):
    return JSONResponse({"message": "Hello world!"})
