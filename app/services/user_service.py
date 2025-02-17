from typing import Any
from fastapi import HTTPException

from app.core.db import AsyncSession
from app.core.security import hash_password
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreateSchema


class UserService:
    @staticmethod
    async def register_user(db: AsyncSession, user_data: UserCreateSchema) -> Any:
        """
        Registers a new user by checking for duplicates, hashing the password, and saving the user to the database.
        """
        existing_user =  await UserRepository.get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_pw = hash_password(user_data.password)
        user_dict = user_data.dict()
        user_dict["hashed_password"] = hashed_pw
        del user_dict["password"]

        user = await UserRepository.create_user(db, user_dict)
        if not user:
            raise HTTPException(status_code=400, detail="User creation failed")

        return user
