import asyncio
from datetime import UTC, datetime
from uuid import UUID, uuid4

import httpx
from sqlalchemy import update

from src.auth.models import RefreshSession
from src.main import app

REGISTER = "/api/v1/auth/register"
LOGIN = "/api/v1/auth/login"
REFRESH = "/api/v1/auth/refresh"


async def register(
    client, login="user1", email="user1@example.com", password="password123"
):
    return await client.post(
        REGISTER,
        json={
            "login": login,
            "email": email,
            "nickname": "Nick",
            "password1": password,
            "password2": password,
        },
    )


async def test_register_success(client):
    resp = await register(client)
    assert resp.status_code == 200
    assert resp.json()["message"] == "User was successfully created"


async def test_register_duplicate_login(client):
    await register(client)
    resp = await register(client)
    assert resp.status_code == 400


async def test_register_password_mismatch(client):
    resp = await client.post(
        REGISTER,
        json={
            "login": "user1",
            "email": "user1@example.com",
            "nickname": "Nick",
            "password1": "a",
            "password2": "b",
        },
    )
    assert resp.status_code == 422


async def test_login_success(client):
    await register(client)
    resp = await client.post(LOGIN, json={"login": "user1", "password": "password123"})
    assert resp.status_code == 200
    assert resp.json()["data"]["access_token"]


async def test_login_wrong_password(client):
    await register(client)
    resp = await client.post(LOGIN, json={"login": "user1", "password": "wrong"})
    assert resp.status_code == 401


async def test_login_unknown_user(client):
    resp = await client.post(LOGIN, json={"login": "nobody", "password": "x"})
    assert resp.status_code == 404


async def test_logout(client):
    resp = await client.post("/api/v1/auth/logout")
    assert resp.status_code == 200


async def test_refresh_without_cookie(client):
    resp = await client.post("/api/v1/auth/refresh")
    assert resp.status_code == 401


def _refresh_token_from(response) -> str:
    set_cookie = response.headers.get("set-cookie", "")
    return set_cookie.split("refresh_token=")[1].split(";")[0]


async def _login(client) -> httpx.Response:
    await register(client)
    return await client.post(LOGIN, json={"login": "user1", "password": "password123"})


async def _refresh_with_token(refresh_token: str) -> httpx.Response:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        return await client.post(
            REFRESH,
            headers={"Cookie": f"refresh_token={refresh_token}"},
        )


async def test_register_invalid_email(client):
    resp = await client.post(
        REGISTER,
        json={
            "login": "user1",
            "email": "not-an-email",
            "nickname": "Nick",
            "password1": "password123",
            "password2": "password123",
        },
    )
    assert resp.status_code == 422


async def test_register_missing_password(client):
    resp = await client.post(
        REGISTER,
        json={"login": "user1", "email": "user1@example.com", "nickname": "Nick"},
    )
    assert resp.status_code == 422


async def test_register_duplicate_email(client):
    await register(client, login="user1", email="dup@example.com")
    resp = await register(client, login="user2", email="dup@example.com")
    assert resp.status_code == 400


async def test_login_by_email(client):
    await register(client)
    resp = await client.post(
        LOGIN,
        json={"email": "user1@example.com", "password": "password123"},
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["access_token"]


async def test_login_missing_password(client):
    resp = await client.post(LOGIN, json={"login": "user1"})
    assert resp.status_code == 422


async def test_login_without_credentials(client):
    resp = await client.post(LOGIN, json={"password": "x"})
    assert resp.status_code == 404


async def test_refresh_with_valid_cookie(client):
    await register(client)
    login_resp = await client.post(
        LOGIN, json={"login": "user1", "password": "password123"}
    )
    refresh_token = _refresh_token_from(login_resp)

    resp = await client.post(
        "/api/v1/auth/refresh",
        headers={"Cookie": f"refresh_token={refresh_token}"},
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["access_token"]


async def test_logout_with_cookie(client):
    await register(client)
    login_resp = await client.post(
        LOGIN, json={"login": "user1", "password": "password123"}
    )
    refresh_token = _refresh_token_from(login_resp)

    resp = await client.post(
        "/api/v1/auth/logout", headers={"Cookie": f"refresh_token={refresh_token}"}
    )
    assert resp.status_code == 200


async def test_refresh_with_malformed_uuid_cookie_returns_401(client):
    resp = await _refresh_with_token("not-a-uuid")

    assert resp.status_code == 401
    assert resp.json()["message"] == "Invalid refresh token"


async def test_refresh_with_unknown_uuid_returns_401(client):
    resp = await _refresh_with_token(str(uuid4()))

    assert resp.status_code == 401
    assert resp.json()["message"] == "Invalid refresh token"


async def test_refresh_token_cannot_be_reused(client):
    login_resp = await _login(client)
    old_refresh_token = _refresh_token_from(login_resp)

    first_resp = await _refresh_with_token(old_refresh_token)
    reused_resp = await _refresh_with_token(old_refresh_token)

    assert first_resp.status_code == 200
    assert reused_resp.status_code == 401
    assert reused_resp.json()["message"] == "Invalid refresh token"


async def test_concurrent_refresh_consumes_token_once(client):
    login_resp = await _login(client)
    refresh_token = _refresh_token_from(login_resp)

    first_resp, second_resp = await asyncio.gather(
        _refresh_with_token(refresh_token),
        _refresh_with_token(refresh_token),
    )

    assert sorted((first_resp.status_code, second_resp.status_code)) == [200, 401]


async def test_expired_refresh_token_returns_401(client, db_session):
    login_resp = await _login(client)
    refresh_token = UUID(_refresh_token_from(login_resp))
    expired_at = int(datetime.now(UTC).timestamp()) - 1

    await db_session.execute(
        update(RefreshSession)
        .where(RefreshSession.refresh_token == refresh_token)
        .values(expires_in=expired_at)
    )
    await db_session.commit()

    resp = await _refresh_with_token(str(refresh_token))

    assert resp.status_code == 401
    assert resp.json()["message"] == "Invalid refresh token"


async def test_login_does_not_expose_refresh_token_in_json(client):
    resp = await _login(client)

    assert resp.status_code == 200
    assert "refresh_token" not in resp.json()["data"]


async def test_refresh_does_not_expose_refresh_token_in_json(client):
    login_resp = await _login(client)
    refresh_token = _refresh_token_from(login_resp)

    resp = await _refresh_with_token(refresh_token)

    assert resp.status_code == 200
    assert "refresh_token" not in resp.json()["data"]


async def test_auth_cookies_have_security_attributes(client):
    login_resp = await _login(client)
    refresh_token = _refresh_token_from(login_resp)
    refresh_resp = await _refresh_with_token(refresh_token)

    for resp in (login_resp, refresh_resp):
        set_cookie = resp.headers["set-cookie"].lower()
        assert "httponly" in set_cookie
        assert "samesite=strict" in set_cookie


async def test_refresh_rotates_cookie(client):
    login_resp = await _login(client)
    old_refresh_token = _refresh_token_from(login_resp)

    refresh_resp = await _refresh_with_token(old_refresh_token)
    new_refresh_token = _refresh_token_from(refresh_resp)

    assert refresh_resp.status_code == 200
    assert new_refresh_token != old_refresh_token
