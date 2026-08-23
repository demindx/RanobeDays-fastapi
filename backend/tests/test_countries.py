async def test_list_countries_empty(client):
    resp = await client.get("/api/v1/country/")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


async def test_create_country(client):
    resp = await client.post("/api/v1/country/", json={"name": "Russia"})
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Russia"


async def test_get_country_by_id(client, seed):
    country = await seed.country(name="Japan")
    resp = await client.get(f"/api/v1/country/{country.id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "Japan"


async def test_get_country_not_found(client):
    resp = await client.get("/api/v1/country/999999")
    assert resp.status_code == 404


async def test_update_country(client, seed):
    country = await seed.country()
    resp = await client.patch(
        f"/api/v1/country/{country.id}", json={"name": "USA"}
    )
    assert resp.status_code == 200
    assert resp.json()["data"]["name"] == "USA"


async def test_delete_country(client, seed):
    country = await seed.country()
    resp = await client.delete(f"/api/v1/country/{country.id}")
    assert resp.status_code == 200

    get_resp = await client.get(f"/api/v1/country/{country.id}")
    assert get_resp.status_code == 404
