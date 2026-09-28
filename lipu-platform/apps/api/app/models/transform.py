"""Transform requests store references to files, never image bytes."""

from typing import TYPE_CHECKING, Any
from uuid import UUID as PythonUUID

from sqlalchemy import CheckConstraint, ForeignKey, Index, String, Text, text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import (
    TransformAssetType,
    TransformStatus,
    TransformTarget,
    TransformVariant,
    sql_in,
)
from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.lead import Lead
    from app.models.user import User


class TransformRequest(BaseModel):
    """A visualization request. Generation itself is a later service."""

    __tablename__ = "transform_requests"
    __table_args__ = (
        CheckConstraint(sql_in("target", TransformTarget), name="ck_transform_requests_target"),
        CheckConstraint(sql_in("status", TransformStatus), name="ck_transform_requests_status"),
        CheckConstraint(
            f"variant IS NULL OR {sql_in('variant', TransformVariant)}",
            name="ck_transform_requests_variant",
        ),
        Index("idx_transform_requests_user", "user_id"),
        Index("idx_transform_requests_status", "status"),
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
    target: Mapped[str] = mapped_column(String(16), nullable=False)
    variant: Mapped[str | None] = mapped_column(String(32), nullable=True)
    status: Mapped[str] = mapped_column(
        String(16), default=TransformStatus.UPLOADED.value, nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="transform_requests", foreign_keys=[user_id])
    lead: Mapped["Lead"] = relationship()
    assets: Mapped[list["TransformAsset"]] = relationship(back_populates="transform_request")
    result: Mapped["TransformResult"] = relationship(
        back_populates="transform_request", uselist=False
    )


class TransformAsset(BaseModel):
    """Pointer to an object that will live in storage, not in PostgreSQL."""

    __tablename__ = "transform_assets"
    __table_args__ = (
        CheckConstraint(
            sql_in("asset_type", TransformAssetType), name="ck_transform_assets_asset_type"
        ),
        Index("idx_transform_assets_request", "transform_request_id"),
    )

    transform_request_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transform_requests.id", ondelete="CASCADE"),
        nullable=False,
    )
    asset_type: Mapped[str] = mapped_column(String(16), nullable=False)
    storage_key: Mapped[str] = mapped_column(String(500), nullable=False)
    mime_type: Mapped[str] = mapped_column(String(120), nullable=False)
    asset_metadata: Mapped[dict[str, Any]] = mapped_column(
        "metadata",
        JSONB,
        default=dict,
        server_default=text("'{}'::jsonb"),
        nullable=False,
    )

    transform_request: Mapped["TransformRequest"] = relationship(back_populates="assets")


class TransformResult(BaseModel):
    """Outcome of a transform request, linked to a result asset when one exists."""

    __tablename__ = "transform_results"

    transform_request_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transform_requests.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    result_asset_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("transform_assets.id", ondelete="SET NULL"),
        nullable=True,
    )
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    transform_request: Mapped["TransformRequest"] = relationship(back_populates="result")
    result_asset: Mapped["TransformAsset"] = relationship(foreign_keys=[result_asset_id])
