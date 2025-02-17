from typing import Any, Sequence
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.author_repo import AuthorRepository


class AuthorService:
    @staticmethod
    async def get_author_by_id(db: AsyncSession, author_id: int) -> Row[Any]:
        """
        Fetches an author by ID from the repository.
        """
        author = await AuthorRepository.get_author_by_id(db, author_id)
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author was not found.")
        return author

    @staticmethod
    async def get_all_authors(db: AsyncSession) -> Sequence[Row[Any]]:
        """
        Fetches all authors from the repository.
        """
        return await AuthorRepository.get_all_authors(db)

    @staticmethod
    async def create_author(db: AsyncSession, name: str, biography: str) -> Row[Any] | None:
        """
        Creates a new author.
        """
        existing_author = await AuthorRepository.get_author_by_name(db, name)
        if existing_author:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Author with this name already exists.")
        return await AuthorRepository.create_author(db, name, biography)

    @staticmethod
    async def update_author(db: AsyncSession, author_id: int, name: str, biography: str) -> Row[Any] | None:
        """
        Updates an author's information.
        """
        author = await AuthorRepository.get_author_by_id(db, author_id)
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author was not found.")
        return await AuthorRepository.update_author(db, author_id, name, biography)

    @staticmethod
    async def delete_author(db: AsyncSession, author_id: int) -> Any:
        """
        Deletes an author from the repository by their ID.
        """
        author = await AuthorRepository.get_author_by_id(db, author_id)
        if not author:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author was not found.")
        return await AuthorRepository.delete_author(db, author_id)