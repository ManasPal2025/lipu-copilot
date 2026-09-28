"""Object storage dependency."""

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.services.storage import ObjectStorage, build_object_storage


def get_object_storage(settings: Settings = Depends(get_settings)) -> ObjectStorage:
    return build_object_storage(settings)
