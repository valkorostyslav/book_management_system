from typing import Any, Sequence

from sqlalchemy import Row, text

from app.core.db import AsyncSession


class AuthorRepository:
    @staticmethod
    async def get_author_by_id(db: AsyncSession, author_id: int) -> Row[Any] | None:
        """
        Retrieves an author by ID from the database.
        """
        query = text("SELECT * FROM author WHERE id = :author_id")
        result = await db.execute(query, {"author_id": author_id})
        return result.fetchone()

    @staticmethod
    async def get_all_authors(db: AsyncSession) -> Sequence[Row[Any]]:
        """
        Retrieves all authors from the database.
        """
        query = text("SELECT * FROM author")
        result = await db.execute(query)
        return result.fetchall()

    @staticmethod
    async def get_author_by_name(db: AsyncSession, name: str) -> Row[Any] | None:
        """
        Retrieves an author by their name from the database.
        """
        query = text("SELECT * FROM author WHERE name = :name")
        result = await db.execute(query, {"name": name})
        return result.fetchone()

    @staticmethod
    async def create_author(db: AsyncSession, name: str, biography: str) -> Row[Any] | None:
        """
        Inserts a new author into the database.
        """
        query = text("""
            INSERT INTO author (name, biography) 
            VALUES (:name, :biography) 
            RETURNING id, name, biography
        """)
        result = await db.execute(query, {"name": name, "biography": biography})
        await db.commit()
        return result.fetchone()

    @staticmethod
    async def update_author(db: AsyncSession, author_id: int, name: str, biography: str) -> Row[Any] | None:
        """
        Updates an author's details in the database.
        """
        query = text("""
            UPDATE author
            SET name = :name, biography = :biography
            WHERE id = :author_id
            RETURNING id, name, biography
        """)
        result = await db.execute(query, {"name": name, "biography": biography, "author_id": author_id})
        await db.commit()
        return result.fetchone()

    @staticmethod
    async def delete_author(db: AsyncSession, author_id: int) -> Any:
        """
        Deletes an author from the database by ID.
        """
        query = text("DELETE FROM author WHERE id = :author_id")
        result = await db.execute(query, {"author_id": author_id})
        await db.commit()
        return result.rowcount > 0 # type: ignore