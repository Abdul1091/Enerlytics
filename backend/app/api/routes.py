from fastapi import APIRouter

from app.core.logging import logger

router = APIRouter()

@router.get("/")
def root():
    logger.info("Root endpoint accessed.")
    return {
        "message": "Welcome to Enerlytics API"
    }

@router.get("/health")
def health_check():
    logger.info("Health check requested.")
    return {
        "status": "healthy"
    }