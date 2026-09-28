"""S3-compatible object storage.

PostgreSQL and the object store cannot share one transaction. Callers upload
after the database row is flushed, then commit. If the commit fails, the
caller deletes the object. A later maintenance job should remove any object
that survives a crash between those two steps.
"""

from __future__ import annotations

import asyncio
from typing import Protocol
from uuid import UUID, uuid4

import boto3
from botocore.client import Config
from botocore.exceptions import BotoCoreError, ClientError

from app.core.config import Settings
from app.core.exceptions import StorageError


class ObjectStorage(Protocol):
    async def put_object(self, key: str, body: bytes, content_type: str) -> None:
        """Store one private object."""

    async def delete_object(self, key: str) -> None:
        """Remove one object. Missing objects are not an error."""

    async def get_object(self, key: str) -> tuple[bytes, str]:
        """Return the private object bytes and content type."""

    async def signed_url(self, key: str, expires_in: int) -> str:
        """Return a short-lived URL for a private object."""


class DisabledStorage:
    """Used when object storage is not configured. Samples do not need it."""

    async def put_object(self, key: str, body: bytes, content_type: str) -> None:
        raise StorageError("Image storage is not configured.")

    async def delete_object(self, key: str) -> None:
        return None

    async def get_object(self, key: str) -> tuple[bytes, str]:
        raise StorageError("Image storage is not configured.")

    async def signed_url(self, key: str, expires_in: int) -> str:
        raise StorageError("Image storage is not configured.")


class MemoryStorage:
    """In-memory stand-in for tests. It never talks to a cloud account."""

    def __init__(self) -> None:
        self.objects: dict[str, tuple[bytes, str]] = {}
        self.fail_put = False
        self.fail_get = False
        self.deleted: list[str] = []

    async def put_object(self, key: str, body: bytes, content_type: str) -> None:
        _require_private_key(key)
        if self.fail_put:
            raise StorageError("Image storage is not configured.")
        self.objects[key] = (body, content_type)

    async def delete_object(self, key: str) -> None:
        self.deleted.append(key)
        self.objects.pop(key, None)

    async def get_object(self, key: str) -> tuple[bytes, str]:
        _require_private_key(key)
        if self.fail_get or key not in self.objects:
            raise StorageError("The image could not be stored.")
        return self.objects[key]

    async def signed_url(self, key: str, expires_in: int) -> str:
        _require_private_key(key)
        if key not in self.objects:
            raise StorageError("The image could not be stored.")
        token = uuid4().hex
        return f"https://storage.test/signed/{token}?expires={expires_in}"


class S3ObjectStorage:
    """Private bucket adapter. The vendor is selected only by configuration."""

    def __init__(self, settings: Settings) -> None:
        if not settings.storage_bucket or not settings.storage_access_key or not settings.storage_secret_key:
            raise StorageError("Image storage is not configured.")
        self.bucket = settings.storage_bucket
        self.expires_in = settings.storage_signed_url_ttl_seconds
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.storage_endpoint or None,
            aws_access_key_id=settings.storage_access_key,
            aws_secret_access_key=settings.storage_secret_key,
            region_name=settings.storage_region or "us-east-1",
            config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
        )

    async def put_object(self, key: str, body: bytes, content_type: str) -> None:
        await asyncio.to_thread(self._put, key, body, content_type)

    async def delete_object(self, key: str) -> None:
        await asyncio.to_thread(self._delete, key)

    async def get_object(self, key: str) -> tuple[bytes, str]:
        _require_private_key(key)
        return await asyncio.to_thread(self._get, key)

    async def signed_url(self, key: str, expires_in: int) -> str:
        _require_private_key(key)
        return await asyncio.to_thread(self._sign, key, expires_in)

    def create_bucket(self) -> None:
        """Create the configured bucket. Local tests use this; production buckets already exist."""

        self._client.create_bucket(Bucket=self.bucket)

    def _put(self, key: str, body: bytes, content_type: str) -> None:
        _require_private_key(key)
        try:
            self._client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=body,
                ContentType=content_type,
            )
        except (BotoCoreError, ClientError) as exc:
            raise StorageError("The image could not be stored.") from exc

    def _get(self, key: str) -> tuple[bytes, str]:
        try:
            response = self._client.get_object(Bucket=self.bucket, Key=key)
            body = response["Body"].read()
            content_type = str(response.get("ContentType") or "application/octet-stream")
            return body, content_type
        except (BotoCoreError, ClientError) as exc:
            raise StorageError("The image could not be stored.") from exc

    def _delete(self, key: str) -> None:
        try:
            self._client.delete_object(Bucket=self.bucket, Key=key)
        except (BotoCoreError, ClientError) as exc:
            raise StorageError("The image could not be stored.") from exc

    def _sign(self, key: str, expires_in: int) -> str:
        try:
            return self._client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expires_in,
            )
        except (BotoCoreError, ClientError) as exc:
            raise StorageError("The image could not be stored.") from exc


def _require_private_key(key: str) -> None:
    """Reject anything other than a server-built transform object key."""

    if not key.startswith("transform/") or ".." in key or "\\" in key or "\x00" in key:
        raise StorageError("The image could not be stored.")


def source_object_key(user_id: UUID, request_id: UUID, extension: str) -> str:
    """Build a server-owned key. The original filename is never included."""

    safe_extension = extension.strip().lower().lstrip(".")
    if safe_extension not in {"jpg", "png", "webp"}:
        raise StorageError("The image could not be stored.")
    return f"transform/{user_id}/{request_id}/source/{uuid4().hex}.{safe_extension}"


def result_object_key(user_id: UUID, request_id: UUID, extension: str) -> str:
    """Build a server-owned key for a generated image."""

    safe_extension = extension.strip().lower().lstrip(".")
    if safe_extension not in {"jpg", "png", "webp"}:
        raise StorageError("The image could not be stored.")
    return f"transform/{user_id}/{request_id}/result/{uuid4().hex}.{safe_extension}"


def build_object_storage(settings: Settings) -> ObjectStorage:
    if not settings.storage_enabled:
        return DisabledStorage()
    if settings.storage_provider != "s3":
        raise StorageError("Image storage is not configured.")
    return S3ObjectStorage(settings)
