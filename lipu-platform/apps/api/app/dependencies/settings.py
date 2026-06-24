"""Settings dependency helpers."""

from app.core.config import Settings, get_settings


def get_app_settings() -> Settings:
    """Expose typed settings through FastAPI dependency injection."""

    return get_settings()

