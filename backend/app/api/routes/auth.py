from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.api.schemas.auth import (
    LoginRequest,
    TokenResponse,
)
from app.core.config import settings
from app.core.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    credentials: LoginRequest,
):
    if (
        credentials.username != settings.ADMIN_USERNAME
        or not verify_password(
            credentials.password,
            settings.ADMIN_PASSWORD_HASH,
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials.",
        )

    token = create_access_token(
        credentials.username,
        settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    return TokenResponse(
        access_token=token,
        token_type="bearer",
    )