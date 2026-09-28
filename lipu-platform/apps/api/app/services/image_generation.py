"""Image generation providers. Service code depends on this interface, not a vendor SDK."""

from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import Protocol

import httpx

from app.core.config import Settings
from app.core.exceptions import GenerationError


@dataclass(frozen=True)
class GeneratedImage:
    """Normalized provider output. Vendor response objects stay inside the adapter."""

    data: bytes
    mime_type: str
    provider: str
    model: str


class ImageGenerationProvider(Protocol):
    name: str

    async def generate(
        self,
        *,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> GeneratedImage:
        """Return one generated image."""


class DisabledImageGenerationProvider:
    """Used when generation is turned off or credentials are missing."""

    name = "disabled"

    async def generate(
        self,
        *,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> GeneratedImage:
        raise GenerationError("Visualization is not available right now.", category="disabled")


class OpenAIImageGenerationProvider:
    """Edits the customer's private source through the OpenAI images API."""

    name = "openai"

    def __init__(self, settings: Settings) -> None:
        self._api_key = settings.openai_api_key
        self._model = settings.openai_image_model
        self._size = settings.openai_image_size
        self._quality = settings.openai_image_quality
        self._timeout = settings.openai_image_timeout_seconds

    async def generate(
        self,
        *,
        image_bytes: bytes,
        mime_type: str,
        prompt: str,
    ) -> GeneratedImage:
        if not self._api_key or not self._model:
            raise GenerationError("Visualization is not available right now.", category="disabled")
        extension = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}.get(
            mime_type, "png"
        )
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(
                    "https://api.openai.com/v1/images/edits",
                    headers={"Authorization": f"Bearer {self._api_key}"},
                    data={
                        "model": self._model,
                        "prompt": prompt,
                        "size": self._size,
                        "quality": self._quality,
                        "n": "1",
                        "output_format": "png",
                    },
                    files={"image": (f"source.{extension}", image_bytes, mime_type)},
                )
        except httpx.HTTPError as exc:
            raise GenerationError(category="provider") from exc
        if response.status_code >= 400:
            raise GenerationError(category="provider")
        return GeneratedImage(
            data=_decode_image(response),
            mime_type="image/png",
            provider=self.name,
            model=self._model,
        )


def _decode_image(response: httpx.Response) -> bytes:
    try:
        payload = response.json()
        encoded = payload["data"][0]["b64_json"]
        raw = base64.b64decode(encoded, validate=True)
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise GenerationError(category="invalid_result") from exc
    if not raw:
        raise GenerationError(category="invalid_result")
    return raw


def build_image_generation_provider(settings: Settings) -> ImageGenerationProvider:
    if not settings.image_generation_enabled:
        return DisabledImageGenerationProvider()
    if settings.image_generation_provider == "openai":
        return OpenAIImageGenerationProvider(settings)
    return DisabledImageGenerationProvider()
