"""Validate customer image uploads without trusting the browser MIME type alone."""

from app.core.exceptions import PayloadTooLargeError, UnprocessableError

_JPEG = b"\xff\xd8\xff"
_PNG = b"\x89PNG\r\n\x1a\n"
_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/webp": "webp",
}


def detect_image(data: bytes, declared: str | None, *, max_bytes: int) -> tuple[str, str]:
    """Return the MIME type and extension after checking size and file signature."""

    if len(data) > max_bytes:
        raise PayloadTooLargeError("Please choose an image under the size limit.")
    if not data:
        raise UnprocessableError("Please choose a JPG, PNG, or WebP image.")

    if data.startswith(b"RIFF") and len(data) >= 12 and data[8:12] == b"WEBP":
        mime = "image/webp"
    elif data.startswith(_JPEG):
        mime = "image/jpeg"
    elif data.startswith(_PNG):
        mime = "image/png"
    else:
        raise UnprocessableError("Please choose a JPG, PNG, or WebP image.")

    cleaned = (declared or "").split(";", 1)[0].strip().lower()
    if cleaned and cleaned not in {"application/octet-stream", mime}:
        raise UnprocessableError("Please choose a JPG, PNG, or WebP image.")
    return mime, _TYPES[mime]
