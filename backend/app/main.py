from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.core.config import settings
from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handle application startup and shutdown events.
    """
    logger.info("Starting Enerlytics API...")

    yield

    logger.info("Shutting down Enerlytics API...")




app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan
)


app.include_router(router)