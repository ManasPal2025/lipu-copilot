"""Retrieve relevant chunks from the local Chroma vector store."""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document

from config import CHROMA_PERSIST_DIR, COLLECTION_NAME, DEFAULT_TOP_K
from embeddings import create_embeddings, embed_query_text
from resources import get_embeddings, get_vector_store
from vectorstore import load_vector_store, search_by_vector_with_score


def retrieve(
    question: str,
    k: int = DEFAULT_TOP_K,
    *,
    persist_directory: Path | None = None,
    collection_name: str = COLLECTION_NAME,
) -> list[tuple[Document, float]]:
    """Return top-k chunks with similarity scores (lower = closer)."""
    if persist_directory is not None or collection_name != COLLECTION_NAME:
        embeddings = create_embeddings()
        store = load_vector_store(
            embeddings,
            persist_directory=persist_directory or CHROMA_PERSIST_DIR,
            collection_name=collection_name,
        )
    else:
        store = get_vector_store()
        embeddings = get_embeddings()

    search_query = embed_query_text(question.strip())
    query_vector = embeddings.embed_query(search_query)
    return search_by_vector_with_score(store, query_vector, k)
