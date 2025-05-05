from fastapi import APIRouter
from typing import List
from app.models.hn_item import HNItem
from app.scrapping.scrape_hn import fetch_realtime_headlines

router = APIRouter()

@router.get("/", response_model=List[HNItem], summary="Fetch real-time Hacker News headlines")
async def get_headlines():
    headlines = fetch_realtime_headlines()
    return headlines