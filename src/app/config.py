from functools import lru_cache
from pydantic import BaseModel, Field
import os


class Settings(BaseModel):
    """
    Central configuration for the application.

    Values are read from environment variables.
    Defaults are safe for local development.
    """

    app_name: str = Field(
        default="stockmcp", description="The name of the application."
    )
    environment: str = Field(
        default="dev", description="The deployment environment (dev, test, prod)."
    )
    log_level: str = Field(
        default="INFO", description="The logging level for the application."
    )
    market_timezone: str = Field(
        default="Asia/Kolkata", description="The timezone for market data."
    )
    enable_backtesting: bool = Field(
        default=True, description="Flag to enable or disable backtesting features."
    )


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
