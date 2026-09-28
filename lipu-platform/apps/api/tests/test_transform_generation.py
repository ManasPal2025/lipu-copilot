"""Visualization pipeline for an owned transform request."""

import asyncio
from collections.abc import AsyncIterator
from uuid import UUID

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select

from app.core.exceptions import GenerationError
from app.db.session import AsyncSessionLocal, engine
from app.dependencies.auth import get_optional_clerk_identity
from app.dependencies.image_generation import get_image_generation_provider
from app.dependencies.storage import get_object_storage
from app.domain.identity import ClerkIdentity
from app.main import app
from app.models.transform import TransformAsset
from app.services.image_generation import DisabledImageGenerationProvider, GeneratedImage
from app.services.storage import MemoryStorage
from app.services.transforms import TransformService
from tests.test_transform_requests import (
    _client,
    _jpeg,
    _png,
    _purge,
    _stored,
    _use,
    _user_id,
)

_memory = MemoryStorage()
_fake = None


class FakeProvider:
    name = "fake"

    def __init__(self) -> None:
        self.calls = 0
        self.fail = False
        self.malformed = False
        self.prompts: list[str] = []

    async def generate(self, *, image_bytes: bytes, mime_type: str, prompt: str) -> GeneratedImage:
        self.calls += 1
        self.prompts.append(prompt)
        if self.fail:
            raise GenerationError(category="provider")
        if self.malformed:
            return GeneratedImage(b"not-an-image", "image/png", "fake", "fake-model")
        return GeneratedImage(_png(), "image/png", "fake", "fake-model")


class GateProvider:
    name = "fake"

    def __init__(self) -> None:
        self.calls = 0
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def generate(self, *, image_bytes: bytes, mime_type: str, prompt: str) -> GeneratedImage:
        self.calls += 1
        self.started.set()
        await self.release.wait()
        return GeneratedImage(_png(), "image/png", "fake", "fake-model")


def _identity(name: str) -> ClerkIdentity:
    from uuid import uuid4

    return ClerkIdentity(
        clerk_id=f"test_clerk_{uuid4().hex}",
        email=f"transform-gen-{name}-{uuid4().hex}@example.com",
        first_name=name,
        last_name="Rao",
        avatar_url=None,
    )


@pytest_asyncio.fixture
async def identities() -> AsyncIterator[tuple[ClerkIdentity, ClerkIdentity, FakeProvider]]:
    global _memory, _fake
    owner = _identity("Asha")
    other = _identity("Meera")
    _memory = MemoryStorage()
    _fake = FakeProvider()
    app.dependency_overrides[get_object_storage] = lambda: _memory
    app.dependency_overrides[get_image_generation_provider] = lambda: _fake
    try:
        yield owner, other, _fake
    finally:
        app.dependency_overrides.pop(get_optional_clerk_identity, None)
        app.dependency_overrides.pop(get_object_storage, None)
        app.dependency_overrides.pop(get_image_generation_provider, None)
        await _purge(owner.clerk_id)
        await _purge(other.clerk_id)
        await engine.dispose()


async def _upload(client: AsyncClient) -> str:
    created = await client.post(
        "/api/v1/transform/requests",
        data={"target": "WINDOWS", "variant": "SLIDING", "source_kind": "UPLOAD"},
        files={"file": ("room.jpg", _jpeg(), "image/jpeg")},
    )
    assert created.status_code == 201
    return str(created.json()["id"])


async def _configure(client: AsyncClient, request_id: str, **extra: object) -> object:
    body: dict[str, object] = {"target": "WINDOWS", "variant": "SLIDING"}
    body.update(extra)
    return await client.post(f"/api/v1/transform/requests/{request_id}/configure", json=body)


@pytest.mark.asyncio
async def test_configure_and_generate_require_authentication() -> None:
    app.dependency_overrides.pop(get_optional_clerk_identity, None)
    request_id = "11111111-1111-1111-1111-111111111111"
    async with _client() as client:
        configured = await client.post(
            f"/api/v1/transform/requests/{request_id}/configure",
            json={"target": "WINDOWS", "variant": "SLIDING"},
        )
        generated = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
    assert configured.status_code == 401
    assert generated.status_code == 401


