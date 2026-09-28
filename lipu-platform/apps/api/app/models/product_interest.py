"""What a person, lead, or consultation is asking about."""

from typing import TYPE_CHECKING
from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import ProductArea, sql_in
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.consultation_request import ConsultationRequest
    from app.models.lead import Lead
    from app.models.product import Product
    from app.models.project import Project
    from app.models.user import User


class ProductInterest(BaseModel):
    """An interest in a product area, independent of the current page layout."""

    __tablename__ = "product_interests"
    __table_args__ = (
        CheckConstraint(sql_in("area", ProductArea), name="ck_product_interests_area"),
        CheckConstraint(
            "user_id IS NOT NULL OR lead_id IS NOT NULL OR consultation_request_id IS NOT NULL OR project_id IS NOT NULL",
            name="ck_product_interests_has_owner",
        ),
        Index("idx_product_interests_user", "user_id"),
        Index("idx_product_interests_lead", "lead_id"),
        Index("idx_product_interests_consultation", "consultation_request_id"),
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
    consultation_request_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("consultation_requests.id", ondelete="SET NULL"),
        nullable=True,
    )
    project_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="SET NULL"),
        nullable=True,
    )
    product_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True,
    )
    area: Mapped[str] = mapped_column(String(32), nullable=False)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["User"] = relationship(back_populates="product_interests", foreign_keys=[user_id])
    lead: Mapped["Lead"] = relationship(back_populates="product_interests")
    consultation_request: Mapped["ConsultationRequest"] = relationship(
        back_populates="product_interests"
    )
    project: Mapped["Project"] = relationship(back_populates="product_interests")
    product: Mapped["Product"] = relationship()
