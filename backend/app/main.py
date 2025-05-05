import asyncio
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from app.api import routes as api_router  # Import the combined router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

from app.scrapping.scrape_books import scrape_all_books
from app.scrapping.scrape_hn import fetch_realtime_headlines

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run initial scrapers (non-blocking)
    async def run_scrapers():
        try:
            scrape_all_books()  # Your existing book scraper
            # Pre-load HN data (optional)
            fetch_realtime_headlines()
        except Exception as e:
            app.state.logger.error(f"Scraper init failed: {e}")
    
    asyncio.create_task(run_scrapers())
    yield
    # Cleanup if needed


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# CORS middleware (adjust as needed for your frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include the API router
app.include_router(api_router.api_router, prefix=settings.API_V1_STR, tags=["API"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)