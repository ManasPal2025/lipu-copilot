"""Organization repository."""

from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import func, select

from app.models.organization import Organization
from app.repositories.base import BaseRepository


class OrganizationRepository(BaseRepository[Organization]):
    model = Organization

    async def get_active(self, organization_id: UUID) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(Organization.id == organization_id, Organization.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(Organization.slug == slug, Organization.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(func.lower(Organization.name) == name.lower(), Organization.deleted_at.is_(None))
        )
        return result.scalar_one_or_none()

    async def list_active(self, *, offset: int = 0, limit: int = 100) -> Sequence[Organization]:
        result = await self.session.execute(
            select(Organization)
            .where(Organization.deleted_at.is_(None))
            .order_by(Organization.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()

