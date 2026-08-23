async def test_list_categories_empty(client):
    resp = await client.get("/api/v1/category/")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_create_category(client):
    resp = await client.post(
        "/api/v1/category/", json={"name": "Fantasy", "type": "genre"}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Fantasy"
    assert resp.json()["data"]["type"] == "genre"


async def test_get_category_by_id(client, seed):
    category = await seed.category(name="Action")
    resp = await client.get(f"/api/v1/category/{category.id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Action"


async def test_get_category_not_found(client):
    resp = await client.get("/api/v1/category/999999")
    assert resp.status_code == 404


async def test_update_category(client, seed):
    category = await seed.category()
    resp = await client.patch(
        f"/api/v1/category/{category.id}", json={"name": "Sci-Fi"}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Sci-Fi"


async def test_delete_category(client, seed):
    category = await seed.category()
    resp = await client.delete(f"/api/v1/category/{category.id}")
    assert resp.status_code == 200

    get_resp = await client.get(f"/api/v1/category/{category.id}")
    assert get_resp.status_code == 404


async def test_create_category_invalid_type(client):
    resp = await client.post(
        "/api/v1/category/", json={"name": "X", "type": "unknown"}
    )
    assert resp.status_code == 422
