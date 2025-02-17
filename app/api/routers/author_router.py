from typing import Any, List, Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.engine.row import Row
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.author_schema import AuthorCreate, AuthorResponse
from app.services.author_service import AuthorService

router = APIRouter()


@router.get("/", response_model=List[AuthorResponse])
async def get_all_authors(db: AsyncSession = Depends(get_db)) -> Sequence[Row[Any]]:
    """
    Retrieves a list of all authors from the database.
    """
    return await AuthorService.get_all_authors(db)


@router.get("/{author_id}", response_model=AuthorResponse)
async def get_author(author_id: int,db: AsyncSession = Depends(get_db)) -> Row[Any]:
    """
    Retrieves a specific author by their ID from the database.
    """
    return await AuthorService.get_author_by_id(db, author_id)


@router.post("/", response_model=AuthorResponse, status_code=201)

async def create_author(author_data: AuthorCreate, db: AsyncSession = Depends(get_db)) -> Row[Any] | None:
    """
    Creates a new author in the database.
    """
    return await AuthorService.create_author(db, author_data.name, author_data.biography)


@router.put("/{author_id}", response_model=AuthorResponse)
async def update_author(author_id: int, author_data: AuthorCreate, db: AsyncSession = Depends(get_db)) -> Row[Any] | None:
    """
    Updates an existing author's details in the database.
    """
    return await AuthorService.update_author(db, author_id, author_data.name, author_data.biography)


@router.delete("/{author_id}", status_code=204)
async def delete_author(author_id: int, db: AsyncSession = Depends(get_db)) -> None:
    """
    Deletes an author by their ID from the database.
    """
    success = await AuthorService.delete_author(db, author_id)
    if not success:
        raise HTTPException(status_code=404, detail="Author is not found")