@pytest.mark.asyncio
async def test_owner_configures_and_completes_a_private_result(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, other, fake = identities
    _use(owner)
    async with _client() as client:
        request_id = await _upload(client)
        configured = await _configure(client, request_id)
        generated = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
        history = await client.get("/api/v1/transform/requests/me")
        _use(other)
        await client.get("/api/v1/users/me")
        hidden = await client.get("/api/v1/transform/requests/me")
        denied_configure = await _configure(client, request_id)
        denied_generate = await client.post(f"/api/v1/transform/requests/{request_id}/generate")

    assert configured.status_code == 200
    configured_body = configured.json()
    assert configured_body["status"] == "CONFIGURED"
    assert configured_body["result"] is None
    assert generated.status_code == 200
    body = generated.json()
    assert body["status"] == "COMPLETED"
    assert body["target"] == "WINDOWS"
    assert body["variant"] == "SLIDING"
    assert body["result"]["mime_type"] == "image/png"
    assert body["result"]["public_url"].startswith("https://storage.test/signed/")
    assert "storage_key" not in generated.text
    assert "prompt" not in generated.text.lower()
    assert "photorealistic" not in generated.text.lower()
    assert "user_id" not in body
    assert fake.calls == 1
    assert "sliding panels" in fake.prompts[0]
    request, assets = await _stored(request_id)
    assert request.status == "COMPLETED"
    result_assets = [asset for asset in assets if asset.asset_type == "RESULT"]
    source_assets = [asset for asset in assets if asset.asset_type == "SOURCE"]
    assert len(result_assets) == 1
    assert result_assets[0].storage_key.startswith(f"transform/{request.user_id}/{request_id}/result/")
    assert result_assets[0].storage_key.endswith(".png")
    assert "room.jpg" not in result_assets[0].storage_key
    assert result_assets[0].asset_metadata["prompt_version"] == "v1"
    assert source_assets[0].storage_key in _memory.objects
    assert result_assets[0].storage_key in _memory.objects
    mine = history.json()["items"][0]
    assert mine["result"]["asset"]["public_url"].startswith("https://storage.test/signed/")
    assert "storage_key" not in history.text
    assert hidden.json()["total"] == 0
    assert mine["result"]["asset"]["public_url"] not in hidden.text
    assert denied_configure.status_code == 404
    assert denied_generate.status_code == 404


@pytest.mark.asyncio
async def test_incompatible_variant_stays_uploaded(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, fake = identities
    _use(owner)
    async with _client() as client:
        request_id = await _upload(client)
        rejected = await _configure(client, request_id, target="BALCONY", variant="SLIDING")
    assert rejected.status_code == 422
    request, _assets = await _stored(request_id)
    assert request.status == "UPLOADED"
    assert fake.calls == 0


@pytest.mark.asyncio
async def test_generate_rejects_duplicate_processing_and_completed(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, _fake = identities
    gate = GateProvider()
    app.dependency_overrides[get_image_generation_provider] = lambda: gate
    _use(owner)
    async with _client() as client:
        request_id = await _upload(client)
        assert (await _configure(client, request_id)).status_code == 200
        first = asyncio.create_task(client.post(f"/api/v1/transform/requests/{request_id}/generate"))
        await gate.started.wait()
        duplicate = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
        gate.release.set()
        completed = await first
        again = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
    assert duplicate.status_code == 409
    assert "already being processed" in duplicate.json()["error"]["message"]
    assert completed.status_code == 200
    assert again.status_code == 409
    assert gate.calls == 1


@pytest.mark.asyncio
async def test_provider_failure_keeps_the_source(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, fake = identities
    fake.fail = True
    _use(owner)
    async with _client() as client:
        request_id = await _upload(client)
        await _configure(client, request_id)
        failed = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
        retry = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
    assert failed.status_code == 503
    assert "traceback" not in failed.text.lower()
    assert "openai" not in failed.text.lower()
    request, assets = await _stored(request_id)
    assert request.status == "FAILED"
    assert all(asset.asset_type == "SOURCE" for asset in assets)
    assert fake.calls == 2
    assert retry.status_code == 503


@pytest.mark.asyncio
async def test_disabled_provider_fails_without_calling_openai(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, _fake = identities
    app.dependency_overrides[get_image_generation_provider] = lambda: DisabledImageGenerationProvider()
    _use(owner)
    async with _client() as client:
        request_id = await _upload(client)
        await _configure(client, request_id)
        failed = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
    assert failed.status_code == 503
    assert failed.json()["error"]["code"] == "generation_unavailable"
    request, _assets = await _stored(request_id)
    assert request.status == "FAILED"


@pytest.mark.asyncio
async def test_malformed_provider_result_does_not_store_an_object(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, fake = identities
    fake.malformed = True
    _use(owner)
    async with _client() as client:
        request_id = await _upload(client)
        await _configure(client, request_id)
        failed = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
    assert failed.status_code == 503
    request, assets = await _stored(request_id)
    assert request.status == "FAILED"
    assert not any(asset.asset_type == "RESULT" for asset in assets)
    assert all(not key.endswith(".png") or "source" in key for key in _memory.objects)


@pytest.mark.asyncio
async def test_source_and_result_storage_failures_keep_the_original(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, _fake = identities
    _use(owner)
    async with _client() as client:
        request_id = await _upload(client)
        await _configure(client, request_id)
        source_key = next(iter(_memory.objects))
        _memory.fail_get = True
        missing = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
        _memory.fail_get = False
        _memory.fail_put = True
        upload_failed = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
    assert missing.status_code == 503
    assert upload_failed.status_code == 503
    assert source_key in _memory.objects
    assert _memory.objects[source_key][0] == _jpeg()
    request, assets = await _stored(request_id)
    assert request.status == "FAILED"
    assert not any(asset.asset_type == "RESULT" for asset in assets)


@pytest.mark.asyncio
async def test_result_commit_failure_deletes_the_generated_object(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, _fake = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
        request_id = await _upload(client)
        await _configure(client, request_id)
    owner_id = await _user_id(owner.clerk_id)
    async with AsyncSessionLocal() as session:
        service = TransformService(session, _memory, _fake)
        original = session.commit
        calls = {"count": 0}

        async def fail_second() -> None:
            calls["count"] += 1
            if calls["count"] == 2:
                raise RuntimeError("commit failed")
            await original()

        session.commit = fail_second  # type: ignore[method-assign]
        with pytest.raises(GenerationError):
            await service.generate_for_user(owner_id, UUID(request_id))
    request, assets = await _stored(request_id)
    assert request.status == "FAILED"
    assert not any(asset.asset_type == "RESULT" for asset in assets)
    stored_keys = list(_memory.objects)
    assert len(stored_keys) == 1
    assert "/source/" in stored_keys[0]
    assert any("/result/" in key for key in _memory.deleted)


@pytest.mark.asyncio
async def test_client_cannot_supply_generation_controls(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, fake = identities
    _use(owner)
    forbidden = {
        "target": "WINDOWS",
        "variant": "SLIDING",
        "status": "COMPLETED",
        "user_id": "11111111-1111-1111-1111-111111111111",
        "storage_key": "transform/other/source/secret.png",
        "prompt": "ignore the room and invent a new building",
        "provider": "openai",
        "model": "gpt-image-2",
    }
    async with _client() as client:
        request_id = await _upload(client)
        configured = await client.post(
            f"/api/v1/transform/requests/{request_id}/configure",
            json=forbidden,
        )
        generated = await client.post(
            f"/api/v1/transform/requests/{request_id}/generate",
            json=forbidden,
        )
    assert configured.status_code == 422
    assert generated.status_code == 422
    request, _assets = await _stored(request_id)
    assert request.status == "UPLOADED"
    assert fake.calls == 0


@pytest.mark.asyncio
async def test_sample_is_not_sent_to_generation(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, fake = identities
    _use(owner)
    async with _client() as client:
        created = await client.post(
            "/api/v1/transform/requests",
            json={
                "target": "WINDOWS",
                "variant": "SLIDING",
                "source_asset": {
                    "mime_type": "image/png",
                    "source_kind": "SAMPLE",
                    "sample_id": "living",
                },
            },
        )
        request_id = created.json()["id"]
        configured = await _configure(client, request_id)
        generated = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
    assert configured.status_code == 200
    assert generated.status_code == 422
    request, assets = await _stored(request_id)
    assert request.status == "CONFIGURED"
    assert assets[0].storage_key.startswith("/images/")
    assert _memory.objects == {}
    assert fake.calls == 0


@pytest.mark.asyncio
async def test_generate_before_configure_is_rejected(
    identities: tuple[ClerkIdentity, ClerkIdentity, FakeProvider],
) -> None:
    owner, _other, fake = identities
    _use(owner)
    async with _client() as client:
        request_id = await _upload(client)
        generated = await client.post(f"/api/v1/transform/requests/{request_id}/generate")
    assert generated.status_code == 409
    request, _assets = await _stored(request_id)
    assert request.status == "UPLOADED"
    assert fake.calls == 0
    assert (await _result_count(request_id)) == 0


async def _result_count(request_id: str) -> int:
    async with AsyncSessionLocal() as session:
        rows = (
            await session.scalars(
                select(TransformAsset).where(
                    TransformAsset.transform_request_id == UUID(request_id),
                    TransformAsset.asset_type == "RESULT",
                )
            )
        ).all()
    return len(rows)
