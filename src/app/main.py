from fastapi import FastAPI

from app.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

app = FastAPI()


@app.get("/")
def health():
    logger.info("Health check called")
    return {"status": "ok"}
