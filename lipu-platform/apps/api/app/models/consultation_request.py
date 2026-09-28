"""Consultation requests from guests or registered users."""

from typing import TYPE_CHECKING
from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import ContactMethod, LeadStatus, ProjectType, sql_in
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.lead import Lead
    from app.models.product_interest import ProductInterest
    from app.models.user import User


class ConsultationRequest(BaseModel):
    """A consultation that can be submitted without an account."""

    __tablename__ = "consultation_requests"
    __table_args__ = (
        CheckConstraint(
            sql_in("project_type", ProjectType), name="ck_consultation_requests_project_type"
        ),
        CheckConstraint(sql_in("status", LeadStatus), name="ck_consultation_requests_status"),
        CheckConstraint(
            f"preferred_contact_method IS NULL OR {sql_in('preferred_contact_method', ContactMethod)}",
            name="ck_consultation_requests_preferred_contact_method",
        ),
        Index("idx_consultation_requests_email", "email"),
        Index("idx_consultation_requests_status", "status"),
        Index("idx_consultation_requests_user", "user_id"),
        Index("idx_consultation_requests_lead", "lead_id"),
    )

    user_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    lead_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leads.id", ondelete="SET NULL"),
        nullable=True,
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    project_type: Mapped[str] = mapped_column(String(32), nullable=False)
    location: Mapped[str] = mapped_column(String(160), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    approximate_size: Mapped[str | None] = mapped_column(String(120), nullable=True)
    preferred_contact_method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    preferred_callback_time: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default=LeadStatus.NEW.value, nullable=False)
    created_by_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    updated_by_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        back_populates="consultation_requests", foreign_keys=[user_id]
    )
    lead: Mapped["Lead"] = relationship(back_populates="consultation_requests")
    product_interests: Mapped[list["ProductInterest"]] = relationship(
        back_populates="consultation_request"
    )
