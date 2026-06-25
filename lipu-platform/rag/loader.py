"""Load markdown knowledge-base documents with YAML frontmatter."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import yaml
from langchain_core.documents import Document

from config import DOCUMENTS_DIR, SKIP_FILENAMES, VALID_CATEGORIES

logger = logging.getLogger(__name__)


def _parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---"):
        raise ValueError("Missing YAML frontmatter")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Malformed frontmatter block")

    meta = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\n")
    return meta, body


def _flatten_metadata(meta: dict[str, Any], source: str) -> dict[str, str | int | float | bool]:
    """Chroma metadata values must be scalar types."""
    flat: dict[str, str | int | float | bool] = {"source": source}

    for key, value in meta.items():
        if value is None:
            continue
        if isinstance(value, (str, int, float, bool)):
            flat[key] = value
        elif isinstance(value, list):
            flat[key] = ", ".join(str(item) for item in value)
        else:
            flat[key] = str(value)

    return flat


def _should_skip(meta: dict[str, Any], path: Path) -> str | None:
    if path.name in SKIP_FILENAMES:
        return "template file"

    status = str(meta.get("status", "published")).lower()
    if status == "draft":
        return "draft status"

    doc_id = meta.get("id")
    category = meta.get("category")
    if not doc_id or not category:
        return "missing id or category"

    if category not in VALID_CATEGORIES:
        return f"invalid category: {category}"

    expected_prefix = f"{category}/"
    if not str(doc_id).startswith(expected_prefix):
        return f"id {doc_id!r} does not match category {category!r}"

    if path.parent.name != category:
        return f"file folder {path.parent.name!r} != category {category!r}"

    return None


def load_documents(documents_dir: Path | None = None) -> list[Document]:
    root = documents_dir or DOCUMENTS_DIR
    if not root.is_dir():
        raise FileNotFoundError(f"Documents directory not found: {root}")

    documents: list[Document] = []
    skipped = 0

    for path in sorted(root.rglob("*.md")):
        try:
            raw = path.read_text(encoding="utf-8")
            meta, body = _parse_frontmatter(raw)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            logger.warning("Skipping %s: %s", path.relative_to(root), exc)
            skipped += 1
            continue

        skip_reason = _should_skip(meta, path)
        if skip_reason:
            logger.info("Skipping %s (%s)", path.relative_to(root), skip_reason)
            skipped += 1
            continue

        if not body.strip():
            logger.warning("Skipping empty body: %s", path.relative_to(root))
            skipped += 1
            continue

        rel_source = str(path.relative_to(root)).replace("\\", "/")
        metadata = _flatten_metadata(meta, rel_source)

        # Prepend title and summary for richer embeddings
        title = meta.get("title", "")
        summary = meta.get("summary", "")
        prefix_parts = [p for p in (title, summary) if p]
        page_content = body
        if prefix_parts:
            page_content = f"{'. '.join(prefix_parts)}.\n\n{body}"

        documents.append(Document(page_content=page_content, metadata=metadata))

    logger.info("Loaded %d documents (%d skipped)", len(documents), skipped)
    return documents
