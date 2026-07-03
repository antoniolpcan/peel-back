from fastapi.testclient import TestClient
from app.core.config import settings

def test_create_post(client: TestClient):
    response = client.post(f"{settings.API_V1_STR}/posts/", json={"title": "Meu Post", "body": "Conteúdo"})
    assert response.status_code == 201