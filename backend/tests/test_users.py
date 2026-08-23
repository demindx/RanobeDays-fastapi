async def register_and_login(client, login="user1", email="user1@example.com", password="password123"):
    await client.post(
        "/api/v1/auth/register",
        json={
            "login": login,
            "email": email,
            "nickname": "Nick",
            "password1": password,
            "password2": password,
        },
    )
    resp = await client.post(
        "/api/v1/auth/login",
        json={"login": login, "password": password, "fingerprint": "fp"},
    )
    return resp.json()["data"]["access_token"]


async def test_list_users_empty(client):
    resp = await client.get("/api/v1/users/")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_list_users(client, seed):
    await seed.user()
    await seed.user(login="user2", email="user2@example.com")
    resp = await client.get("/api/v1/users/")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 2


async def test_get_user_by_id(client, seed):
    user, _ = await seed.user()
    resp = await client.get(f"/api/v1/users/{user.id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["email"] == "user1@example.com"


async def test_get_user_not_found(client):
    resp = await client.get("/api/v1/users/999999")
    assert resp.status_code == 404


async def test_get_me_requires_auth(client):
    resp = await client.get("/api/v1/users/me")
    assert resp.status_code == 401


async def test_get_me(client):
    token = await register_and_login(client)
    resp = await client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["email"] == "user1@example.com"
    assert data["user_profile"]["nickname"] == "Nick"


async def test_get_profile(client, seed):
    _, profile = await seed.user()
    resp = await client.get(f"/api/v1/users/{profile.id}/profile")
    assert resp.status_code == 200
    assert resp.json()["data"]["nickname"] == "User One"


async def test_patch_profile(client, seed):
    _, profile = await seed.user()
    resp = await client.patch(
        f"/api/v1/users/{profile.id}/profile", json={"nickname": "Renamed"}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["nickname"] == "Renamed"
