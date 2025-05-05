from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import json
from app.models.book import Book
from app.utils.redis_utils import get_redis_client
from app.core.logging import api_logger

router = APIRouter()

@router.post("/init", response_model=List[Book], summary="Triggers initial book scraping")
async def initialize_books():
    from app.scrapping.scrape_books import scrape_all_books
    scrape_all_books()
    r = get_redis_client()
    books_data = []
    for key in r.scan_iter("book:*"):
        book_json = r.get(key)
        if book_json:
            try:
                books_data.append(Book(**json.loads(book_json)))
            except Exception as e:
                api_logger.error(f"Error parsing book data from Redis: {e}")
    return books_data

@router.get("/search", response_model=List[Book], summary="Search books by title or category")
async def search_books(q: Optional[str] = Query(None, description="Search term for title or category")):
    r = get_redis_client()
    matching_books = []
    for key in r.scan_iter("book:*"):
        book_json = r.get(key)
        if book_json:
            try:
                book = Book(**json.loads(book_json))
                if q is None or q.lower() in book.title.lower() or q.lower() in book.category.lower():
                    matching_books.append(book)
            except Exception as e:
                api_logger.error(f"Error parsing book data from Redis during search: {e}")
    return matching_books

@router.get("/", response_model=List[Book], summary="Retrieve books, optionally filter by category")
async def get_books(category: Optional[str] = Query(None, description="Filter books by category")):
    r = get_redis_client()
    books = []
    for key in r.scan_iter("book:*"):
        book_json = r.get(key)
        if book_json:
            try:
                book = Book(**json.loads(book_json))
                if category is None or book.category.lower() == category.lower():
                    books.append(book)
            except Exception as e:
                api_logger.error(f"Error parsing book data from Redis during retrieval: {e}")
    return books