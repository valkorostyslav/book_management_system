from pydantic import BaseModel, field_validator
from datetime import datetime
from app.models.book import ALLOWED_GENRES

class BookCreateAndUpdateSchema(BaseModel):
    title: str
    genre: str
    published_year: int
    author_id: int

    @field_validator("title")
    def title_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value

    @field_validator("genre")
    def genre_valid(cls, value):
        if value not in ALLOWED_GENRES:
            raise ValueError(f"Invalid genre. Allowed genres: {', '.join(ALLOWED_GENRES)}")
        return value

    @field_validator("published_year")
    def published_year_valid(cls, value):
        current_year = datetime.now().year
        if not (1800 <= value <= current_year):
            raise ValueError(f"Published year must be between 1800 and {current_year}")
        return value

    class Config:
        str_min_length = 0
        str_strip_whitespace = True

class BookResponseSchema(BaseModel):
    id: int
    title: str
    genre: str
    published_year: int
    author_id: int

    class Config:
        from_attributes = True