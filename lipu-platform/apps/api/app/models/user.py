"""User ORM model."""

from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID as PythonUUID

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization


class User(BaseModel):
    """Local user profile backed by Clerk authentication."""

    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("clerk_id", "email", name="uq_users_clerk_email"),
        UniqueConstraint("clerk_id", name="uq_users_clerk_id"),
        Index("idx_users_organization_role", "organization_id", "role"),
        Index("idx_users_status", "status"),
    )

    clerk_id: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    permissions: Mapped[list[str]] = mapped_column(JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False)
    profile: Mapped[dict[str, Any]] = mapped_column(JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    login_count: Mapped[int] = mapped_column(default=0, server_default="0", nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active", server_default="active", nullable=False)
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped["Organization"] = relationship(back_populates="users")
