"""RAG ingestion and AI mode configuration."""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

RAG_ROOT = Path(__file__).resolve().parent
PLATFORM_ROOT = RAG_ROOT.parent

CHROMA_PERSIST_DIR = RAG_ROOT / "data" / "chroma"


def resolve_documents_dir() -> Path:
    """Prefer rag/documents (Railway deploy root); fall back to monorepo ../documents."""
    local_deployment = RAG_ROOT / "documents"
    monorepo = PLATFORM_ROOT / "documents"

    if local_deployment.is_dir():
        logger.info(
            "[DOCS] Using local deployment documents path: %s",
            local_deployment.resolve(),
        )
        return local_deployment

    logger.info("[DOCS] Using monorepo documents path: ../documents")
    return monorepo


DOCUMENTS_DIR = resolve_documents_dir()

COLLECTION_NAME = "lipu_knowledge"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
GEMINI_MODEL = "gemini-2.0-flash"
DEFAULT_TOP_K = 5
FALLBACK_TOP_K = 3

# ── AI mode (single switch) ───────────────────────────────────────────────
# Change only AI_MODE to switch behaviour:
#   "retrieval" — Chroma retrieval + formatted answer (default, offline-capable)
#   "gemini"    — Retrieval context → Gemini synthesis
AI_MODE = "retrieval"

ENABLE_GEMINI = AI_MODE == "gemini"

RAG_SERVER_HOST = "127.0.0.1"
RAG_SERVER_PORT = 8100

# Secondary split for oversized sections (chars ≈ 200–800 words)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

SKIP_FILENAMES = {"_template.md"}

VALID_CATEGORIES = frozenset({
    "catalog",
    "faq",
    "glass",
    "hardware",
    "warranty",
    "installation",
    "odisha-climate",
    "design-inspiration",
    "pricing-guide",
    "service-support",
})
