"""Image generation dependency."""

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.services.image_generation import ImageGenerationProvider, build_image_generation_provider


def get_image_generation_provider(
    settings: Settings = Depends(get_settings),
) -> ImageGenerationProvider:
    return build_image_generation_provider(settings)
