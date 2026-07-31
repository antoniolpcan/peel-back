import uuid

async def test_create_user(client):
    random_email = f"user_{uuid.uuid4().hex[:6]}@example.com"
    payload = {
        "name": "Novo Usuario",
        "email": random_email,
        "password": "password123",
        "username": f"user_{uuid.uuid4().hex[:6]}"
    }
    response = await client.post("/api/v1/users", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data


async def test_update_current_user_authenticated(client, auth_headers):
    payload = {"name": "Nome Atualizado"}

    response = await client.patch("/api/v1/users/me", json=payload, headers=auth_headers)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Nome Atualizado"


async def test_update_current_user_unauthorized(client):

    response = await client.patch("/api/v1/users/me", json={"name": "Tentativa Invalida"})
    assert response.status_code == 401