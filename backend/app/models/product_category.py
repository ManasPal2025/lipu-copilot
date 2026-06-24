"""Product category ORM model."""

from typing import TYPE_CHECKING
from uuid import UUID as PythonUUID

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.product import Product


class ProductCategory(BaseModel):
    """Product category with optional self-referencing hierarchy."""

    __tablename__ = "product_categories"
    __table_args__ = (
        UniqueConstraint("organization_id", "slug", name="uq_product_categories_organization_id_slug"),
        Index("idx_product_categories_parent", "parent_category_id"),
        Index("idx_product_categories_active", "is_active"),
    )

    organization_id: Mapped[PythonUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_category_id: Mapped[PythonUUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("product_categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    icon_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    display_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)
    seo_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    seo_keywords: Mapped[str | None] = mapped_column(String(500), nullable=True)

    organization: Mapped["Organization"] = relationship()
    parent_category: Mapped["ProductCategory | None"] = relationship(
        remote_side="ProductCategory.id",
        back_populates="child_categories",
    )
    child_categories: Mapped[list["ProductCategory"]] = relationship(back_populates="parent_category")
    products: Mapped[list["Product"]] = relationship(back_populates="category")

