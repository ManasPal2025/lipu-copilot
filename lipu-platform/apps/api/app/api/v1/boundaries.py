"""Client-independent API boundaries.

These paths are the contract for web, Android, and iOS. Route handlers are
intentionally not mounted in this foundation task.
"""

API_BOUNDARIES: dict[str, tuple[str, ...]] = {
    "auth": ("/api/v1/auth",),
    "users": ("/api/v1/users", "/api/v1/users/me"),
    "leads": ("/api/v1/leads",),
    "consultations": ("/api/v1/consultations",),
    "projects": ("/api/v1/projects",),
    "products": ("/api/v1/products", "/api/v1/product-interests"),
    "transform": ("/api/v1/transform/requests",),
    "conversations": ("/api/v1/conversations",),
}
