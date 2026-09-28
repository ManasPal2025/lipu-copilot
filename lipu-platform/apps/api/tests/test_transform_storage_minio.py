"""Upload a real image to local MinIO when that service is running."""

import os
import socket
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.core.config import get_settings
from app.dependencies.auth import get_optional_clerk_identity
from app.dependencies.storage import get_object_storage
from app.domain.identity import ClerkIdentity
from app.main import app
from app.services.storage import S3ObjectStorage
from tests.test_transform_requests import _jpeg, _purge, _stored, _use


def _minio_open() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", 9000), timeout=1):
            return True
    except OSError:
        return False


@pytest_asyncio.fixture
async def minio_storage():
    settings = get_settings().model_copy(
        update={
            "storage_enabled": True,
            "storage_provider": "s3",
            "storage_bucket": "lipu-transform-dev",
            "storage_region": "us-east-1",
            "storage_endpoint": "http://127.0.0.1:9000",
            "storage_access_key": os.environ.get("MINIO_ROOT_USER", "minioadmin"),
            "storage_secret_key": os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin"),
            "storage_signed_url_ttl_seconds": 900,
        }
    )
    storage = S3ObjectStorage(settings)
    try:
        storage.create_bucket()
    except Exception:
        pass
    app.dependency_overrides[get_object_storage] = lambda: storage
    identity = ClerkIdentity(
        clerk_id=f"test_clerk_{uuid4().hex}",
        email=f"transform-save-minio-{uuid4().hex}@example.com",
        first_name="Asha",
        last_name="Rao",
        avatar_url=None,
    )
    other = ClerkIdentity(
        clerk_id=f"test_clerk_{uuid4().hex}",
        email=f"transform-save-minio-{uuid4().hex}@example.com",
        first_name="Meera",
        last_name="Rao",
        avatar_url=None,
    )
    existing = {
        item["Key"]
        for item in storage._client.list_objects_v2(Bucket=storage.bucket).get("Contents", [])
    }
    try:
        yield storage, identity, other
    finally:
        app.dependency_overrides.pop(get_optional_clerk_identity, None)
        app.dependency_overrides.pop(get_object_storage, None)
        for item in storage._client.list_objects_v2(Bucket=storage.bucket).get("Contents", []):
            if item["Key"] not in existing:
                storage._client.delete_object(Bucket=storage.bucket, Key=item["Key"])
        await _purge(identity.clerk_id)
        await _purge(other.clerk_id)


@pytest.mark.asyncio
@pytest.mark.skipif(not _minio_open(), reason="MinIO is not running on port 9000")
async def test_minio_upload_is_private_to_the_owner(minio_storage) -> None:
    storage, owner, other = minio_storage
    _use(owner)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        created = await client.post(
            "/api/v1/transform/requests",
            data={"target": "WINDOWS", "variant": "SLIDING", "source_kind": "UPLOAD"},
            files={"file": ("room.jpg", _jpeg(), "image/jpeg")},
        )
        history = await client.get("/api/v1/transform/requests/me")
        _use(other)
        await client.get("/api/v1/users/me")
        hidden = await client.get("/api/v1/transform/requests/me")

    assert created.status_code == 201
    body = created.json()
    assert body["status"] == "UPLOADED"
    request, assets = await _stored(body["id"])
    key = assets[0].storage_key
    assert key.startswith("transform/")
    assert key.endswith(".jpg")
    assert "room.jpg" not in key
    stored = storage._client.get_object(Bucket=storage.bucket, Key=key)
    assert stored["Body"].read() == _jpeg()
    signed = history.json()["items"][0]["source_asset"]["public_url"]
    assert "X-Amz-Signature" in signed
    assert "storage_key" not in history.text
    async with AsyncClient() as http:
        downloaded = await http.get(signed)
    assert downloaded.status_code == 200
    assert downloaded.content == _jpeg()
    assert hidden.json()["total"] == 0
    assert signed not in hidden.text
