import uuid
from typing import Annotated

from fastapi import APIRouter, Body, Cookie, Response

from src.auth.dependencies import AuthServiceDep, RefreshToken
from src.auth.schemas import RefreshSessionUpdate, Tokens
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

    response.set_cookie("refresh_token", str(tokens.refresh_token))

    return GenericResponse[Tokens](data=tokens)


@router.post("/refresh")
async def refresh_token_handler(
    service: AuthServiceDep,
    response: Response,
    refresh_token: RefreshToken,
    fingerprint: Annotated[str, Body()],
) -> GenericResponse[Tokens]:
    """Refresh access tokens"""
    tokens = await service.refresh_token(
        RefreshSessionUpdate(refresh_token=refresh_token, fingerprint=fingerprint)
    )

    response.set_cookie("refresh_token", str(tokens.refresh_token))

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

    response.delete_cookie("refresh_token")

    return GenericResponse[None](message="Logout was successful")
