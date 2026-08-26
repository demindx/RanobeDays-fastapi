from typing import Annotated

from fastapi import APIRouter, Cookie, Response

from src.auth.dependencies import AuthServiceDep, RefreshToken
from src.auth.schemas import Tokens
from src.config import config
from src.core.schemas import GenericResponse
from src.users.schemas import UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register_handler(
    service: AuthServiceDep, data: UserRegister
) -> GenericResponse[None]:
    """Register users"""
    await service.register(data)

    return GenericResponse[None](message="User was successfully created")


@router.post("/login")
async def login_handler(
    service: AuthServiceDep, data: UserLogin, response: Response
) -> GenericResponse[Tokens]:
    """Login users"""
    tokens = await service.login(data)

    response.set_cookie(
        "refresh_token",
        str(tokens.refresh_token),
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite="strict",
        path="/api/v1/auth",
    )

    return GenericResponse[Tokens](data=tokens)


@router.post("/refresh")
async def refresh_token_handler(
    service: AuthServiceDep,
    response: Response,
    refresh_token: RefreshToken,
) -> GenericResponse[Tokens]:
    """Refresh access tokens"""
    tokens = await service.refresh_token(refresh_token)

    response.set_cookie(
        "refresh_token",
        str(tokens.refresh_token),
        httponly=True,
        secure=config.COOKIE_SECURE,
        samesite="strict",
        path="/api/v1/auth",
    )

    return GenericResponse[Tokens](data=tokens)


@router.post("/logout")
async def logout_handler(
    service: AuthServiceDep,
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
) -> GenericResponse[None]:
    """Logout users"""
    if refresh_token:
        await service.logout(refresh_token)

    response.delete_cookie(
        "refresh_token",
        samesite="strict",
        httponly=True,
        secure=config.COOKIE_SECURE,
        path="/api/v1/auth",
    )

    return GenericResponse[None](message="Logout was successful")
