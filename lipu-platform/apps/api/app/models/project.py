"""Project records for work that may grow beyond a single enquiry."""

from typing import TYPE_CHECKING
from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import ProjectStatus, ProjectType, sql_in
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.lead import Lead
    from app.models.product_interest import ProductInterest
    from app.models.user import User


class Project(BaseModel):
    """A named Ecotech project, optionally linked to a guest lead."""

    __tablename__ = "projects"
    __table_args__ = (
        CheckConstraint(sql_in("project_type", ProjectType), name="ck_projects_project_type"),
        CheckConstraint(sql_in("status", ProjectStatus), name="ck_projects_status"),
        Index("idx_projects_status", "status"),
        Index("idx_projects_user", "user_id"),
        Index("idx_projects_lead", "lead_id"),
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
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    project_type: Mapped[str] = mapped_column(String(32), nullable=False)
    location: Mapped[str | None] = mapped_column(String(160), nullable=True)
    budget_range: Mapped[str | None] = mapped_column(String(80), nullable=True)
    status: Mapped[str] = mapped_column(
        String(32), default=ProjectStatus.DRAFT.value, nullable=False
    )
    requirements: Mapped[str | None] = mapped_column(Text, nullable=True)
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

    user: Mapped["User"] = relationship(back_populates="projects", foreign_keys=[user_id])
    lead: Mapped["Lead"] = relationship(back_populates="projects")
    product_interests: Mapped[list["ProductInterest"]] = relationship(back_populates="project")
