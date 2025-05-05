from fastapi import status
from app.models.book import Book

def test_initialize_books(client, mock_redis):
    mock_redis.scan_iter.return_value = [b"book:1"]
    mock_redis.get.return_value = '{"id":"1","title":"Test Book","price":19.99,"category":"Fiction"}'
    
    response = client.post("/api/v1/books/init")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Test Book"

def test_search_books(client, mock_redis):
    mock_redis.scan_iter.return_value = [b"book:1", b"book:2"]
    mock_redis.get.side_effect = [
        '{"id":"1","title":"Python Guide","category":"Programming"}',
        '{"id":"2","title":"Fiction Book","category":"Literature"}'
    ]
    
    response = client.get("/api/v1/books/search?q=python")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
    assert "Python" in response.json()[0]["title"]