"""ChromaDB vector store creation with local persistence."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from config import CHROMA_PERSIST_DIR, COLLECTION_NAME

logger = logging.getLogger(__name__)


def create_vector_store(
    chunks: list[Document],
    embeddings: Embeddings,
    *,
    persist_directory: Path | None = None,
    collection_name: str = COLLECTION_NAME,
    reset: bool = False,
) -> Chroma:
    persist_dir = persist_directory or CHROMA_PERSIST_DIR

    if reset and persist_dir.exists():
        logger.info("Removing existing vector store at %s", persist_dir)
        shutil.rmtree(persist_dir)

    persist_dir.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=str(persist_dir),
    )

    count = vectorstore._collection.count()  # noqa: SLF001 — ingestion script diagnostics
    logger.info(
        "Vector store ready — collection=%r persist_dir=%s vectors=%d",
        collection_name,
        persist_dir,
        count,
    )
    return vectorstore


def load_vector_store(
    embeddings: Embeddings,
    *,
    persist_directory: Path | None = None,
    collection_name: str = COLLECTION_NAME,
) -> Chroma:
    """Load an existing persisted Chroma collection."""
    persist_dir = persist_directory or CHROMA_PERSIST_DIR
    if not persist_dir.is_dir():
        raise FileNotFoundError(
            f"Vector store not found at {persist_dir}. Run `python ingest.py` first.",
        )

    count_check = Chroma(
        persist_directory=str(persist_dir),
        embedding_function=embeddings,
        collection_name=collection_name,
    )
    count = count_check._collection.count()  # noqa: SLF001
    if count == 0:
        raise ValueError(f"Vector store at {persist_dir} is empty. Run `python ingest.py --reset`.")

    logger.info(
        "Loaded vector store — collection=%r persist_dir=%s vectors=%d",
        collection_name,
        persist_dir,
        count,
    )
    return count_check


def search_by_vector_with_score(
    store: Chroma,
    query_vector: list[float],
    k: int,
) -> list[tuple[Document, float]]:
    """Vector search returning L2 distance scores (lower = closer)."""
    result = store._collection.query(  # noqa: SLF001
        query_embeddings=[query_vector],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    documents = result.get("documents", [[]])[0]
    metadatas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]

    chunks: list[tuple[Document, float]] = []
    for text, meta, distance in zip(documents, metadatas, distances, strict=False):
        if text is None:
            continue
        chunks.append((Document(page_content=text, metadata=meta or {}), float(distance)))

    return chunks
