from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.core.db import AsyncSession, get_db
from app.repositories.book_repo import BookRepository
from app.schemas.book_schemas import BookCreateAndUpdateSchema, BookResponseSchema
from app.services.book_service import BookService

router = APIRouter()


@router.post("/", response_model=BookResponseSchema)
async def create_book(book: BookCreateAndUpdateSchema, db: AsyncSession = Depends(get_db)) -> BookResponseSchema:
    """
    Creates a new book in the database.
    """
    book_data = await BookService.create_book(
        db, book.title, book.genre, book.published_year, book.author_id
    )
    if not book_data:
        raise HTTPException(status_code=400, detail="Error creating book")
    return BookResponseSchema(
        id=book_data[0],
        title=book_data[1],
        genre=book_data[2],
        published_year=book_data[3],
        author_id=book_data[4],
    )


@router.get("/", response_model=List[BookResponseSchema])
async def get_books(
    title: str = Query(None),
    genre: str = Query(None),
    author_id: int = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    sort_by: str = Query("title", pattern="^(title|published_year|author_id)$"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    db: AsyncSession = Depends(get_db),
    ) -> List[BookResponseSchema]:
    """
    Retrieves a list of books with optional filters, pagination, and sorting.
    """
    books = await BookService.get_books(
        db, title, genre, author_id, page, page_size, sort_by, sort_order
    )
    return [
        BookResponseSchema(
            id=book[0],
            title=book[1],
            genre=book[2],
            published_year=book[3],
            author_id=book[4],
        )
        for book in books
    ]


@router.get("/{book_id}", response_model=BookResponseSchema)
async def get_book_by_id(book_id: int,db: AsyncSession = Depends(get_db)) -> BookResponseSchema:
    """
    Retrieves a book by its ID.
    """
    book_data = await BookService.get_book_by_id(db, book_id)
    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponseSchema(
        id=book_data[0],
        title=book_data[1],
        genre=book_data[2],
        published_year=book_data[3],
        author_id=book_data[4],
    )


@router.put("/{book_id}", response_model=BookResponseSchema)
async def update_book(
    book_id: int, 
    book: BookCreateAndUpdateSchema, 
    db: AsyncSession = Depends(get_db)
    )-> BookResponseSchema:
    """
    Updates an existing book by its ID.
    """
    book_data = await BookService.update_book(
        db, book_id, book.title, book.genre, book.published_year, book.author_id
    )
    if not book_data:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponseSchema(
        id=book_data[0],
        title=book_data[1],
        genre=book_data[2],
        published_year=book_data[3],
        author_id=book_data[4],
    )


@router.delete("/{book_id}", status_code=200)
async def delete_book(book_id: int,db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """
    Deletes a book by its ID.
    """
    row_count = await BookService.delete_book(db, book_id)
    if row_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}


@router.post("/import", status_code=201)
async def import_books(file: UploadFile = File(...),db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """
    Imports books from a JSON or CSV file.
    """
    if file.content_type == "application/json":
        books = await BookService.import_books_from_json(file)
    elif file.content_type == "text/csv":
        books = await BookService.import_books_from_csv(file)
    else:
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only JSON and CSV are allowed."
        )

    await BookRepository.bulk_insert_books(db, books)
    return {"message": "Books imported successfully"}
