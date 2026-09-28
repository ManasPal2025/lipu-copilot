"""Profile details kept apart from authentication identity."""

from typing import TYPE_CHECKING, Any
from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import ContactMethod, sql_in
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.user import User


class UserProfile(BaseModel):
    """Preferences a person can review later in their account."""

    __tablename__ = "user_profiles"
    __table_args__ = (
        CheckConstraint(
            f"preferred_contact_method IS NULL OR {sql_in('preferred_contact_method', ContactMethod)}",
            name="ck_user_profiles_preferred_contact_method",
        ),
    )

    user_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    display_name: Mapped[str | None] = mapped_column(String(160), nullable=True)
    preferred_contact_method: Mapped[str | None] = mapped_column(String(16), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str | None] = mapped_column(String(120), nullable=True)
    company: Mapped[str | None] = mapped_column(String(160), nullable=True)
    project_interests: Mapped[list[Any]] = mapped_column(
        JSONB,
        default=list,
        server_default=text("'[]'::jsonb"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="user_profile")
