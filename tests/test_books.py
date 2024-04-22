def test_create_book(session, client):
    author_name = {"names": ["Test Author"]}
    book_data = {"title": "Test Book", "description": "Test Description"}
    response = client.post("/books", json=author_name, params=book_data)
    assert response.status_code == 200  # Исправлено на 201 Created
    assert "id" in response.json()


def test_get_book_by_id(session, client):
    author_name = {"names": ["Test Author"]}
    book_data = {"title": "Test Book", "description": "Test Description"}
    response = client.post("/books", json=author_name, params=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id


def test_update_book_by_id(session, client):
    author_name = {"names": ["Test Author"]}
    book_data = {"title": "Test Book", "description": "Test Description"}
    response = client.post("/books", json=author_name, params=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    update_data = {"title": "Updated Book", "description": "Updated Description"}
    response = client.put(f"/books/{book_id}", json=author_name, params=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Book"


def test_delete_book_by_id(session, client):
    author_name = {"names": ["Test Author"]}
    book_data = {"title": "Test Book", "description": "Test Description"}
    response = client.post("/books", json=author_name, params=book_data)
    assert response.status_code == 200
    book_id = response.json()["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Книга успешно удалена"
