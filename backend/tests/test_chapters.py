def chapter_payload(novel_id, team_id, **overrides):
    payload = {
        "title": "Chapter 1",
        "number": 1,
        "content": "Hello world",
        "novel_id": novel_id,
        "team_id": team_id,
    }
    payload.update(overrides)
    return payload


async def _seed_novel(seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    language = await seed.language()
    country = await seed.country()
    novel = await seed.novel(team.id, language.id, country.id)
    return novel, team


async def test_list_chapters_empty(client):
    resp = await client.get("/api/v1/chapter/")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_create_chapter(client, seed):
    novel, team = await _seed_novel(seed)
    resp = await client.post(
        "/api/v1/chapter/", json=chapter_payload(novel.id, team.id)
    )
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["title"] == "Chapter 1"
    assert data["novel_id"] == novel.id


async def test_get_chapter_by_id(client, seed):
    novel, team = await _seed_novel(seed)
    chapter = await seed.chapter(novel.id, team.id, title="Seeded")

    resp = await client.get(f"/api/v1/chapter/{chapter.id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Seeded"


async def test_get_chapter_not_found(client):
    resp = await client.get("/api/v1/chapter/999999")
    assert resp.status_code == 404


async def test_update_chapter(client, seed):
    novel, team = await _seed_novel(seed)
    chapter = await seed.chapter(novel.id, team.id)

    resp = await client.patch(
        f"/api/v1/chapter/{chapter.id}", json={"title": "Updated"}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Updated"


async def test_delete_chapter(client, seed):
    novel, team = await _seed_novel(seed)
    chapter = await seed.chapter(novel.id, team.id)

    resp = await client.delete(f"/api/v1/chapter/{chapter.id}")
    assert resp.status_code == 200

    get_resp = await client.get(f"/api/v1/chapter/{chapter.id}")
    assert get_resp.status_code == 404


async def test_create_chapter_missing_novel(client, seed):
    user, _ = await seed.user()
    team = await seed.team(user.id)
    resp = await client.post(
        "/api/v1/chapter/",
        json={"title": "Chapter", "number": 1, "content": "x", "team_id": team.id},
    )
    assert resp.status_code == 422


async def test_create_chapter_invalid_number(client, seed):
    novel, team = await _seed_novel(seed)
    resp = await client.post(
        "/api/v1/chapter/", json=chapter_payload(novel.id, team.id, number="one")
    )
    assert resp.status_code == 422


async def test_chapter_response_shape(client, seed):
    novel, team = await _seed_novel(seed)
    chapter = await seed.chapter(novel.id, team.id)

    resp = await client.get(f"/api/v1/chapter/{chapter.id}")
    data = resp.json()["data"]
    assert data["novel_id"] == novel.id
    assert data["content"] == "Hello"
    assert data["is_published"] is False
    assert data["created_at"]
