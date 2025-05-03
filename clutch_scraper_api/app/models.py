from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ScrapeRequest(BaseModel):
    base_url: HttpUrl
    total_pages: int = 3

class ScrapedCompany(BaseModel):
    sno: int
    name: str
    website: Optional[HttpUrl]
    location: Optional[str]

class ScrapeResponse(BaseModel):
    message: str
    data: List[ScrapedCompany]
