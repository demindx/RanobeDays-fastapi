async def test_list_languages_empty(client):
    resp = await client.get("/api/v1/lang/")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_create_language(client):
    resp = await client.post("/api/v1/lang/", json={"name": "Chinese"})
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Chinese"


async def test_get_language_by_id(client, seed):
    language = await seed.language(name="Korean")
    resp = await client.get(f"/api/v1/lang/{language.id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Korean"


async def test_get_language_not_found(client):
    resp = await client.get("/api/v1/lang/999999")
    assert resp.status_code == 404


async def test_update_language(client, seed):
    language = await seed.language()
    resp = await client.patch(f"/api/v1/lang/{language.id}", json={"name": "Japanese"})
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Japanese"


async def test_delete_language(client, seed):
    language = await seed.language()
    resp = await client.delete(f"/api/v1/lang/{language.id}")
    assert resp.status_code == 200

    get_resp = await client.get(f"/api/v1/lang/{language.id}")
    assert get_resp.status_code == 404
