"""Quote management endpoints."""

from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_session
from app.schemas.pagination import Page
from app.schemas.quote import (
    QuoteConvertToOrder,
    QuoteCreate,
    QuoteDetailRead,
    QuoteItemCreate,
    QuoteItemRead,
    QuoteItemUpdate,
    QuoteRead,
    QuoteReject,
    QuoteSort,
    QuoteStatus,
    QuoteUpdate,
)
from app.services.quote import QuoteService


router = APIRouter(prefix="/quotes", tags=["quotes"])


def get_quote_service(session: AsyncSession = Depends(get_session)) -> QuoteService:
    return QuoteService(session)


@router.get("", response_model=Page[QuoteRead])
async def list_quotes(
    organization_id: UUID | None = Query(default=None),
    customer_id: UUID | None = Query(default=None),
    status_filter: QuoteStatus | None = Query(default=None, alias="status"),
    valid_from: date | None = Query(default=None),
    valid_to: date | None = Query(default=None),
    sort: QuoteSort = Query(default="-created_at"),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    service: QuoteService = Depends(get_quote_service),
) -> Page[QuoteRead]:
    return await service.list_quotes(
        organization_id=organization_id,
        customer_id=customer_id,
        status=status_filter,
        valid_from=valid_from,
        valid_to=valid_to,
        sort=sort,
        offset=offset,
        limit=limit,
    )


@router.post("", response_model=QuoteDetailRead, status_code=status.HTTP_201_CREATED)
async def create_quote(
    payload: QuoteCreate,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteDetailRead:
    return await service.create_quote(payload)


@router.get("/{quote_id}", response_model=QuoteDetailRead)
async def get_quote(
    quote_id: UUID,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteDetailRead:
    return await service.get_quote(quote_id, include_items=True)


@router.patch("/{quote_id}", response_model=QuoteDetailRead)
async def update_quote(
    quote_id: UUID,
    payload: QuoteUpdate,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteDetailRead:
    return await service.update_quote(quote_id, payload)


@router.delete("/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(
    quote_id: UUID,
    service: QuoteService = Depends(get_quote_service),
) -> Response:
    await service.delete_quote(quote_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{quote_id}/items", response_model=QuoteItemRead, status_code=status.HTTP_201_CREATED)
async def add_quote_item(
    quote_id: UUID,
    payload: QuoteItemCreate,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteItemRead:
    return await service.add_item(quote_id, payload)


@router.patch("/{quote_id}/items/{item_id}", response_model=QuoteItemRead)
async def update_quote_item(
    quote_id: UUID,
    item_id: UUID,
    payload: QuoteItemUpdate,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteItemRead:
    return await service.update_item(quote_id, item_id, payload)


@router.delete("/{quote_id}/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote_item(
    quote_id: UUID,
    item_id: UUID,
    service: QuoteService = Depends(get_quote_service),
) -> Response:
    await service.delete_item(quote_id, item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{quote_id}/send", response_model=QuoteDetailRead)
async def send_quote(
    quote_id: UUID,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteDetailRead:
    return await service.send_quote(quote_id)


@router.post("/{quote_id}/accept", response_model=QuoteDetailRead)
async def accept_quote(
    quote_id: UUID,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteDetailRead:
    return await service.accept_quote(quote_id)


@router.post("/{quote_id}/reject", response_model=QuoteDetailRead)
async def reject_quote(
    quote_id: UUID,
    payload: QuoteReject,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteDetailRead:
    return await service.reject_quote(quote_id, payload)


@router.post("/{quote_id}/convert-to-order", response_model=QuoteDetailRead)
async def convert_quote_to_order(
    quote_id: UUID,
    payload: QuoteConvertToOrder,
    service: QuoteService = Depends(get_quote_service),
) -> QuoteDetailRead:
    return await service.convert_to_order(quote_id, payload)

