import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.database import engine


@pytest.fixture(autouse=True)
async def reset_db_pool():
    """Descarta o pool de conexões do SQLAlchemy ao final de CADA teste."""
    yield
    await engine.dispose()


@pytest.fixture
async def client():
    """Cliente HTTP assíncrono para os testes."""
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture
def test_user_data():
    return {
        "name": "Test User",
        "username": "testuser",
        "email": "test@example.com",
        "password": "Secretpassw@rd123"
    }


@pytest.fixture
async def created_user(client, test_user_data):
    response = await client.post("/api/v1/users", json=test_user_data)
    if response.status_code == 201:
        return response.json()
    return test_user_data


@pytest.fixture
async def auth_headers(client, created_user, test_user_data):
    login_data = {
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = await client.post("/api/v1/auth", data=login_data)
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}