"""SQLAlchemy model for a show."""

from typing import Optional
import datetime
import typing
from sqlalchemy import String, Integer, Date, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base

if typing.TYPE_CHECKING:
    from .episode import Episode
    from .network import Network
    from .season import Season
    from .show_genre import ShowGenre


class Show(Base):
    """SQLAlchemy model for a show."""

    __tablename__ = "shows"

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    maze_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(255))
    runtime: Mapped[Optional[int]] = mapped_column(Integer)
    averageRuntime: Mapped[Optional[int]] = mapped_column(Integer)
    premiered: Mapped[Optional[datetime.date]] = mapped_column(Date)
    ended: Mapped[Optional[datetime.date]] = mapped_column(Date)
    schedule_time: Mapped[Optional[str]] = mapped_column(String(255))
    schedule_days: Mapped[Optional[str]] = mapped_column(String(255))
    network_id: Mapped[Optional[int]] = mapped_column(ForeignKey("networks.id"))
    externals_imdb: Mapped[Optional[str]] = mapped_column(String(255))
    image_medium: Mapped[Optional[str]] = mapped_column(String(255))
    image_original: Mapped[Optional[str]] = mapped_column(String(255))
    summary: Mapped[Optional[str]] = mapped_column(Text)
    updated: Mapped[Optional[int]] = mapped_column(Integer)

    # Relationships - referenced in this model
    seasons: Mapped[list["Season"]] = relationship(back_populates="show", cascade="all, delete-orphan")
    episodes: Mapped[list["Episode"]] = relationship(back_populates="show", cascade="all, delete-orphan")

    # Relationships - referencing this model
    network: Mapped["Network"] = relationship(back_populates="shows")
    show_genres: Mapped[list["ShowGenre"]] = relationship(back_populates="show")
