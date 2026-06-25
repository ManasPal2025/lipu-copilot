"""Application-level singleton for embeddings and Chroma — load once, reuse all requests."""

from __future__ import annotations

import logging
import shutil
import threading
import time
from dataclasses import dataclass
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_PERSIST_DIR, COLLECTION_NAME, DOCUMENTS_DIR

logger = logging.getLogger(__name__)

INGEST_BATCH_SIZE = 50
INGEST_PROGRESS_INTERVAL = 50

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


def _persist_dir_has_sqlite(persist_dir: Path) -> bool:
    return persist_dir.is_dir() and (persist_dir / "chroma.sqlite3").is_file()


def _log_ingest_progress(processed: int, total: int) -> None:
    logger.info("[STARTUP] Vector store ingest progress: %d / %d chunks", processed, total)


def _create_vector_store_batched(
    embeddings: HuggingFaceEmbeddings,
    chunks: list[Document],
) -> Chroma:
    """Build Chroma in batches — same end state as create_vector_store(), startup-only."""
    persist_dir = CHROMA_PERSIST_DIR

    if persist_dir.exists():
        logger.info("[STARTUP] Removing existing vector store at %s", persist_dir)
        shutil.rmtree(persist_dir)

    persist_dir.mkdir(parents=True, exist_ok=True)

    total = len(chunks)
    processed = 0
    store: Chroma | None = None

    try:
        for start in range(0, total, INGEST_BATCH_SIZE):
            batch = chunks[start : start + INGEST_BATCH_SIZE]
            if store is None:
                store = Chroma.from_documents(
                    documents=batch,
                    embedding=embeddings,
                    collection_name=COLLECTION_NAME,
                    persist_directory=str(persist_dir),
                )
            else:
                store.add_documents(batch)

            processed += len(batch)
            if processed % INGEST_PROGRESS_INTERVAL == 0 or processed == total:
                _log_ingest_progress(processed, total)

        if store is None:
            raise RuntimeError("No chunks were ingested into the vector store")

        count = store._collection.count()  # noqa: SLF001
        logger.info(
            "[STARTUP] Vector store ready — collection=%r persist_dir=%s vectors=%d",
            COLLECTION_NAME,
            persist_dir,
            count,
        )
        return store
    except Exception:
        logger.exception(
            "[STARTUP] Vector store creation failed after %d / %d chunks (OOM or Chroma error)",
            processed,
            total,
        )
        raise


def _build_chroma_from_documents(embeddings: HuggingFaceEmbeddings) -> None:
    """Same pipeline as ingest.py — load, split, embed, persist (batched at startup)."""
    from loader import load_documents
    from splitter import split_documents

    doc_start = time.perf_counter()
    documents = load_documents(DOCUMENTS_DIR)
    document_load_ms = (time.perf_counter() - doc_start) * 1000
    logger.info(
        "[STARTUP] Document load time: %.0fms (%d documents)",
        document_load_ms,
        len(documents),
    )

    if not documents:
        raise RuntimeError(f"No documents to ingest. Check {DOCUMENTS_DIR}")

    chunk_start = time.perf_counter()
    chunks = split_documents(documents)
    chunk_generation_ms = (time.perf_counter() - chunk_start) * 1000
    logger.info(
        "[STARTUP] Chunk generation time: %.0fms (%d chunks)",
        chunk_generation_ms,
        len(chunks),
    )

    if not chunks:
        raise RuntimeError("No chunks produced after splitting")

    vector_store_start = time.perf_counter()
    _create_vector_store_batched(embeddings, chunks)
    vector_store_creation_ms = (time.perf_counter() - vector_store_start) * 1000
    logger.info("[STARTUP] Vector store creation time: %.0fms", vector_store_creation_ms)


def _load_or_build_vector_store(embeddings: HuggingFaceEmbeddings) -> Chroma:
    from vectorstore import load_vector_store

    if _persist_dir_has_sqlite(CHROMA_PERSIST_DIR):
        try:
            load_start = time.perf_counter()
            store = load_vector_store(embeddings)
            vector_store_load_ms = (time.perf_counter() - load_start) * 1000
            logger.info("[STARTUP] Chroma index found. Skipping ingest.")
            logger.info("[STARTUP] Vector store load time: %.0fms", vector_store_load_ms)
            return store
        except ValueError:
            logger.info("[STARTUP] Chroma index empty. Rebuilding from markdown documents...")
        except FileNotFoundError:
            logger.info("[STARTUP] Chroma index missing. Building from markdown documents...")
    else:
        logger.info("[STARTUP] Chroma index missing. Building from markdown documents...")

    _build_chroma_from_documents(embeddings)
    logger.info("[STARTUP] Ingest completed successfully.")
    return load_vector_store(embeddings)


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
        logger.info("[STARTUP] Embedding model load time: %.0fms", _init_embedding_ms)

        chroma_start = time.perf_counter()
        _store = _load_or_build_vector_store(_embeddings)
        _init_chroma_ms = (time.perf_counter() - chroma_start) * 1000
        logger.info("[STARTUP] Chroma initialization time: %.0fms", _init_chroma_ms)

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
