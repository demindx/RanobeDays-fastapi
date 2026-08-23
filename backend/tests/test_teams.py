async def test_list_teams_empty(client):
    resp = await client.get("/api/v1/teams/")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_create_team(client, seed):
    user, _ = await seed.user()
    resp = await client.post(
        "/api/v1/teams/",
        json={"creator_id": user.id, "name": "Team", "type": "translators"},
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["name"] == "Team"
    assert data["type"] == "translators"


async def test_get_team_by_id(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id, name="Seeded")
    resp = await client.get(f"/api/v1/teams/{team.id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Seeded"


async def test_get_team_not_found(client):
    resp = await client.get("/api/v1/teams/999999")
    assert resp.status_code == 404


async def test_update_team(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    resp = await client.patch(f"/api/v1/teams/{team.id}", json={"name": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Updated"


async def test_delete_team(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    resp = await client.delete(f"/api/v1/teams/{team.id}")
    assert resp.status_code == 200

    get_resp = await client.get(f"/api/v1/teams/{team.id}")
    assert get_resp.status_code == 404


async def test_get_team_users(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    await seed.membership(team.id, user.id)

    resp = await client.get(f"/api/v1/teams/{team.id}/users")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1


async def test_add_user_to_team(client, seed):
    user, _ = await seed.user()
    user2, _ = await seed.user(login="user2", email="user2@example.com")
    team = await seed.team(user.id)

    resp = await client.patch(
        f"/api/v1/teams/{team.id}/users", json={"user_id": user2.id, "role": "manager"}
    )
    assert resp.status_code == 200


async def test_add_duplicate_user_to_team(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    await seed.membership(team.id, user.id)

    resp = await client.patch(
        f"/api/v1/teams/{team.id}/users", json={"user_id": user.id, "role": "manager"}
    )
    assert resp.status_code == 400


async def test_remove_user_from_team(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    await seed.membership(team.id, user.id)

    resp = await client.delete(f"/api/v1/teams/{team.id}/users/{user.id}")
    assert resp.status_code == 200


async def test_get_team_novels(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    language = await seed.language()
    country = await seed.country()
    await seed.novel(team.id, language.id, country.id, title="Novel A")

    resp = await client.get(f"/api/v1/teams/{team.id}/novels")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["title"] == "Novel A"


async def test_create_team_invalid_type(client, seed):
    user, _ = await seed.user()
    resp = await client.post(
        "/api/v1/teams/", json={"creator_id": user.id, "name": "Team", "type": "unknown"}
    )
    assert resp.status_code == 422


async def test_create_team_unknown_creator(client):
    resp = await client.post(
        "/api/v1/teams/", json={"creator_id": 999999, "name": "Team", "type": "translators"}
    )
    assert resp.status_code == 400


async def test_get_team_users_empty(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)

    resp = await client.get(f"/api/v1/teams/{team.id}/users")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_get_team_novels_empty(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)

    resp = await client.get(f"/api/v1/teams/{team.id}/novels")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_team_users_response_shape(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    await seed.membership(team.id, user.id)

    resp = await client.get(f"/api/v1/teams/{team.id}/users")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert len(data) == 1
    assert data[0]["role"] == "manager"
    assert data[0]["user"]["email"] == "user1@example.com"
