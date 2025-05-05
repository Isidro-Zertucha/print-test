from fastapi import APIRouter
from app.api.endpoints import books, headlines

api_router = APIRouter()
api_router.include_router(books.router, prefix="/books", tags=["books"])
api_router.include_router(headlines.router, prefix="/headlines", tags=["headlines"])