def novel_payload(team_id, language_id, country_id, **overrides):
    payload = {
        "title": "Test Novel",
        "age_limit": 16,
        "team_id": team_id,
        "language_id": language_id,
        "country_id": country_id,
        "description": "Description",
        "publish_date": "2024-01-01T00:00:00Z",
        "type": "original",
    }
    payload.update(overrides)
    return payload


async def _seed_basics(seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    language = await seed.language()
    country = await seed.country()
    return team, language, country


async def test_list_novels_empty(client):
    resp = await client.get("/api/v1/novel/")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_create_novel(client, seed):
    team, language, country = await _seed_basics(seed)
    resp = await client.post(
        "/api/v1/novel/", json=novel_payload(team.id, language.id, country.id)
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Test Novel"


async def test_get_novel_by_id(client, seed):
    team, language, country = await _seed_basics(seed)
    novel = await seed.novel(team.id, language.id, country.id, title="Seed Novel")

    resp = await client.get(f"/api/v1/novel/{novel.id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Seed Novel"


async def test_list_novels(client, seed):
    team, language, country = await _seed_basics(seed)
    await seed.novel(team.id, language.id, country.id)
    await seed.novel(team.id, language.id, country.id, title="Second")

    resp = await client.get("/api/v1/novel/")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 2


async def test_get_novel_not_found(client):
    resp = await client.get("/api/v1/novel/999999")
    assert resp.status_code == 404


async def test_update_novel(client, seed):
    team, language, country = await _seed_basics(seed)
    novel = await seed.novel(team.id, language.id, country.id)

    resp = await client.patch(f"/api/v1/novel/{novel.id}", json={"title": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Updated"


async def test_delete_novel(client, seed):
    team, language, country = await _seed_basics(seed)
    novel = await seed.novel(team.id, language.id, country.id)

    resp = await client.delete(f"/api/v1/novel/{novel.id}")
    assert resp.status_code == 200

    get_resp = await client.get(f"/api/v1/novel/{novel.id}")
    assert get_resp.status_code == 404


async def test_create_novel_invalid_type(client, seed):
    team, language, country = await _seed_basics(seed)
    resp = await client.post(
        "/api/v1/novel/",
        json=novel_payload(team.id, language.id, country.id, type="unknown"),
    )
    assert resp.status_code == 422


async def test_create_novel_invalid_publish_date(client, seed):
    team, language, country = await _seed_basics(seed)
    resp = await client.post(
        "/api/v1/novel/",
        json=novel_payload(team.id, language.id, country.id, publish_date="not-a-date"),
    )
    assert resp.status_code == 422


async def test_create_novel_invalid_age_limit(client, seed):
    team, language, country = await _seed_basics(seed)
    resp = await client.post(
        "/api/v1/novel/",
        json=novel_payload(team.id, language.id, country.id, age_limit="sixteen"),
    )
    assert resp.status_code == 422


async def test_create_novel_unknown_team(client, seed):
    user, _ = await seed.user()
    language = await seed.language()
    country = await seed.country()
    resp = await client.post(
        "/api/v1/novel/", json=novel_payload(999999, language.id, country.id)
    )
    assert resp.status_code == 400


async def test_list_novels_pagination(client, seed):
    team, language, country = await _seed_basics(seed)
    for i in range(3):
        await seed.novel(team.id, language.id, country.id, title=f"Novel {i}")

    resp = await client.get("/api/v1/novel/?limit=2&offset=1")
    assert resp.status_code == 200
    body = resp.json()
    assert body["limit"] == 2
    assert body["offset"] == 1
    assert len(body["data"]) == 2


async def test_novel_response_shape(client, seed):
    team, language, country = await _seed_basics(seed)
    novel = await seed.novel(team.id, language.id, country.id)

    resp = await client.get(f"/api/v1/novel/{novel.id}")
    data = resp.json()["data"]
    assert data["title"] == "Test Novel"
    assert data["language"]["name"] == "Chinese"
    assert data["country"]["name"] == "Russian"
    assert data["categories"] == []
    assert data["slug"]
    assert data["cover_path"] == "default_cover.png"
    assert data["status"] == "continues"
    assert data["type"] == "original"


async def test_delete_novel_not_found_is_idempotent(client):
    resp = await client.delete("/api/v1/novel/999999")
    assert resp.status_code == 200


async def test_novels_wrong_method(client):
    resp = await client.put("/api/v1/novel/")
    assert resp.status_code == 405
