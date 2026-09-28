"""Checks that must pass before the API serves a production environment.

The messages name configuration, never secret values.
"""

from app.core.config import Settings


def production_blockers(settings: Settings) -> list[str]:
    """Return human-readable production configuration problems."""

    problems: list[str] = []
    if settings.debug:
        problems.append("DEBUG must be false.")
    if not settings.clerk_secret_key.startswith("sk_") or "YOUR" in settings.clerk_secret_key.upper():
        problems.append("CLERK_SECRET_KEY must be the production Clerk secret.")
    if _unsafe_origins(settings.cors_origins):
        problems.append("CORS_ORIGINS must list explicit https origins for the Ecotech site.")
    if _unsafe_origins(settings.clerk_authorized_parties):
        problems.append("CLERK_AUTHORIZED_PARTIES must list the production site origin.")
    if not settings.allowed_hosts or "*" in settings.allowed_hosts or set(settings.allowed_hosts) <= {
        "localhost",
        "127.0.0.1",
    }:
        problems.append("ALLOWED_HOSTS must name the production API host.")
    if "lipu_password_dev" in str(settings.database_url):
        problems.append("DATABASE_URL must not use the local development password.")
    if not settings.database_ssl:
        problems.append("DATABASE_SSL must be true.")
    if settings.storage_enabled:
        if not settings.storage_access_key or not settings.storage_secret_key:
            problems.append("STORAGE_ACCESS_KEY and STORAGE_SECRET_KEY are required.")
        elif settings.storage_access_key == settings.storage_secret_key:
            problems.append("STORAGE_ACCESS_KEY and STORAGE_SECRET_KEY must be different values.")
        if settings.storage_public_base_url:
            problems.append("STORAGE_PUBLIC_BASE_URL must stay empty so objects remain private.")
    if settings.image_generation_enabled and not settings.openai_api_key:
        problems.append("OPENAI_API_KEY is required when image generation is enabled.")
    return problems


def _unsafe_origins(origins: list[str]) -> bool:
    if not origins:
        return True
    for origin in origins:
        lowered = origin.lower()
        if origin == "*" or lowered == "null":
            return True
        if not lowered.startswith("https://"):
            return True
        if "localhost" in lowered or "127.0.0.1" in lowered:
            return True
    return False
