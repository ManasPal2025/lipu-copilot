"""User ORM model."""

from datetime import datetime
from typing import TYPE_CHECKING, Any
from uuid import UUID as PythonUUID

from sqlalchemy import DateTime, ForeignKey, Index, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.communication import Conversation
    from app.models.consultation_request import ConsultationRequest
    from app.models.lead import Lead
    from app.models.organization import Organization
    from app.models.product_interest import ProductInterest
    from app.models.project import Project
    from app.models.transform import TransformRequest
    from app.models.user_profile import UserProfile


class User(BaseModel):
    """Identity record for a guest-capable account.

    Credentials are an external provider reference (`clerk_id`) or a one-way
    `password_hash`. This model never stores a plaintext password.
    """

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
    permissions: Mapped[list[str]] = mapped_column(
        JSONB, default=list, server_default=text("'[]'::jsonb"), nullable=False
    )
    profile: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default=text("'{}'::jsonb"), nullable=False
    )
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    login_count: Mapped[int] = mapped_column(default=0, server_default="0", nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), default="active", server_default="active", nullable=False
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    organization: Mapped["Organization"] = relationship(back_populates="users")
    user_profile: Mapped["UserProfile"] = relationship(back_populates="user", uselist=False)
    leads: Mapped[list["Lead"]] = relationship(back_populates="user", foreign_keys="Lead.user_id")
    consultation_requests: Mapped[list["ConsultationRequest"]] = relationship(
        back_populates="user",
        foreign_keys="ConsultationRequest.user_id",
    )
    projects: Mapped[list["Project"]] = relationship(
        back_populates="user", foreign_keys="Project.user_id"
    )
    transform_requests: Mapped[list["TransformRequest"]] = relationship(
        back_populates="user",
        foreign_keys="TransformRequest.user_id",
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user",
        foreign_keys="Conversation.user_id",
    )
    product_interests: Mapped[list["ProductInterest"]] = relationship(
        back_populates="user",
        foreign_keys="ProductInterest.user_id",
    )
