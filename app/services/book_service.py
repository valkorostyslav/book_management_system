import csv
import json
from io import StringIO
from typing import Any, Optional, Sequence

from fastapi import HTTPException, UploadFile
from sqlalchemy import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSession
from app.repositories.book_repo import BookRepository


class BookService:
    @staticmethod
    async def create_book(db, title: str, genre: str, published_year: int, author_id: int) -> Row[Any] | None:
        """
        Creates a new book record in the repository.
        """
        book_data = await BookRepository.create_book(
            db, title, genre, published_year, author_id
        )
        return book_data

    @staticmethod
    async def get_books(
        db: AsyncSession,
        title: Optional[str] = None,
        genre: Optional[str] = None,
        author_id: Optional[int] = None,
        page: int = 1,
        page_size: int = 10,
        sort_by: str = "title",
        sort_order: str = "asc",
    ) -> Sequence[Row[Any]]:
        """
        Retrieves books with optional filtering, pagination, and sorting.
        """
        return await BookRepository.get_books(
            db, title, genre, author_id, page, page_size, sort_by, sort_order
        )

    @staticmethod
    async def get_book_by_id(db, book_id: int) -> Row[Any] | None:
        """
        Retrieves a book by its ID from the repository.
        """
        return await BookRepository.get_book_by_id(db, book_id)

    @staticmethod
    async def update_book(db, book_id: int, title: str, genre: str, published_year: int, author_id: int) -> Row[Any] | None:
        """
        Updates an existing book in the repository.
        """
        return await BookRepository.update_book(
            db, book_id, title, genre, published_year, author_id
        )

    @staticmethod
    async def delete_book(db, book_id: int) -> Any:
        """
        Deletes a book by its ID from the repository.
        """
        return await BookRepository.delete_book(db, book_id)

    @staticmethod
    async def import_books_from_json(file: UploadFile) -> Any:
        """
        Imports books from a JSON file.
        """
        content = await file.read()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")

    @staticmethod
    async def import_books_from_csv(file: UploadFile) -> list[dict[str | Any, str | Any]]:
        """
        Imports books from a CSV file.
        """
        content = await file.read()
        try:
            csv_reader = csv.DictReader(StringIO(content.decode("utf-8")))
            return [row for row in csv_reader]
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error parsing CSV file: {e}")
