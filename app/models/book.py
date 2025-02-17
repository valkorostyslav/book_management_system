from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base

ALLOWED_GENRES = ["Fiction", "Non-Fiction", "Science", "History"]


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    genre: Mapped[str] = mapped_column(index=True)
    published_year: Mapped[int] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id", ondelete="CASCADE"))  # type: ignore

    author = relationship("Author", back_populates="books", lazy="selectin")  # type: ignore

    __table_args__ = (
        CheckConstraint("published_year >= 1800", name="check_published_year"),
        CheckConstraint(f"genre IN {tuple(ALLOWED_GENRES)}", name="check_genre"),
    )
