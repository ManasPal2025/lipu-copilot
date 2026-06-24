"""Organization application service."""

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.organization import Organization
from app.repositories.organization import OrganizationRepository
from app.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.services.base import BaseService


class OrganizationService(BaseService):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.organizations = OrganizationRepository(session)

    async def list_organizations(self, *, offset: int = 0, limit: int = 100) -> list[Organization]:
        return list(await self.organizations.list_active(offset=offset, limit=limit))

    async def get_organization(self, organization_id: UUID) -> Organization:
        organization = await self.organizations.get_active(organization_id)
        if organization is None:
            raise NotFoundError("Organization not found.")
        return organization

    async def create_organization(self, payload: OrganizationCreate) -> Organization:
        if await self.organizations.get_by_slug(payload.slug):
            raise ConflictError("Organization slug already exists.", details={"slug": payload.slug})
        if await self.organizations.get_by_name(payload.name):
            raise ConflictError("Organization name already exists.", details={"name": payload.name})

        organization = await self.organizations.create(**payload.model_dump())
        await self.session.commit()
        await self.session.refresh(organization)
        return organization

    async def update_organization(self, organization_id: UUID, payload: OrganizationUpdate) -> Organization:
        organization = await self.get_organization(organization_id)
        values = payload.model_dump(exclude_unset=True)

        if "slug" in values:
            existing = await self.organizations.get_by_slug(values["slug"])
            if existing and existing.id != organization_id:
                raise ConflictError("Organization slug already exists.", details={"slug": values["slug"]})

        if "name" in values:
            existing = await self.organizations.get_by_name(values["name"])
            if existing and existing.id != organization_id:
                raise ConflictError("Organization name already exists.", details={"name": values["name"]})

        updated = await self.organizations.update(organization, **values)
        await self.session.commit()
        await self.session.refresh(updated)
        return updated

    async def delete_organization(self, organization_id: UUID) -> None:
        organization = await self.get_organization(organization_id)
        organization.deleted_at = datetime.now(UTC)
        await self.session.commit()

