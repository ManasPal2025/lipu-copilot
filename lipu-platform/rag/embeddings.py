"""Embedding model factory."""

from __future__ import annotations

from langchain_huggingface import HuggingFaceEmbeddings

from config import EMBEDDING_MODEL


def create_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


# BGE retrieval query prefix (documents ingested without prefix)
BGE_QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def embed_query_text(question: str) -> str:
    return f"{BGE_QUERY_PREFIX}{question}"
