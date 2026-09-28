"""Persist a signed-in customer's transform request."""

from collections.abc import AsyncIterator
from unittest.mock import patch
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete, select, text

from app.db.session import AsyncSessionLocal, engine
from app.dependencies.auth import get_optional_clerk_identity
from app.dependencies.storage import get_object_storage
from app.domain.identity import ClerkIdentity
from app.main import app
from app.models.transform import TransformAsset, TransformRequest, TransformResult
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.platform import TransformRequestSubmission
from app.services.storage import MemoryStorage
from app.services.transforms import SAMPLE_CATALOGUE, TransformService

_memory = MemoryStorage()


def _jpeg() -> bytes:
    return b"\xff\xd8\xff\xe0" + b"\x00" * 32


def _png() -> bytes:
    return b"\x89PNG\r\n\x1a\n" + b"\x00" * 32


def _webp() -> bytes:
    return b"RIFF" + b"\x00\x00\x00\x00" + b"WEBP" + b"\x00" * 16


async def _purge(clerk_id: str) -> None:
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User).where(User.clerk_id == clerk_id))
        if user is not None:
            request_ids = list(
                (
                    await session.scalars(
                        select(TransformRequest.id).where(TransformRequest.user_id == user.id)
                    )
                ).all()
            )
            if request_ids:
                await session.execute(
                    delete(TransformResult).where(
                        TransformResult.transform_request_id.in_(request_ids)
                    )
                )
                await session.execute(
                    delete(TransformAsset).where(TransformAsset.transform_request_id.in_(request_ids))
                )
                await session.execute(
                    delete(TransformRequest).where(TransformRequest.id.in_(request_ids))
                )
            await session.execute(delete(UserProfile).where(UserProfile.user_id == user.id))
            await session.execute(delete(User).where(User.id == user.id))
        await session.commit()


def _identity(name: str) -> ClerkIdentity:
    return ClerkIdentity(
        clerk_id=f"test_clerk_{uuid4().hex}",
        email=f"transform-save-{name}-{uuid4().hex}@example.com",
        first_name=name,
        last_name="Rao",
        avatar_url=None,
    )


def _use(identity: ClerkIdentity) -> None:
    async def current() -> ClerkIdentity:
        return identity

    app.dependency_overrides[get_optional_clerk_identity] = current


def _client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost")


def _sample(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "target": "WINDOWS",
        "variant": "SLIDING",
        "source_asset": {
            "mime_type": "image/png",
            "source_kind": "SAMPLE",
            "sample_id": "living",
        },
    }
    payload.update(overrides)
    return payload


async def _user_id(clerk_id: str) -> UUID:
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User).where(User.clerk_id == clerk_id))
        assert user is not None
        return user.id


async def _stored(request_id: str) -> tuple[TransformRequest, list[TransformAsset]]:
    async with AsyncSessionLocal() as session:
        request = await session.get(TransformRequest, UUID(request_id))
        assert request is not None
        assets = list(
            (
                await session.scalars(
                    select(TransformAsset).where(TransformAsset.transform_request_id == request.id)
                )
            ).all()
        )
        return request, assets


@pytest_asyncio.fixture
async def identities() -> AsyncIterator[tuple[ClerkIdentity, ClerkIdentity]]:
    global _memory
    owner = _identity("Asha")
    other = _identity("Meera")
    _memory = MemoryStorage()
    app.dependency_overrides[get_object_storage] = lambda: _memory
    try:
        yield owner, other
    finally:
        app.dependency_overrides.pop(get_optional_clerk_identity, None)
        app.dependency_overrides.pop(get_object_storage, None)
        await _purge(owner.clerk_id)
        await _purge(other.clerk_id)
        await engine.dispose()


@pytest.mark.asyncio
async def test_transform_create_requires_authentication() -> None:
    app.dependency_overrides.pop(get_optional_clerk_identity, None)
    async with _client() as client:
        response = await client.post("/api/v1/transform/requests", json=_sample())

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


@pytest.mark.asyncio
async def test_transform_create_rejects_an_invalid_session() -> None:
    app.dependency_overrides.pop(get_optional_clerk_identity, None)
    async with _client() as client:
        response = await client.post(
            "/api/v1/transform/requests",
            json=_sample(),
            headers={"Authorization": "Bearer not-a-session"},
        )

    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


