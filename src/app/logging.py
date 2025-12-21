import logging
from app.config import get_settings


def configure_logging() -> None:
    """
    Configure application-wide logging.

    Should be called once at application startup.
    """
    settings = get_settings()

    logging.basicConfig(
        level=settings.log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a module-specific logger.
    """
    return logging.getLogger(name)
