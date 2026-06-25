"""Application-level singleton for embeddings and Chroma — load once, reuse all requests."""

from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_embeddings: HuggingFaceEmbeddings | None = None
_store: Chroma | None = None
_initialized = False

_init_embedding_ms = 0.0
_init_chroma_ms = 0.0
_init_total_ms = 0.0


@dataclass(frozen=True)
class ResourceInitTimings:
    embedding_model_ms: float
    chroma_init_ms: float
    total_ms: float


def initialize_resources(*, warmup_embed: bool = True) -> ResourceInitTimings:
    """Load embedding model and Chroma vector store once per process."""
    global _embeddings, _store, _initialized
    global _init_embedding_ms, _init_chroma_ms, _init_total_ms

    with _lock:
        if _initialized:
            return ResourceInitTimings(
                embedding_model_ms=_init_embedding_ms,
                chroma_init_ms=_init_chroma_ms,
                total_ms=_init_total_ms,
            )

        total_start = time.perf_counter()

        embed_start = time.perf_counter()
        from embeddings import create_embeddings

        _embeddings = create_embeddings()
        if warmup_embed:
            _embeddings.embed_query("Represent this sentence for searching relevant passages: warmup")
        _init_embedding_ms = (time.perf_counter() - embed_start) * 1000

        chroma_start = time.perf_counter()
        from vectorstore import load_vector_store

        _store = load_vector_store(_embeddings)
        _init_chroma_ms = (time.perf_counter() - chroma_start) * 1000

        _init_total_ms = (time.perf_counter() - total_start) * 1000
        _initialized = True

        logger.info(
            "RAG resources ready — embedding=%.0fms chroma=%.0fms total=%.0fms",
            _init_embedding_ms,
            _init_chroma_ms,
            _init_total_ms,
        )

        return ResourceInitTimings(
            embedding_model_ms=_init_embedding_ms,
            chroma_init_ms=_init_chroma_ms,
            total_ms=_init_total_ms,
        )


def get_embeddings() -> HuggingFaceEmbeddings:
    if not _initialized:
        initialize_resources()
    assert _embeddings is not None
    return _embeddings


def get_vector_store() -> Chroma:
    if not _initialized:
        initialize_resources()
    assert _store is not None
    return _store


def resources_initialized() -> bool:
    return _initialized


def get_init_timings() -> ResourceInitTimings:
    return ResourceInitTimings(
        embedding_model_ms=_init_embedding_ms,
        chroma_init_ms=_init_chroma_ms,
        total_ms=_init_total_ms,
    )