@pytest.mark.asyncio
async def test_signed_in_customer_persists_a_sample_request(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, other = identities
    _use(owner)
    async with _client() as client:
        created = await client.post("/api/v1/transform/requests", json=_sample())
        assert created.status_code == 201
        history = await client.get("/api/v1/transform/requests/me")
        _use(other)
        await client.get("/api/v1/users/me")
        hidden = await client.get("/api/v1/transform/requests/me")

    body = created.json()
    assert set(body) == {"id", "created_at", "target", "variant", "status"}
    assert body["target"] == "WINDOWS"
    assert body["variant"] == "SLIDING"
    assert body["status"] == "UPLOADED"
    assert "user_id" not in body
    assert "storage_key" not in created.text
    assert _memory.objects == {}

    request, assets = await _stored(body["id"])
    owner_id = await _user_id(owner.clerk_id)
    assert request.user_id == owner_id
    assert request.status == "UPLOADED"
    assert len(assets) == 1
    assert assets[0].asset_type == "SOURCE"
    assert assets[0].mime_type == "image/png"
    assert assets[0].storage_key == SAMPLE_CATALOGUE["living"]
    assert "base64" not in assets[0].storage_key
    assert not assets[0].storage_key.startswith("data:")
    assert not assets[0].storage_key.startswith("blob:")

    mine = history.json()
    assert mine["total"] == 1
    assert mine["items"][0]["id"] == body["id"]
    assert mine["items"][0]["status"] == "UPLOADED"
    assert mine["items"][0]["source_asset"]["public_url"] == SAMPLE_CATALOGUE["living"]
    assert "storage_key" not in history.text
    assert "demo-catalogue" not in history.text
    assert hidden.json()["total"] == 0
    assert body["id"] not in hidden.text


@pytest.mark.asyncio
async def test_upload_stores_the_file_outside_postgres(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, other = identities
    _use(owner)
    files = {"file": ("../../secret room.jpg", _webp(), "image/webp")}
    data = {"target": "DOORS", "variant": "FRENCH", "source_kind": "UPLOAD", "user_id": "ignored", "status": "COMPLETED"}
    async with _client() as client:
        created = await client.post("/api/v1/transform/requests", data=data, files=files)
        history = await client.get("/api/v1/transform/requests/me")
        _use(other)
        await client.get("/api/v1/users/me")
        hidden = await client.get("/api/v1/transform/requests/me")

    assert created.status_code == 201
    body = created.json()
    assert body["status"] == "UPLOADED"
    assert body["target"] == "DOORS"
    assert body["variant"] == "FRENCH"
    assert "storage_key" not in body
    request, assets = await _stored(body["id"])
    owner_id = await _user_id(owner.clerk_id)
    assert request.user_id == owner_id
    assert request.status == "UPLOADED"
    key = assets[0].storage_key
    assert key.startswith(f"transform/{owner_id}/{request.id}/source/")
    assert key.endswith(".webp")
    assert "secret" not in key
    assert assets[0].mime_type == "image/webp"
    assert assets[0].asset_type == "SOURCE"
    assert _memory.objects[key][0] == _webp()
    assert "bytea" not in await _column_types()
    item = history.json()["items"][0]
    assert item["source_asset"]["public_url"].startswith("https://storage.test/signed/")
    assert key not in history.text
    assert hidden.json()["total"] == 0
    assert item["source_asset"]["public_url"] not in hidden.text


async def _column_types() -> list[str]:
    async with AsyncSessionLocal() as session:
        return list(
            (
                await session.execute(
                    text(
                        "SELECT data_type FROM information_schema.columns "
                        "WHERE table_name = 'transform_assets'"
                    )
                )
            ).scalars().all()
        )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("payload", "mime", "extension"),
    [
        (_jpeg, "image/jpeg", "jpg"),
        (_png, "image/png", "png"),
        (_webp, "image/webp", "webp"),
    ],
)
async def test_accepted_image_signatures(
    identities: tuple[ClerkIdentity, ClerkIdentity],
    payload,
    mime: str,
    extension: str,
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        response = await client.post(
            "/api/v1/transform/requests",
            data={"target": "WINDOWS", "variant": "SLIDING", "source_kind": "UPLOAD"},
            files={"file": (f"room.{extension}", payload(), mime)},
        )
    assert response.status_code == 201
    _request, assets = await _stored(response.json()["id"])
    assert assets[0].mime_type == mime
    assert assets[0].storage_key.endswith(f".{extension}")


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "body",
    [
        b"<svg xmlns='http://www.w3.org/2000/svg'></svg>",
        b"GIF89a" + b"\x00" * 16,
        b"%PDF-1.4",
        b"not-an-image",
    ],
)
async def test_rejected_file_types(
    identities: tuple[ClerkIdentity, ClerkIdentity],
    body: bytes,
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        response = await client.post(
            "/api/v1/transform/requests",
            data={"target": "WINDOWS", "source_kind": "UPLOAD"},
            files={"file": ("file.bin", body, "application/octet-stream")},
        )
    assert response.status_code == 422
    assert "Traceback" not in response.text
    assert _memory.objects == {}


@pytest.mark.asyncio
async def test_oversized_upload_is_rejected(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    blob = _jpeg() + b"\x00" * (10 * 1024 * 1024)
    async with _client() as client:
        response = await client.post(
            "/api/v1/transform/requests",
            data={"target": "WINDOWS", "source_kind": "UPLOAD"},
            files={"file": ("big.jpg", blob, "image/jpeg")},
        )
    assert response.status_code == 413
    assert "Traceback" not in response.text
    assert _memory.objects == {}


@pytest.mark.asyncio
async def test_json_upload_without_a_file_is_rejected(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        response = await client.post(
            "/api/v1/transform/requests",
            json={
                "target": "DOORS",
                "variant": "FRENCH",
                "source_asset": {"mime_type": "image/webp", "source_kind": "UPLOAD"},
            },
        )
    assert response.status_code == 422
    assert _memory.objects == {}


@pytest.mark.asyncio
async def test_storage_failure_rolls_back_the_request(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    _memory.fail_put = True
    async with _client() as client:
        response = await client.post(
            "/api/v1/transform/requests",
            data={"target": "WINDOWS", "variant": "CASEMENT", "source_kind": "UPLOAD"},
            files={"file": ("room.jpg", _jpeg(), "image/jpeg")},
        )
    assert response.status_code == 503
    assert "Traceback" not in response.text
    owner_id = await _user_id(owner.clerk_id)
    async with AsyncSessionLocal() as session:
        rows = (
            await session.scalars(select(TransformRequest.id).where(TransformRequest.user_id == owner_id))
        ).all()
    assert rows == []
    assert _memory.objects == {}


@pytest.mark.asyncio
async def test_commit_failure_deletes_the_uploaded_object(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
    owner_id = await _user_id(owner.clerk_id)
    payload = TransformRequestSubmission.model_validate(
        {
            "target": "WINDOWS",
            "variant": "SLIDING",
            "source_asset": {"mime_type": "image/jpeg", "source_kind": "UPLOAD"},
        }
    )
    async with AsyncSessionLocal() as session:
        service = TransformService(session, _memory)

        async def fail_commit() -> None:
            raise RuntimeError("commit failed")

        session.commit = fail_commit  # type: ignore[method-assign]
        with pytest.raises(RuntimeError, match="commit failed"):
            await service.create_for_user(owner_id, payload, (_jpeg(), "image/jpeg"))
    assert _memory.objects == {}
    assert _memory.deleted
    async with AsyncSessionLocal() as session:
        rows = (
            await session.scalars(select(TransformRequest.id).where(TransformRequest.user_id == owner_id))
        ).all()
    assert rows == []


@pytest.mark.asyncio
async def test_client_cannot_set_owner_or_status(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, other = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
        _use(other)
        await client.get("/api/v1/users/me")
        _use(owner)
        response = await client.post(
            "/api/v1/transform/requests",
            json={
                **_sample(),
                "user_id": str(await _user_id(other.clerk_id)),
                "status": "COMPLETED",
            },
        )

    assert response.status_code == 422
    owner_id = await _user_id(owner.clerk_id)
    other_id = await _user_id(other.clerk_id)
    async with AsyncSessionLocal() as session:
        owner_count = (
            await session.scalars(select(TransformRequest.id).where(TransformRequest.user_id == owner_id))
        ).all()
        other_count = (
            await session.scalars(select(TransformRequest.id).where(TransformRequest.user_id == other_id))
        ).all()
    assert owner_count == []
    assert other_count == []


@pytest.mark.asyncio
async def test_request_without_a_variant_is_saved(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        response = await client.post(
            "/api/v1/transform/requests",
            json=_sample(target="TERRACE", variant=None),
        )

    assert response.status_code == 201
    body = response.json()
    assert body["target"] == "TERRACE"
    assert body["variant"] is None
    assert body["status"] == "UPLOADED"


@pytest.mark.asyncio
async def test_failed_asset_insert_rolls_back_the_request(
    identities: tuple[ClerkIdentity, ClerkIdentity],
) -> None:
    owner, _other = identities
    _use(owner)
    async with _client() as client:
        await client.get("/api/v1/users/me")
    owner_id = await _user_id(owner.clerk_id)
    payload = TransformRequestSubmission.model_validate(_sample())

    with patch("app.services.transforms.TransformAsset", side_effect=RuntimeError("forced")):
        async with AsyncSessionLocal() as session:
            with pytest.raises(RuntimeError, match="forced"):
                await TransformService(session).create_for_user(owner_id, payload)

    async with AsyncSessionLocal() as session:
        requests = (
            await session.scalars(
                select(TransformRequest.id).where(TransformRequest.user_id == owner_id)
            )
        ).all()
        assets = (
            await session.scalars(
                select(TransformAsset.id)
                .join(TransformRequest)
                .where(TransformRequest.user_id == owner_id)
            )
        ).all()
    assert requests == []
    assert assets == []
