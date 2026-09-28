"""Transform requests for the signed-in customer."""

from json import JSONDecodeError
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Request, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import PayloadTooLargeError, UnprocessableError
from app.dependencies.account import get_account_service
from app.dependencies.auth import require_clerk_identity
from app.dependencies.database import get_session
from app.dependencies.image_generation import get_image_generation_provider
from app.dependencies.storage import get_object_storage
from app.domain.identity import ClerkIdentity
from app.schemas.platform import (
    TransformConfigure,
    TransformHistoryPage,
    TransformPipelineView,
    TransformRequestAccepted,
    TransformRequestSubmission,
)
from app.services.account import AccountService
from app.services.image_generation import ImageGenerationProvider
from app.services.storage import ObjectStorage
from app.services.transforms import TransformService


router = APIRouter(prefix="/transform/requests", tags=["transform"])
_ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}


def get_transform_service(
    session: AsyncSession = Depends(get_session),
    storage: ObjectStorage = Depends(get_object_storage),
    generation: ImageGenerationProvider = Depends(get_image_generation_provider),
) -> TransformService:
    return TransformService(session, storage, generation)


@router.get("/me", response_model=TransformHistoryPage)
async def list_my_transformations(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
    service: TransformService = Depends(get_transform_service),
) -> TransformHistoryPage:
    user = await account.sync_identity(identity)
    return await service.list_for_user(user.id, page=page, page_size=page_size)


@router.post("", response_model=TransformRequestAccepted, status_code=status.HTTP_201_CREATED)
async def create_transform_request(
    request: Request,
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
    service: TransformService = Depends(get_transform_service),
) -> TransformRequestAccepted:
    payload, upload = await _read_submission(request)
    user = await account.sync_identity(identity)
    return await service.create_for_user(user.id, payload, upload)


@router.post("/{transform_request_id}/configure", response_model=TransformPipelineView)
async def configure_transform_request(
    transform_request_id: UUID,
    payload: TransformConfigure,
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
    service: TransformService = Depends(get_transform_service),
) -> TransformPipelineView:
    user = await account.sync_identity(identity)
    return await service.configure_for_user(
        user.id,
        transform_request_id,
        target=payload.target.value,
        variant=payload.variant.value if payload.variant is not None else None,
    )


@router.post("/{transform_request_id}/generate", response_model=TransformPipelineView)
async def generate_transform_request(
    transform_request_id: UUID,
    request: Request,
    identity: ClerkIdentity = Depends(require_clerk_identity),
    account: AccountService = Depends(get_account_service),
    service: TransformService = Depends(get_transform_service),
) -> TransformPipelineView:
    if await request.body():
        raise UnprocessableError("The request could not be accepted.")
    user = await account.sync_identity(identity)
    return await service.generate_for_user(user.id, transform_request_id)


async def _read_submission(
    request: Request,
) -> tuple[TransformRequestSubmission, tuple[bytes, str | None] | None]:
    settings = get_settings()
    limit = settings.transform_max_upload_mb * 1024 * 1024
    length = request.headers.get("content-length")
    if length and length.isdigit() and int(length) > limit + 65536:
        raise PayloadTooLargeError("Please choose an image under the size limit.")

    content_type = request.headers.get("content-type", "")
    if "multipart/form-data" in content_type:
        form = await request.form()
        file = form.get("file")
        data: bytes | None = None
        declared: str | None = None
        if file is not None and hasattr(file, "read"):
            data = await file.read(limit + 1)
            declared = getattr(file, "content_type", None)
        variant = form.get("variant")
        if not isinstance(variant, str) or not variant.strip():
            variant = None
        sample_id = form.get("sample_id")
        if not isinstance(sample_id, str) or not sample_id.strip():
            sample_id = None
        source_kind = form.get("source_kind")
        if not isinstance(source_kind, str) or not source_kind.strip():
            source_kind = "UPLOAD" if data is not None else "SAMPLE"
        mime = declared if isinstance(declared, str) and declared in _ALLOWED_MIME else "image/jpeg"
        if source_kind == "SAMPLE":
            mime = "image/png"
        payload = _submission(
            {
                "target": form.get("target"),
                "variant": variant,
                "source_asset": {
                    "mime_type": mime,
                    "source_kind": source_kind,
                    "sample_id": sample_id,
                },
            }
        )
        if payload.source_asset.source_kind == "SAMPLE":
            return payload, None
        return payload, (data or b"", declared if isinstance(declared, str) else None)

    try:
        body = await request.json()
    except JSONDecodeError as exc:
        raise UnprocessableError("The request could not be accepted.") from exc
    return _submission(body), None


def _submission(body: object) -> TransformRequestSubmission:
    try:
        return TransformRequestSubmission.model_validate(body)
    except ValidationError as exc:
        raise UnprocessableError("The request could not be accepted.") from exc
