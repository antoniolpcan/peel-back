
async def test_login_success(client, created_user, test_user_data):
    login_payload = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = await client.post("/api/v1/auth", data=login_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_invalid_credentials(client):
    login_payload = {
        "username": "wrong@example.com",
        "password": "wrongpassword"
    }
    response = await client.post("/api/v1/auth", data=login_payload)
    assert response.status_code in [400, 401, 422]