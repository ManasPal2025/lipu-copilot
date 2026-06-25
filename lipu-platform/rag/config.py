"""RAG ingestion and AI mode configuration."""

from __future__ import annotations

import os
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent
PLATFORM_ROOT = RAG_ROOT.parent

DOCUMENTS_DIR = PLATFORM_ROOT / "documents"
CHROMA_PERSIST_DIR = RAG_ROOT / "data" / "chroma"

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
