from pydantic import BaseModel, Field
from typing import Optional

class Book(BaseModel):
    id: str = Field(..., description="Unique identifier for the book")
    title: str = Field(..., description="Title of the book")
    price: float = Field(..., description="Price of the book in GBP")
    category: str = Field(..., description="Category of the book")
    image_url: Optional[str] = Field(None, description="URL of the book's cover image")