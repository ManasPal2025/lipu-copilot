"""Organization ORM model."""

from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Index, Integer, String, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class Organization(BaseModel):
    """Tenant organization.

    Matches the organizations table from 01-DATABASE-SCHEMA.md.
    """

    __tablename__ = "organizations"
    __table_args__ = (
        UniqueConstraint("name", name="uq_organizations_name"),
        UniqueConstraint("slug", name="uq_organizations_slug"),
        Index("idx_organizations_slug", "slug"),
        Index("idx_organizations_status", "status"),
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    website_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address: Mapped[dict[str, Any] | None] = mapped_column(JSONB, nullable=True)
    founded_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active", nullable=False)
    settings: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    users: Mapped[list["User"]] = relationship(back_populates="organization", cascade="all, delete-orphan")
