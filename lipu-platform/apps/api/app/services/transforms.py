"""Transform requests for the signed-in customer."""

import time
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.config import get_settings
from app.core.exceptions import ConflictError, GenerationError, NotFoundError, StorageError, UnprocessableError
from app.core.logging import get_logger
from app.domain.enums import TransformAssetType, TransformStatus
from app.models.transform import TransformAsset, TransformRequest, TransformResult
from app.schemas.platform import (
    TransformHistoryAsset,
    TransformHistoryItem,
    TransformHistoryPage,
    TransformHistoryResult,
    TransformPipelineAsset,
    TransformPipelineView,
    TransformRequestAccepted,
    TransformRequestSubmission,
)
from app.services.base import BaseService
from app.services.image_generation import (
    ImageGenerationProvider,
    build_image_generation_provider,
)
from app.services.image_uploads import detect_image
from app.services.storage import (
    ObjectStorage,
    build_object_storage,
    result_object_key,
    source_object_key,
)
from app.services.transform_prompts import build_transform_prompt, variants_match

logger = get_logger(__name__)

GENERATED_MAX_BYTES = 20 * 1024 * 1024

# Catalogue images already served by the site. These are references, not uploads.
SAMPLE_CATALOGUE: dict[str, str] = {
    "living": "/images/transform/ecotech/transform-sample-living-01.png",
    "balcony": "/images/transform/ecotech/transform-sample-balcony-01.png",
    "apartment": "/images/transform/ecotech/transform-sample-apartment-01.png",
    "villa": "/images/transform/ecotech/transform-sample-villa-01.png",
}
SAMPLE_MIME = "image/png"


def public_asset_url(storage_key: str) -> str | None:
    """Return a site path only when the key is an existing catalogue image."""

    key = storage_key.strip()
    if not key.startswith("/images/"):
        return None
    if any(token in key for token in ("..", "\\", "\n", "\r", "?", "#", "://")):
        return None
    return key


def _source_asset(request: TransformRequest) -> TransformAsset | None:
    sources = [
        asset
        for asset in request.assets
        if asset.asset_type == TransformAssetType.SOURCE.value
    ]
    if not sources:
        return None
    sources.sort(key=lambda asset: (asset.created_at, asset.id), reverse=True)
    return sources[0]


