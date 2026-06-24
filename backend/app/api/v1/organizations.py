"""Organization CRUD endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from app.schemas.organization import OrganizationCreate, OrganizationRead, OrganizationUpdate
from app.services.organization import OrganizationService


router = APIRouter(prefix="/organizations", tags=["organizations"])


def get_organization_service(session: AsyncSession = Depends(get_session)) -> OrganizationService:
    return OrganizationService(session)


@router.get("", response_model=list[OrganizationRead])
async def list_organizations(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: OrganizationService = Depends(get_organization_service),
) -> list[OrganizationRead]:
    return await service.list_organizations(offset=offset, limit=limit)


@router.post("", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
async def create_organization(
    payload: OrganizationCreate,
    service: OrganizationService = Depends(get_organization_service),
) -> OrganizationRead:
    return await service.create_organization(payload)


@router.get("/{organization_id}", response_model=OrganizationRead)
async def get_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
) -> OrganizationRead:
    return await service.get_organization(organization_id)


@router.patch("/{organization_id}", response_model=OrganizationRead)
async def update_organization(
    organization_id: UUID,
    payload: OrganizationUpdate,
    service: OrganizationService = Depends(get_organization_service),
) -> OrganizationRead:
    return await service.update_organization(organization_id, payload)


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: UUID,
    service: OrganizationService = Depends(get_organization_service),
) -> Response:
    await service.delete_organization(organization_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

