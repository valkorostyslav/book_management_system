from typing import Any, Optional, Sequence

from fastapi import HTTPException
from sqlalchemy import Row, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import AsyncSession
from app.models.book import ALLOWED_GENRES


class BookRepository:
    @staticmethod
    async def create_book(db: AsyncSession, title: str, genre: str, published_year: int, author_id: int) -> Row[Any] | None:
        """
        Inserts a new book into the database and returns its data.
        """
        query = text("""
            INSERT INTO "book" (title, genre, published_year, author_id)
            VALUES (:title, :genre, :published_year, :author_id)
            RETURNING id, title, genre, published_year, author_id
        """)
        async with db.begin():
            result = await db.execute(
                query,
                {
                    "title": title,
                    "genre": genre,
                    "published_year": published_year,
                    "author_id": author_id,
                },
            )
        return result.fetchone()

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
        Retrieves books from the database with filtering, pagination, and sorting.
        """
        filters = []
        params = {}

        if title:
            filters.append("title ILIKE :title")
            params["title"] = f"%{title}%"

        if genre:
            filters.append("genre = :genre")
            params["genre"] = genre

        if author_id:
            filters.append("author_id = :author_id")
            params["author_id"] = author_id

        where_clause = " WHERE " + " AND ".join(filters) if filters else ""
        sort_clause = f"ORDER BY {sort_by} {sort_order}"

        offset = (page - 1) * page_size
        limit = page_size

        query = text(f"""
            SELECT id, title, genre, published_year, author_id 
            FROM book
            {where_clause}
            {sort_clause}
            LIMIT :limit OFFSET :offset
        """)

        params["limit"] = limit
        params["offset"] = offset

        result = await db.execute(query, params)
        return result.fetchall()

    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: int) -> Row[Any] | None:
        query = text("""
            SELECT id, title, genre, published_year, author_id 
            FROM "book" 
            WHERE id = :book_id
        """)
        result = await db.execute(query, {"book_id": book_id})
        return result.fetchone()

    @staticmethod
    async def update_book(
        db: AsyncSession,
        book_id: int,
        title: str,
        genre: str,
        published_year: int,
        author_id: int,
    ) -> Row[Any] | None:
        """
        Updates a book record in the database.
        """
        query = text("""
            UPDATE "book" 
            SET title = :title, genre = :genre, published_year = :published_year, author_id = :author_id
            WHERE id = :book_id
            RETURNING id, title, genre, published_year, author_id
        """)
        result = await db.execute(
            query,
            {
                "title": title,
                "genre": genre,
                "published_year": published_year,
                "author_id": author_id,
                "book_id": book_id,
            },
        )
        return result.fetchone()

    @staticmethod
    async def delete_book(db: AsyncSession, book_id: int) -> Any:
        """
        Deletes a book from the database.
        """
        query = text('DELETE FROM "book" WHERE id = :book_id')
        result = await db.execute(query, {"book_id": book_id})
        return result.rowcount  # type: ignore

    @staticmethod
    async def bulk_insert_books(db: AsyncSession, books_data: list[dict]) -> None:
        """
        Inserts multiple books into the database in bulk.
        """
        if not books_data:
            raise HTTPException(status_code=400, detail="No books to import")

        existing_authors = await db.execute(text("SELECT id FROM author"))
        existing_author_ids = {row[0] for row in existing_authors.fetchall()}

        query = text("""
            INSERT INTO book (title, genre, published_year, author_id)
            VALUES (:title, :genre, :published_year, :author_id)
        """)

        try:
            for book in books_data:
                if book["genre"] not in ALLOWED_GENRES:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid genre: {book['genre']}"
                    )

                if book["published_year"] < 1800:
                    raise HTTPException(
                        status_code=400, detail="published_year must be >= 1800"
                    )

                if book["author_id"] not in existing_author_ids:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Author ID {book['author_id']} does not exist",
                    )

                await db.execute(query, book)

            await db.commit()

        except Exception as e:
            await db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
