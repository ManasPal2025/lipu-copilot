"""Clerk identity resolved on the server. The browser never supplies this."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClerkIdentity:
    clerk_id: str
    email: str
    first_name: str | None
    last_name: str | None
    avatar_url: str | None
