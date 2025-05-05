from pydantic import BaseModel, Field
from typing import Optional

class HNItem(BaseModel):
    title: str = Field(..., description="Title of the Hacker News story")
    score: int = Field(..., description="Score of the Hacker News story")
    url: Optional[str] = Field(None, description="URL of the Hacker News story")