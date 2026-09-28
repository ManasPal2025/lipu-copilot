"""Production configuration and credential-exposure checks."""

import boto3
import pytest
from botocore.client import Config
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings
from app.core.exceptions import StorageError
from app.core.production import production_blockers
from app.dependencies.auth import get_optional_clerk_identity
from app.domain.identity import ClerkIdentity
from app.main import app
from app.services.storage import MemoryStorage, S3ObjectStorage


def _production(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "app_env": "production",
        "debug": False,
        "clerk_secret_key": "sk_live_example",
        "cors_origins": ["https://www.ecotech.example"],
        "clerk_authorized_parties": ["https://www.ecotech.example"],
        "allowed_hosts": ["api.ecotech.example"],
        "database_url": "postgresql+asyncpg://app:secret@db.internal:5432/ecotech",
        "database_ssl": True,
        "storage_enabled": True,
        "storage_access_key": "AKIAEXAMPLE",
        "storage_secret_key": "secret-that-is-different",
        "storage_public_base_url": "",
        "image_generation_enabled": True,
        "openai_api_key": "sk-example",
    }
    values.update(overrides)
    return Settings(**values)


def test_valid_production_settings_have_no_blockers() -> None:
    assert production_blockers(_production()) == []


def test_production_rejects_shared_storage_credentials_and_wildcard_cors() -> None:
    problems = production_blockers(
        _production(
            cors_origins=["*"],
            storage_access_key="same-value",
            storage_secret_key="same-value",
            database_ssl=False,
        )
    )
    assert any("CORS_ORIGINS" in problem for problem in problems)
    assert any("STORAGE_ACCESS_KEY" in problem for problem in problems)
    assert any("DATABASE_SSL" in problem for problem in problems)
    assert "same-value" not in " ".join(problems)


def test_presigned_url_contains_access_key_id_but_not_secret() -> None:
    access_key = "AKIAIOSFODNN7EXAMPLE"
    secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    settings = _production(
        app_env="development",
        storage_bucket="private-bucket",
        storage_region="us-east-1",
        storage_endpoint="https://s3.amazonaws.com",
        storage_access_key=access_key,
        storage_secret_key=secret,
    )
    storage = S3ObjectStorage(settings)
    url = storage._sign("transform/user/request/source/file.png", 900)
    assert secret not in url
    assert access_key in url
    assert "X-Amz-Credential" in url
    assert "X-Amz-Signature" in url


def test_boto_signature_matches_distinct_credentials() -> None:
    access_key = "AKIAIOSFODNN7EXAMPLE"
    secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    client = boto3.client(
        "s3",
        endpoint_url="https://s3.amazonaws.com",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret,
        region_name="us-east-1",
        config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
    )
    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": "private-bucket", "Key": "transform/user/request/result/file.png"},
        ExpiresIn=900,
    )
    assert secret not in url
    assert access_key in url


@pytest.mark.asyncio
async def test_memory_signed_url_does_not_embed_storage_key() -> None:
    storage = MemoryStorage()
    key = "transform/user/request/source/file.png"
    await storage.put_object(key, b"\xff\xd8\xff", "image/jpeg")
    url = await storage.signed_url(key, 60)
    assert key not in url
    assert "file.png" not in url


@pytest.mark.asyncio
async def test_storage_rejects_path_traversal() -> None:
    storage = MemoryStorage()
    with pytest.raises(StorageError):
        await storage.put_object("transform/../secret", b"\xff\xd8\xff", "image/jpeg")


@pytest.mark.asyncio
async def test_staff_routes_require_authentication() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
        for path in ("/api/v1/organizations", "/api/v1/quotes", "/api/v1/catalog/products"):
            response = await client.get(path)
            assert response.status_code == 401
            assert "sk_" not in response.text
            assert "postgres" not in response.text.lower()


@pytest.mark.asyncio
async def test_authenticated_customer_cannot_use_staff_routes() -> None:
    identity = ClerkIdentity(
        clerk_id="test_clerk_staff_gate",
        email="qa-staff-gate@example.com",
        first_name="QA",
        last_name="Gate",
        avatar_url=None,
    )
    app.dependency_overrides[get_optional_clerk_identity] = lambda: identity
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:
            response = await client.get("/api/v1/organizations")
    finally:
        app.dependency_overrides.pop(get_optional_clerk_identity, None)
    assert response.status_code == 403
