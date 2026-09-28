"""Consultation capture for guests and signed-in customers."""

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.account import get_account_service
from app.dependencies.auth import get_optional_clerk_identity, require_clerk_identity
from app.dependencies.database import get_session
from app.domain.identity import ClerkIdentity
from app.schemas.platform import ConsultationAccepted, ConsultationHistoryPage, ConsultationSubmission
from app.services.account import AccountService
from app.services.consultations import ConsultationService


router = APIRouter(prefix="/consultations", tags=["consultations"])


def get_consultation_service(session: AsyncSession = Depends(get_session)) -> ConsultationService:
    return ConsultationService(session)


@router.get("/me", response_model=ConsultationHistoryPage)
async def list_my_consultations(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
    service: ConsultationService = Depends(get_consultation_service),
) -> ConsultationHistoryPage:
    user = await account.sync_identity(identity)
    return await service.list_for_user(user.id, page=page, page_size=page_size)


@router.post("", response_model=ConsultationAccepted, status_code=status.HTTP_201_CREATED)
async def create_consultation(
    payload: ConsultationSubmission,
    service: ConsultationService = Depends(get_consultation_service),
    identity: ClerkIdentity | None = Depends(get_optional_clerk_identity),
    account: AccountService = Depends(get_account_service),
) -> ConsultationAccepted:
    # A user_id in the body is ignored. Guests stay unattached. Signed-in
    # customers are linked to the local user for this Clerk session only.
    # Older guest enquiries with the same email are left unchanged.
    owner_id = None
    if identity is not None:
        owner = await account.sync_identity(identity)
        owner_id = owner.id
    return await service.submit(payload, authenticated_user_id=owner_id)
