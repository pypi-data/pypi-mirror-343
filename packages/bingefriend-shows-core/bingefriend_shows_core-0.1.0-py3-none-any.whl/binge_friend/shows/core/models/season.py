"""SQLAlchemy model for a season."""

import datetime
import typing
from typing import Optional
from sqlalchemy import ForeignKey, Integer, String, Date, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if typing.TYPE_CHECKING:
    from .episode import Episode
    from .network import Network
    from .show import Show


class Season(Base):
    """SQLAlchemy model for a season."""

    __tablename__ = "seasons"

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    maze_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(255))
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    episodeOrder: Mapped[Optional[int]] = mapped_column(Integer)
    premiereDate: Mapped[Optional[datetime.date]] = mapped_column(Date)
    endDate: Mapped[Optional[datetime.date]] = mapped_column(Date)
    network_id: Mapped[Optional[int]] = mapped_column(ForeignKey("networks.id"))
    image_medium: Mapped[Optional[str]] = mapped_column(String(255))
    image_original: Mapped[Optional[str]] = mapped_column(String(255))
    summary: Mapped[Optional[str]] = mapped_column(Text)
    show_id: Mapped[int] = mapped_column(ForeignKey("shows.id"), nullable=False)

    # Relationships - referenced in this model
    network: Mapped[Optional["Network"]] = relationship(back_populates="seasons")
    show: Mapped["Show"] = relationship(back_populates="seasons")

    # Relationships - referencing this model
    episodes: Mapped[list["Episode"]] = relationship(back_populates="season", cascade="all, delete-orphan")
