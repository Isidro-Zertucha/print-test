from fastapi import status
from unittest.mock import patch
from app.models.hn_item import HNItem

def test_get_headlines_success(client):
    mock_data = [{
        "title": "Test Story",
        "url": "http://example.com",
        "score": 100,
        "page": 1
    }]
    
    with patch('app.scrapping.scrape_hn.fetch_realtime_headlines', return_value=mock_data):
        response = client.get("/api/v1/headlines/")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]["title"] == "Test Story"

def test_get_headlines_failure(client):
    with patch('app.scrapping.scrape_hn.fetch_realtime_headlines', side_effect=Exception("Scraping failed")):
        response = client.get("/api/v1/headlines/")
        
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert "Scraping failed" in response.json()["detail"]