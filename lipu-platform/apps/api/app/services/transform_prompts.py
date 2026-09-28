"""Server-owned visualization instructions. The browser never supplies a prompt."""

PROMPT_VERSION = "v1"

_TARGETS = {
    "WINDOWS": "premium slim-profile aluminium windows",
    "DOORS": "premium aluminium doors",
    "BALCONY": "a premium glazed balcony enclosure",
    "TERRACE": "premium terrace glazing",
    "OUTDOOR": "premium outdoor glazed openings",
}

_VARIANTS = {
    "SLIDING": "sliding panels",
    "CASEMENT": "casement sashes",
    "LARGE_OPENING": "a large opening system",
    "BIFOLD": "bifold panels",
    "FRENCH": "French doors",
}

_ALLOWED_VARIANTS = {
    "WINDOWS": {"SLIDING", "CASEMENT", "LARGE_OPENING"},
    "DOORS": {"SLIDING", "BIFOLD", "FRENCH"},
    "BALCONY": set(),
    "TERRACE": set(),
    "OUTDOOR": set(),
}


def variants_match(target: str, variant: str | None) -> bool:
    """Return whether this opening type belongs to the selected target."""

    allowed = _ALLOWED_VARIANTS.get(target)
    if allowed is None:
        return False
    if not allowed:
        return variant is None
    return variant in allowed


def build_transform_prompt(target: str, variant: str | None) -> tuple[str, str]:
    """Return a versioned instruction that keeps the customer's architecture."""

    treatment = _TARGETS[target]
    if variant is not None:
        treatment = f"{treatment} with {_VARIANTS[variant]}"
    prompt = (
        "Edit this photograph into a realistic premium architectural visualization. "
        "Preserve the existing room or building, camera perspective, proportions, "
        "and major architectural elements. "
        f"Change only the requested opening treatment to {treatment}. "
        "Do not move or redesign unrelated furniture, walls, flooring, ceiling, "
        "landscaping, or lighting. Keep the result photorealistic."
    )
    return prompt, PROMPT_VERSION
