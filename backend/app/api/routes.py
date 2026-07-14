from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.logging import logger
from app.db.session import get_db

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

@router.get("/db-test", tags=["Health"])
def database_test(db: Session = Depends(get_db)):
    """
    Test the database connection.
    """
    version = db.execute(text("SELECT version();")).scalar()

    return {
        "status": "connected",
        "database": version,
    }