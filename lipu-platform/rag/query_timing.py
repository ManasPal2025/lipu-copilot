"""Request lifecycle timing for RAG queries."""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field

from langchain_core.documents import Document

from config import DEFAULT_TOP_K


@dataclass
class QueryTimings:
    api_received_ms: float = 0.0
    embedding_model_load_ms: float = 0.0
    chroma_init_ms: float = 0.0
    query_embedding_ms: float = 0.0
    retrieval_ms: float = 0.0
    answer_format_ms: float = 0.0
    total_ms: float = 0.0
    embedding_loaded_per_request: bool = False
    chroma_loaded_per_request: bool = False
    vector_store_opened_per_request: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RetrieveTimings:
    query_embedding_ms: float = 0.0
    retrieval_ms: float = 0.0
    total_ms: float = 0.0
    chunks: list[tuple[Document, float]] = field(default_factory=list)


def retrieve_timed(question: str, k: int = DEFAULT_TOP_K) -> RetrieveTimings:
    from embeddings import embed_query_text
    from resources import get_embeddings, get_vector_store
    from retriever_debug import (
        DEBUG_RAW_K,
        RetrievalDebugReport,
        collection_name,
        collection_vector_count,
        is_enabled,
        log_retrieval_report,
        simulate_source_filter,
    )
    from vectorstore import search_by_vector_with_score

    total_start = time.perf_counter()
    debug = is_enabled()

    store = get_vector_store()
    embeddings = get_embeddings()

    embed_start = time.perf_counter()
    search_query = embed_query_text(question.strip())
    query_vector = embeddings.embed_query(search_query)
    query_embedding_ms = (time.perf_counter() - embed_start) * 1000

    retrieval_start = time.perf_counter()
    raw_k = max(k, DEBUG_RAW_K) if debug else k
    raw_chunks = search_by_vector_with_score(store, query_vector, raw_k)
    chunks = raw_chunks[:k]
    retrieval_ms = (time.perf_counter() - retrieval_start) * 1000

    if debug:
        source_decisions = simulate_source_filter(chunks)
        kept = sum(1 for item in source_decisions if item.kept)
        discarded = sum(1 for item in source_decisions if not item.kept)
        log_retrieval_report(
            RetrievalDebugReport(
                question=question.strip(),
                retrieval_collection=collection_name(store),
                vector_count=collection_vector_count(store),
                requested_k=k,
                raw_match_count=len(raw_chunks),
                chunks_after_k_limit=len(chunks),
                source_decisions=source_decisions,
                sources_kept=kept,
                sources_discarded=discarded,
            ),
            raw_chunks,
        )

    return RetrieveTimings(
        query_embedding_ms=query_embedding_ms,
        retrieval_ms=retrieval_ms,
        total_ms=(time.perf_counter() - total_start) * 1000,
        chunks=chunks,
    )


def build_query_timings(
    *,
    wall_start: float,
    was_initialized: bool,
    init_embedding_ms: float,
    init_chroma_ms: float,
    query_embedding_ms: float,
    retrieval_ms: float,
    answer_format_ms: float,
) -> QueryTimings:
    embedding_per_request = not was_initialized and init_embedding_ms > 0
    chroma_per_request = not was_initialized and init_chroma_ms > 0

    return QueryTimings(
        embedding_model_load_ms=init_embedding_ms if not was_initialized else 0.0,
        chroma_init_ms=init_chroma_ms if not was_initialized else 0.0,
        query_embedding_ms=query_embedding_ms,
        retrieval_ms=retrieval_ms,
        answer_format_ms=answer_format_ms,
        total_ms=(time.perf_counter() - wall_start) * 1000,
        embedding_loaded_per_request=embedding_per_request,
        chroma_loaded_per_request=chroma_per_request,
        vector_store_opened_per_request=chroma_per_request,
    )
