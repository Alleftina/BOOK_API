from starlette.testclient import TestClient
from loguru import logger


def test_create_author(client: TestClient):
    author_data = {"name": "Test Author"}
    response = client.post("/authors", params=author_data)
    assert response.status_code == 200
    assert response.json()["name"] == author_data["name"]


def test_get_authors(client: TestClient):
    response = client.get("/authors")
    logger.info(response.json())
    assert response.status_code == 200
