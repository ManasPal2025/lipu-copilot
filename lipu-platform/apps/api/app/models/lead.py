"""Lead records that can arrive from any Ecotech client."""

from typing import TYPE_CHECKING
from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import LeadPriority, LeadSource, LeadStatus, sql_in
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.consultation_request import ConsultationRequest
    from app.models.communication import CommunicationEvent, Conversation
    from app.models.product_interest import ProductInterest
    from app.models.project import Project
    from app.models.user import User


class Lead(BaseModel):
    """A person or enquiry Ecotech may follow, including guests."""

    __tablename__ = "leads"
    __table_args__ = (
        CheckConstraint(sql_in("source", LeadSource), name="ck_leads_source"),
        CheckConstraint(sql_in("status", LeadStatus), name="ck_leads_status"),
        CheckConstraint(sql_in("priority", LeadPriority), name="ck_leads_priority"),
        Index("idx_leads_status", "status"),
        Index("idx_leads_source", "source"),
        Index("idx_leads_email", "email"),
        Index("idx_leads_user", "user_id"),
    )

    user_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    source: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=LeadStatus.NEW.value, nullable=False)
    priority: Mapped[str] = mapped_column(
        String(16), default=LeadPriority.NORMAL.value, nullable=False
    )
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(32), nullable=True)
    location: Mapped[str | None] = mapped_column(String(160), nullable=True)
    project_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    user: Mapped["User"] = relationship(back_populates="leads", foreign_keys=[user_id])
    consultation_requests: Mapped[list["ConsultationRequest"]] = relationship(back_populates="lead")
    projects: Mapped[list["Project"]] = relationship(back_populates="lead")
    product_interests: Mapped[list["ProductInterest"]] = relationship(back_populates="lead")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="lead")
    communication_events: Mapped[list["CommunicationEvent"]] = relationship(back_populates="lead")
