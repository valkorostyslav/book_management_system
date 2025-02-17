from datetime import datetime, timedelta
from typing import Any

import bcrypt
from jose import jwt
from sqlalchemy import Row

from app.core.config import ALGORITHM, SECRET_KEY
from app.core.db import AsyncSession
from app.repositories.user_repo import UserRepository


async def authenticate_user(
    email: str, password: str, db: AsyncSession
) -> Row[Any] | None:
    """
    Verifies user credentials against the database.
    """
    user = await UserRepository.get_user_by_email(db, email)
    if user and bcrypt.checkpw(
        password.encode("utf-8"), user.hashed_password.encode("utf-8")
    ):
        return user
    return None


def create_access_token(user_id: int) -> str:
    """
    Generates an access token that expires in 15 minutes.
    """
    access_token_expires = timedelta(minutes=15)
    access_token = jwt.encode(
        {"sub": str(user_id), "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return access_token


def create_refresh_token(user_id: int) -> str:
    """
    Generates a refresh token that expires in 7 days.
    """
    refresh_token_expires = timedelta(days=7)
    refresh_token = jwt.encode(
        {"sub": user_id, "exp": datetime.utcnow() + refresh_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return refresh_token
