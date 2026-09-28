"""Verify a Clerk session token with the official Clerk backend SDK.

Passwords are never accepted here. A bearer token is trusted only after Clerk
verifies its signature. Client-supplied user ids are not identities.
"""

from typing import Mapping

from clerk_backend_api import Clerk
from clerk_backend_api.security.types import AuthenticateRequestOptions, AuthStatus

from app.core.exceptions import UnauthorizedError
from app.core.logging import get_logger
from app.domain.identity import ClerkIdentity


logger = get_logger(__name__)


class _HeaderRequest:
    def __init__(self, headers: Mapping[str, str]) -> None:
        self.headers = headers


def _text(value: object, limit: int) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = " ".join(value.split())
    if not cleaned:
        return None
    return cleaned[:limit]


def _primary_email(user: object) -> str | None:
    addresses = getattr(user, "email_addresses", None) or []
    primary_id = getattr(user, "primary_email_address_id", None)
    chosen = None
    for address in addresses:
        if getattr(address, "id", None) == primary_id:
            chosen = address
            break
    if chosen is None and addresses:
        chosen = addresses[0]
    if chosen is None:
        return None
    email = getattr(chosen, "email_address", None)
    if not isinstance(email, str):
        return None
    return email.strip().lower()


async def verify_clerk_bearer(
    authorization: str,
    *,
    secret_key: str,
    authorized_parties: list[str],
) -> ClerkIdentity:
    """Return the Clerk user behind a bearer token, or reject the request."""

    if not secret_key:
        raise UnauthorizedError("Authentication is required.")

    try:
        async with Clerk(bearer_auth=secret_key) as clerk:
            state = await clerk.authenticate_request_async(
                _HeaderRequest({"Authorization": authorization}),
                AuthenticateRequestOptions(
                    secret_key=secret_key,
                    authorized_parties=authorized_parties or None,
                    accepts_token=["session_token"],
                ),
            )
            if state.status != AuthStatus.SIGNED_IN or not state.payload:
                raise UnauthorizedError("Authentication is required.")

            subject = state.payload.get("sub")
            if not isinstance(subject, str) or not subject.strip():
                raise UnauthorizedError("Authentication is required.")
            clerk_id = subject.strip()
            if len(clerk_id) > 255:
                raise UnauthorizedError("Authentication is required.")

            email = state.payload.get("email")
            first_name = state.payload.get("first_name") or state.payload.get("given_name")
            last_name = state.payload.get("last_name") or state.payload.get("family_name")
            avatar_url = state.payload.get("image_url")
            if not isinstance(email, str) or "@" not in email:
                clerk_user = await clerk.users.get_async(user_id=clerk_id)
                email = _primary_email(clerk_user)
                first_name = first_name or getattr(clerk_user, "first_name", None)
                last_name = last_name or getattr(clerk_user, "last_name", None)
                avatar_url = avatar_url or getattr(clerk_user, "image_url", None)
    except UnauthorizedError:
        raise
    except Exception as exc:
        logger.warning("Clerk verification failed", extra={"error_type": type(exc).__name__})
        raise UnauthorizedError("Authentication is required.") from None

    if not isinstance(email, str):
        raise UnauthorizedError("Authentication is required.")
    normalized = email.strip().lower()
    if "@" not in normalized or len(normalized) > 255:
        raise UnauthorizedError("Authentication is required.")

    return ClerkIdentity(
        clerk_id=clerk_id,
        email=normalized,
        first_name=_text(first_name, 100),
        last_name=_text(last_name, 100),
        avatar_url=_text(avatar_url, 500),
    )