class TransformService(BaseService):
    def __init__(
        self,
        session: AsyncSession,
        storage: ObjectStorage | None = None,
        generation: ImageGenerationProvider | None = None,
    ) -> None:
        super().__init__(session)
        settings = get_settings()
        self.storage = storage if storage is not None else build_object_storage(settings)
        self.generation = (
            generation if generation is not None else build_image_generation_provider(settings)
        )

    async def create_for_user(
        self,
        user_id: UUID,
        payload: TransformRequestSubmission,
        upload: tuple[bytes, str | None] | None = None,
    ) -> TransformRequestAccepted:
        """Store one request and its source, then commit both together.

        Object storage is not part of the database transaction. If the commit
        fails after an upload, the object is deleted. A crash between those
        steps can leave an orphan object for a later cleanup job.
        """

        uploaded_key: str | None = None
        try:
            request = TransformRequest(
                user_id=user_id,
                target=payload.target.value,
                variant=payload.variant.value if payload.variant is not None else None,
                status=TransformStatus.UPLOADED.value,
            )
            self.session.add(request)
            await self.session.flush()
            storage_key, mime_type, metadata = await self._source_pointer(
                user_id, request.id, payload, upload
            )
            if metadata.get("storage") == "object":
                uploaded_key = storage_key
            self.session.add(
                TransformAsset(
                    transform_request_id=request.id,
                    asset_type=TransformAssetType.SOURCE.value,
                    storage_key=storage_key,
                    mime_type=mime_type,
                    asset_metadata=metadata,
                )
            )
            await self.session.commit()
            await self.session.refresh(request)
        except Exception:
            await self.session.rollback()
            if uploaded_key is not None:
                await self._discard_object(uploaded_key)
            raise
        return TransformRequestAccepted(
            id=request.id,
            created_at=request.created_at,
            target=request.target,
            variant=request.variant,
            status=request.status,
        )

    async def configure_for_user(
        self,
        user_id: UUID,
        request_id: UUID,
        *,
        target: str,
        variant: str | None,
    ) -> TransformPipelineView:
        """Move an owned upload from UPLOADED to CONFIGURED."""

        request = await self._owned(user_id, request_id, lock=True)
        if request.status != TransformStatus.UPLOADED.value:
            raise ConflictError("This transformation cannot be configured.")
        if not variants_match(target, variant):
            raise UnprocessableError("That opening does not match the selected target.")
        request.target = target
        request.variant = variant
        request.status = TransformStatus.CONFIGURED.value
        await self.session.commit()
        await self.session.refresh(request)
        return self._pipeline_view(request, result=None)

    async def generate_for_user(self, user_id: UUID, request_id: UUID) -> TransformPipelineView:
        """Generate one private result from the customer's stored source image.

        Object storage and PostgreSQL cannot share a transaction. The result
        object is deleted if the completion commit fails. The source object is
        kept. A crash after upload and before commit can leave an orphan result
        for a later cleanup job.
        """

        request = await self._owned(user_id, request_id, lock=True)
        self._require_generatable(request)
        source = await self._source_row(request.id)
        if source is None or not source.storage_key.startswith("transform/"):
            raise UnprocessableError("An uploaded image is required.")
        request.status = TransformStatus.PROCESSING.value
        await self.session.commit()
        started = time.perf_counter()
        self._log("transform_generation_started", request, user_id, duration_ms=0)
        uploaded_key: str | None = None
        try:
            data, _content_type = await self.storage.get_object(source.storage_key)
            prompt, prompt_version = build_transform_prompt(request.target, request.variant)
            generated = await self.generation.generate(
                image_bytes=data,
                mime_type=source.mime_type,
                prompt=prompt,
            )
            mime_type, extension = detect_image(generated.data, None, max_bytes=GENERATED_MAX_BYTES)
            uploaded_key = result_object_key(user_id, request.id, extension)
            await self.storage.put_object(uploaded_key, generated.data, mime_type)
            outcome = await self._complete(
                request.id,
                user_id,
                uploaded_key,
                mime_type,
                prompt_version,
                generated.provider,
                generated.model,
            )
        except Exception as exc:
            await self._fail_generation(
                request.id,
                user_id,
                request.target,
                request.variant,
                uploaded_key,
                exc,
                started,
            )
            raise
        duration_ms = int((time.perf_counter() - started) * 1000)
        self._log("transform_generation_completed", request, user_id, duration_ms=duration_ms)
        return outcome

    def _require_generatable(self, request: TransformRequest) -> None:
        if request.status == TransformStatus.PROCESSING.value:
            raise ConflictError("Transformation is already being processed.")
        if request.status == TransformStatus.COMPLETED.value:
            raise ConflictError("This transformation is already complete.")
        if request.status not in {TransformStatus.CONFIGURED.value, TransformStatus.FAILED.value}:
            raise ConflictError("Configure this transformation before generating it.")

    async def _complete(
        self,
        request_id: UUID,
        user_id: UUID,
        storage_key: str,
        mime_type: str,
        prompt_version: str,
        provider: str,
        model: str,
    ) -> TransformPipelineView:
        request = await self._owned(user_id, request_id, lock=True)
        asset = TransformAsset(
            transform_request_id=request.id,
            asset_type=TransformAssetType.RESULT.value,
            storage_key=storage_key,
            mime_type=mime_type,
            asset_metadata={
                "storage": "object",
                "prompt_version": prompt_version,
                "provider": provider,
                "model": model,
            },
        )
        self.session.add(asset)
        await self.session.flush()
        existing = await self.session.scalar(
            select(TransformResult).where(TransformResult.transform_request_id == request.id)
        )
        if existing is None:
            self.session.add(
                TransformResult(transform_request_id=request.id, result_asset_id=asset.id, summary=None)
            )
        else:
            existing.result_asset_id = asset.id
            existing.summary = None
        request.status = TransformStatus.COMPLETED.value
        await self.session.commit()
        await self.session.refresh(request)
        ttl = get_settings().storage_signed_url_ttl_seconds
        try:
            public_url = await self.storage.signed_url(storage_key, ttl)
        except Exception:
            public_url = None
        return self._pipeline_view(
            request,
            result=TransformPipelineAsset(id=asset.id, mime_type=mime_type, public_url=public_url),
        )

    async def _fail_generation(
        self,
        request_id: UUID,
        user_id: UUID,
        target: str,
        variant: str | None,
        uploaded_key: str | None,
        exc: Exception,
        started: float,
    ) -> None:
        await self.session.rollback()
        if uploaded_key is not None:
            await self._discard_object(uploaded_key)
        await self._mark_failed(request_id, user_id)
        category = exc.category if isinstance(exc, GenerationError) else "generation"
        if isinstance(exc, StorageError):
            category = "storage"
        elif isinstance(exc, UnprocessableError):
            category = "invalid_result"
        duration_ms = int((time.perf_counter() - started) * 1000)
        logger.warning(
            "transform_generation_failed",
            extra={
                "transform_request_id": str(request_id),
                "user_id": str(user_id),
                "target": target,
                "variant": variant,
                "provider": getattr(self.generation, "name", "unknown"),
                "duration_ms": duration_ms,
                "failure_category": category,
            },
        )
        if not isinstance(exc, GenerationError):
            raise GenerationError(category=category) from exc

    async def _mark_failed(self, request_id: UUID, user_id: UUID) -> None:
        request = await self.session.get(TransformRequest, request_id)
        if request is None or request.user_id != user_id:
            return
        if request.status == TransformStatus.COMPLETED.value:
            return
        request.status = TransformStatus.FAILED.value
        await self.session.commit()

    async def _owned(self, user_id: UUID, request_id: UUID, *, lock: bool) -> TransformRequest:
        statement = select(TransformRequest).where(
            TransformRequest.id == request_id,
            TransformRequest.user_id == user_id,
        )
        if lock:
            statement = statement.with_for_update()
        request = await self.session.scalar(statement)
        if request is None:
            raise NotFoundError("The transformation could not be found.")
        return request

    async def _source_row(self, request_id: UUID) -> TransformAsset | None:
        assets = list(
            (
                await self.session.scalars(
                    select(TransformAsset).where(
                        TransformAsset.transform_request_id == request_id,
                        TransformAsset.asset_type == TransformAssetType.SOURCE.value,
                    )
                )
            ).all()
        )
        if not assets:
            return None
        assets.sort(key=lambda asset: (asset.created_at, asset.id), reverse=True)
        return assets[0]

    def _pipeline_view(
        self, request: TransformRequest, *, result: TransformPipelineAsset | None
    ) -> TransformPipelineView:
        return TransformPipelineView(
            id=request.id,
            status=request.status,
            target=request.target,
            variant=request.variant,
            result=result,
        )

    def _log(
        self, event: str, request: TransformRequest, user_id: UUID, *, duration_ms: int
    ) -> None:
        logger.info(
            event,
            extra={
                "transform_request_id": str(request.id),
                "user_id": str(user_id),
                "target": request.target,
                "variant": request.variant,
                "provider": getattr(self.generation, "name", "unknown"),
                "duration_ms": duration_ms,
            },
        )

    async def list_for_user(
        self, user_id: UUID, *, page: int, page_size: int
    ) -> TransformHistoryPage:
        """Return one customer's transform requests, newest first."""

        total = await self.session.scalar(
            select(func.count())
            .select_from(TransformRequest)
            .where(TransformRequest.user_id == user_id)
        )
        total_count = int(total or 0)
        offset = (page - 1) * page_size
        result = await self.session.scalars(
            select(TransformRequest)
            .where(TransformRequest.user_id == user_id)
            .options(
                selectinload(TransformRequest.assets),
                selectinload(TransformRequest.result).selectinload(TransformResult.result_asset),
            )
            .order_by(TransformRequest.created_at.desc(), TransformRequest.id.desc())
            .offset(offset)
            .limit(page_size)
        )
        rows = list(result.all())
        items = [await self._present(row) for row in rows]
        return TransformHistoryPage(
            items=items,
            page=page,
            page_size=page_size,
            total=total_count,
            has_next=offset + len(rows) < total_count,
        )

    async def _source_pointer(
        self,
        user_id: UUID,
        request_id: UUID,
        payload: TransformRequestSubmission,
        upload: tuple[bytes, str | None] | None,
    ) -> tuple[str, str, dict[str, str]]:
        source = payload.source_asset
        if source.source_kind == "SAMPLE":
            if upload is not None:
                raise UnprocessableError("A sample image is not uploaded.")
            sample_id = source.sample_id or ""
            return (
                SAMPLE_CATALOGUE[sample_id],
                SAMPLE_MIME,
                {"source_kind": "SAMPLE", "sample_id": sample_id, "storage": "demo-catalogue"},
            )
        if upload is None:
            raise UnprocessableError("An image file is required.")
        data, declared = upload
        limit = get_settings().transform_max_upload_mb * 1024 * 1024
        mime_type, extension = detect_image(data, declared, max_bytes=limit)
        key = source_object_key(user_id, request_id, extension)
        await self.storage.put_object(key, data, mime_type)
        return key, mime_type, {"source_kind": "UPLOAD", "storage": "object"}

    async def _discard_object(self, key: str) -> None:
        try:
            await self.storage.delete_object(key)
        except Exception as exc:
            logger.warning(
                "Could not remove an object after a failed transform save",
                extra={"error_type": type(exc).__name__},
            )

    async def _view_url(self, asset: TransformAsset | None) -> str | None:
        if asset is None:
            return None
        catalogue = public_asset_url(asset.storage_key)
        if catalogue is not None:
            return catalogue
        if not asset.storage_key.startswith("transform/"):
            return None
        try:
            ttl = get_settings().storage_signed_url_ttl_seconds
            return await self.storage.signed_url(asset.storage_key, ttl)
        except Exception:
            return None

    async def _present_asset(self, asset: TransformAsset | None) -> TransformHistoryAsset | None:
        if asset is None:
            return None
        return TransformHistoryAsset(
            id=asset.id,
            mime_type=asset.mime_type,
            public_url=await self._view_url(asset),
        )

    async def _present(self, row: TransformRequest) -> TransformHistoryItem:
        outcome = row.result
        result_asset = None if outcome is None else outcome.result_asset
        return TransformHistoryItem(
            id=row.id,
            created_at=row.created_at,
            target=row.target,
            variant=row.variant,
            status=row.status,
            source_asset=await self._present_asset(_source_asset(row)),
            result=None
            if outcome is None
            else TransformHistoryResult(
                id=outcome.id,
                created_at=outcome.created_at,
                asset=await self._present_asset(result_asset),
            ),
        )
