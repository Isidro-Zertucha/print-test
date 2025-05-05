import pytest
from bs4 import BeautifulSoup
from app.scrapping.scrape_books import scrape_book_data, scrape_books_from_page
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_book_page():
    return """
    <html>
        <div class="product_main">
            <h1>Test Book</h1>
            <p class="price_color">£19.99</p>
        </div>
        <ul class="breadcrumb">
            <li><a>Home</a></li>
            <li><a>Books</a></li>
            <li><a>Fiction</a></li>
        </ul>
        <div class="image_container">
            <img src="../../media/test.jpg"/>
        </div>
    </html>
    """

def test_scrape_book_data_success(mock_book_page):
    with patch('requests.get') as mock_get:
        mock_get.return_value.content = mock_book_page
        result = scrape_book_data("http://test.com")
        assert result["title"] == "Test Book"
        assert result["price"] == 19.99
        assert result["category"] == "Fiction"
        assert "test.jpg" in result["image_url"]

def test_scrape_books_from_page(mock_redis, mock_book_page):
    with patch('requests.get') as mock_get:
        mock_get.return_value.content = f"""
        <html>
            <div class="product_pod">
                <h3><a href="book1.html">Book 1</a></h3>
            </div>
            <div class="product_pod">
                <h3><a href="book2.html">Book 2</a></h3>
            </div>
        </html>
        """
        
        # Mock individual book requests
        with patch('app.scrapping.scrape_books.scrape_book_data') as mock_scrape:
            mock_scrape.return_value = {
                "title": "Test Book",
                "price": 15.99,
                "category": "Fiction",
                "image_url": "http://test.com/image.jpg"
            }
            
            count = scrape_books_from_page("http://test.com", mock_redis)
            assert count == 2
            assert mock_redis.set.call_count == 2