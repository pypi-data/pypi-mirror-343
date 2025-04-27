"""SQLAlchemy model for a genre."""

import typing
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if typing.TYPE_CHECKING:
    from .show_genre import ShowGenre


class Genre(Base):
    """SQLAlchemy model for a genre."""

    __tablename__ = "genres"

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    # Relationships - referencing this model
    show_genres: Mapped[list["ShowGenre"]] = relationship(back_populates="genre", cascade="all, delete-orphan")
