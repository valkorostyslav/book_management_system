from typing import Any

from fastapi import APIRouter, Depends

from app.core.db import AsyncSession, get_db
from app.schemas.user_schema import UserCreateSchema, UserResponseSchema
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponseSchema, status_code=201)
async def register(user: UserCreateSchema, db: AsyncSession = Depends(get_db)) -> Any:
    """
    Handles user registration.
    """
    return await UserService.register_user(db, user)
