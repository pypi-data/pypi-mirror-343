"""SQLAlchemy model for a show-genre association."""

import typing
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if typing.TYPE_CHECKING:
    from .genre import Genre
    from .show import Show


class ShowGenre(Base):
    __tablename__ = "show_genre"

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    show_id: Mapped[int] = mapped_column(ForeignKey("shows.id"), nullable=False)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"), nullable=False)

    # Relationships - referenced in this model
    show: Mapped["Show"] = relationship(back_populates="show_genres")
    genre: Mapped["Genre"] = relationship(back_populates="shows")

    # Relationships - referencing this model
    shows: Mapped[list["Show"]] = relationship(back_populates="show_genres")
    genres: Mapped[list["Genre"]] = relationship(back_populates="shows")
