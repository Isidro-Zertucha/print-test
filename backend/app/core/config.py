import os

class Settings:
    PROJECT_NAME: str = "FastAPI Books and News"
    API_V1_STR: str = "/api/v1"
    REDIS_HOST: str = os.getenv("REDIS_HOST", "redis")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    BOOKS_TO_SCRAPE: int = 100
    BOOKS_TO_SCRAPE_URL: str = "https://books.toscrape.com/"
    HACKER_NEWS_URL: str = "https://news.ycombinator.com/"
    HN_PAGES_TO_SCRAPE: int = 5
    SCRAPE_RETRY_COUNT: int = 3
    SCRAPE_RETRY_DELAY: int = 2  # seconds

settings = Settings()