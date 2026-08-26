REGISTER = "/api/v1/auth/register"
LOGIN = "/api/v1/auth/login"


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
