
async def test_create_post(client, auth_headers):
    payload = {
        "title": "Meu Primeiro Post",
        "body": "Conteúdo do post de teste",
        "color_id": None  
    }
    response = await client.post("/api/v1/posts", json=payload, headers=auth_headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert "id" in data


async def test_search_posts_with_pagination(client):
    response = await client.get("/api/v1/posts?skip=0&limit=10&sort_order=desc")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_add_comment_to_post(client, auth_headers):
    post_res = await client.post(
        "/api/v1/posts",
        json={"title": "Post para Comentar", "body": "Texto..."},
        headers=auth_headers
    )
    assert post_res.status_code == 201
    post_id = post_res.json()["id"]

    comment_res = await client.post(
        f"/api/v1/posts/{post_id}/comments?content=Excelente%20post!",
        headers=auth_headers
    )
    
    assert comment_res.status_code == 201
    assert comment_res.json()["content"] == "Excelente post!"