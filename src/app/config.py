from functools import lru_cache
from pydantic import BaseModel
import os


class Settings(BaseModel):
    """
    Central configuration for the application.

    Values are read from environment variables.
    Defaults are safe for local development.
    """

    app_name: str = "stockmcp"
    environment: str = "dev"  # dev | test | prod
    log_level: str = "INFO"

    # Market data
    market_timezone: str = "Asia/Kolkata"

    # Feature flags (future use)
    enable_backtesting: bool = True


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.

    Ensures settings are created once per process
    and reused everywhere.
    """
    return Settings(
        environment=os.getenv("ENVIRONMENT", "dev"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )
