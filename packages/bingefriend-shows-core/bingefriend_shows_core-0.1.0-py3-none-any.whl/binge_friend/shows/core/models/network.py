"""SQLAlchemy model for a network."""
from typing import Optional
from typing_extensions import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base

if TYPE_CHECKING:
    from .show import Show


class Network(Base):
    """SQLAlchemy model for a network."""

    __tablename__ = "networks"

    # Attributes
    id: Mapped[int] = mapped_column(primary_key=True)
    maze_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String)
    country_name: Mapped[Optional[str]] = mapped_column(String)
    country_code: Mapped[Optional[str]] = mapped_column(String)
    country_timezone: Mapped[Optional[str]] = mapped_column(String)

    # Relationships - referencing this model
    shows: Mapped[list["Show"]] = relationship(back_populates="network")
    seasons: Mapped[list["Show"]] = relationship(back_populates="network")
