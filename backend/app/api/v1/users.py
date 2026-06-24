"""User CRUD endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user import UserService


router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)


@router.get("", response_model=list[UserRead])
async def list_users(
    organization_id: UUID | None = Query(default=None),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: UserService = Depends(get_user_service),
) -> list[UserRead]:
    return await service.list_users(organization_id=organization_id, offset=offset, limit=limit)


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return await service.create_user(payload)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return await service.get_user(user_id)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
) -> UserRead:
    return await service.update_user(user_id, payload)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    service: UserService = Depends(get_user_service),
) -> Response:
    await service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

