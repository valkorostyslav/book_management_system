from typing import List

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

from .book import Book


class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    biography: Mapped[str] = mapped_column(Text, nullable=False, default="")

    books: Mapped[List[Book]] = relationship(
        "Book", back_populates="author", lazy="selectin"
    )
