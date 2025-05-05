import requests
from bs4 import BeautifulSoup
import redis
import json
import hashlib
import time
from typing import Dict, Any
from app.core.config import settings
from app.core.logging import book_scraper_logger
from app.utils.redis_utils import get_redis_client

def generate_book_id(url: str) -> str:
    """Generate consistent book ID from URL"""
    return hashlib.sha256(url.encode()).hexdigest()[:10]

def scrape_book_data(book_url: str) -> Dict[str, Any]:
    """Scrape individual book details from product page"""
    try:
        response = requests.get(book_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract book details
        title = soup.select_one('.product_main h1').text.strip()
        price = float(soup.select_one('.product_main .price_color').text.strip().lstrip('£'))
        category = soup.select_one('.breadcrumb > li:nth-child(3) > a').text.strip()
        image_url_relative = soup.select_one('.image_container img')['src']
        image_url = f"{settings.BOOKS_TO_SCRAPE_URL}{image_url_relative.lstrip('../')}"

        return {
            "title": title,
            "price": price,
            "category": category,
            "image_url": image_url
        }
    except requests.exceptions.RequestException as e:
        book_scraper_logger.error(f"Request error for {book_url}: {e}")
        return None
    except Exception as e:
        book_scraper_logger.error(f"Parsing error for {book_url}: {e}")
        return None

def scrape_books_from_page(page_url: str, r: redis.Redis, books_needed: int) -> int:
    """Scrape up to 'books_needed' books from a listing page"""
    scraped_count = 0
    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        for container in soup.select('.product_pod'):
            if scraped_count >= books_needed:
                break

            if link := container.select_one('h3 a'):
                book_url = f"{settings.BOOKS_TO_SCRAPE_URL}catalogue/{link['href'].lstrip('../')}"
                if book_data := scrape_book_data(book_url):
                    if book_data['price'] < 20:  # Price filter
                        book_id = generate_book_id(book_url)
                        # Store complete book data WITH ID
                        r.set(
                            f"book:{book_id}",
                            json.dumps({"id": book_id, **book_data})
                        )
                        book_scraper_logger.info(f"Stored: {book_data['title'][:30]}... (ID: {book_id})")
                        scraped_count += 1

        return scraped_count

    except Exception as e:
        book_scraper_logger.error(f"Page processing failed {page_url}: {e}")
        return 0

def scrape_all_books():
    """Main scraping function that paginates through the catalog with precise limit"""
    r = get_redis_client()
    total_scraped = 0
    page_num = 1

    while total_scraped < settings.BOOKS_TO_SCRAPE:
        books_needed_on_page = settings.BOOKS_TO_SCRAPE - total_scraped
        page_url = (
            f"{settings.BOOKS_TO_SCRAPE_URL}catalogue/page-{page_num}.html"
            if page_num > 1 else
            f"{settings.BOOKS_TO_SCRAPE_URL}catalogue/index.html"
        )

        scraped = scrape_books_from_page(page_url, r, books_needed_on_page)
        total_scraped += scraped
        book_scraper_logger.info(f"Page {page_num}: {scraped} books (Total: {total_scraped})")

        if total_scraped >= settings.BOOKS_TO_SCRAPE:
            book_scraper_logger.info(f"Reached target of {settings.BOOKS_TO_SCRAPE} books.")
            break

        page_num += 1
        time.sleep(1)  # Be polite

        if page_num > 50:  # Safety valve
            book_scraper_logger.warning("Max pages reached, stopping")
            break

    book_scraper_logger.info(f"Scraping complete. Total books: {total_scraped}")

if __name__ == "__main__":
    scrape_all_books()