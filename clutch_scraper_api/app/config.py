from pydantic import BaseSettings, AnyHttpUrl
from typing import List, Optional

class Settings(BaseSettings):
    headless: bool = True
    use_agent: bool = True
    user_agents: List[str] = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/112.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/16.4 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edg/112.0.0.0 Safari/537.36",
    ]
    proxies: List[Optional[str]] = [None]

    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"

    allow_origins: List[AnyHttpUrl] = ["*"]
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]

    class Config:
        env_file = ".env"

settings = Settings()
