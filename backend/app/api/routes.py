from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "Welcome to Enerlytics API"
    }

@router.get("/health")
def health_check():
    return {
        "status": "healthy"
    }