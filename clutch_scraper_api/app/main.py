from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .config import settings
from .models import ScrapeRequest, ScrapeResponse
from .scraper import run_scraper

app = FastAPI(title="Clutch Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

@app.post("/scrape", response_model=ScrapeResponse)
async def scrape(request: ScrapeRequest):
    df, message = await run_scraper(request.base_url, request.total_pages)
    return ScrapeResponse(
        message=message,
        data=[
            {
                "sno": int(row["sno"]),
                "name": row["name"],
                "website": row["website"],
                "location": row["location"]
            }
            for _, row in df.iterrows()
        ]
    )

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=True
    )
