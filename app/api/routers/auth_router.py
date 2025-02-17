from fastapi import APIRouter, Depends, HTTPException

from app.core.db import AsyncSession, get_db
from app.schemas.auth_schemas import TokenResponseSchema
from app.schemas.user_schema import UserLoginSchema
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
)

router = APIRouter()


@router.post("/jwt/create", response_model=TokenResponseSchema)
async def login(
    form_data: UserLoginSchema, db: AsyncSession = Depends(get_db)
) -> dict[str, str]:
    """
    Authenticates user and generates access and refresh tokens.
    """
    user_db = await authenticate_user(form_data.email, form_data.password, db)
    if not user_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(user_db.id)
    refresh_token = create_refresh_token(user_db.id)
    return {"access_token": access_token, "refresh_token": refresh_token}
