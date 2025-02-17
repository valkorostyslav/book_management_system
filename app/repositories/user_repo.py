from typing import Any

from sqlalchemy import Row, text
from sqlalchemy.exc import IntegrityError

from app.core.db import AsyncSession


class UserRepository:
    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Row[Any] | None:
        """
        Retrieves a user from the database by their email address.
        """
        query = text(
            "SELECT id, username, email, first_name, last_name, hashed_password "
            'FROM "user_data" WHERE email = :email'
        )
        result = await db.execute(query, {"email": email})
        return result.fetchone()

    @staticmethod
    async def create_user(db: AsyncSession, user_data: dict) -> Any | None:
        """
        Creates a new user in the database and returns the created user's details.
        """
        query = text("""
        INSERT INTO user_data (username, email, first_name, last_name, hashed_password)
        VALUES (:username, :email, :first_name, :last_name, :hashed_password)
        RETURNING id, username, email, first_name, last_name
        """)
        try:
            result = await db.execute(query, params=user_data)
            await db.commit()
            return result.fetchone()
        except IntegrityError:
            await db.rollback()
            return None
