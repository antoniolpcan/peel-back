import uuid
import pytest

@pytest.fixture
async def second_user(client):
    unique_id = uuid.uuid4().hex[:6]
    payload = {
        "name": f"Target User {unique_id}",
        "username": f"target_{unique_id}",
        "email": f"target_{unique_id}@example.com",
        "password": "password123"
    }
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 201, f"Erro ao criar second_user: {response.json()}"
    return response.json()


async def test_follow_user_success(client, auth_headers, second_user):
    payload = {"following_id": second_user["id"]}
    response = await client.post("/api/v1/follows/", json=payload, headers=auth_headers)
    assert response.status_code == 201


async def test_unfollow_user_success(client, auth_headers, second_user):
    await client.post("/api/v1/follows/", json={"following_id": second_user["id"]}, headers=auth_headers)
    response = await client.delete(f"/api/v1/follows/{second_user['id']}", headers=auth_headers)
    assert response.status_code == 204


async def test_get_followers_and_following(client, auth_headers, second_user):
    await client.post("/api/v1/follows/", json={"following_id": second_user["id"]}, headers=auth_headers)
    followers_res = await client.get(f"/api/v1/follows/followers/{second_user['id']}")
    assert followers_res.status_code == 200
    assert len(followers_res.json()) == 1


async def test_get_user_follow_stats(client, auth_headers, second_user):
    await client.post("/api/v1/follows/", json={"following_id": second_user["id"]}, headers=auth_headers)
    stats_res = await client.get(f"/api/v1/follows/{second_user['id']}/stats")
    assert stats_res.status_code == 200
    assert stats_res.json()["followers_count"] == 1


async def test_follow_user_unauthorized(client, second_user):
    payload = {"following_id": second_user["id"]}
    response = await client.post("/api/v1/follows/", json=payload)
    assert response.status_code == 401