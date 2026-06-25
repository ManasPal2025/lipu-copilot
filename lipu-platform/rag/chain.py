"""RAG chain: retrieval-only or retrieval + Gemini (controlled by config.AI_MODE)."""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass, field
from typing import Literal

from langchain_core.documents import Document

from ai_mode import log_ai_mode
from config import DEFAULT_TOP_K, ENABLE_GEMINI, FALLBACK_TOP_K, GEMINI_MODEL
from confidence import compute_confidence
from fallback import SourceRef, build_sources, format_fallback_answer
from query_timing import QueryTimings, build_query_timings, retrieve_timed
from resources import get_init_timings, resources_initialized

logger = logging.getLogger(__name__)

AIMode = Literal["retrieval", "gemini"]

SYSTEM_PROMPT = """You are an experienced UPVC windows and doors consultant based in Bhubaneswar, Odisha.

Answer the homeowner's question using ONLY the context provided below.
- Be practical and technically accurate.
- Mention Odisha climate, monsoon, or coastal conditions when relevant.
- If the context does not contain enough information, say so clearly — do not invent specs or prices.
- Avoid sales language and exaggerated claims.
- Keep answers concise but complete (2–5 short paragraphs max)."""

RETRIEVAL_UNAVAILABLE = (
    "We could not search our knowledge base right now. "
    "Please try again in a moment, or contact our team for a consultation."
)


@dataclass
class RAGResult:
    question: str
    answer: str
    chunks: list[tuple[Document, float]] = field(default_factory=list)
    fallback: bool = False
    sources: list[SourceRef] = field(default_factory=list)
    confidence: str = "Low"
    mode: AIMode = "retrieval"

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "answer": self.answer,
            "fallback": self.fallback,
            "confidence": self.confidence,
            "mode": self.mode,
            "sources": [{"name": source.name, "id": source.id} for source in self.sources],
        }


def _format_context(chunks: list[tuple[Document, float]]) -> str:
    if not chunks:
        return "(No relevant documents found in the knowledge base.)"

    parts: list[str] = []
    for index, (doc, score) in enumerate(chunks, start=1):
        meta = doc.metadata
        label = meta.get("id") or meta.get("source") or f"chunk-{index}"
        title = meta.get("title", "")
        header = f"[Source {index}: {label}"
        if title:
            header += f" — {title}"
        header += f" | score={score:.4f}]"
        parts.append(f"{header}\n{doc.page_content.strip()}")

    return "\n\n---\n\n".join(parts)


def _retrieval_result(
    question: str,
    chunks: list[tuple[Document, float]],
    *,
    fallback: bool = False,
) -> RAGResult:
    answer, sources = format_fallback_answer(question, chunks)
    return RAGResult(
        question=question,
        answer=answer,
        chunks=chunks[:FALLBACK_TOP_K],
        fallback=fallback,
        sources=sources,
        confidence=compute_confidence(chunks),
        mode="retrieval",
    )


def _invoke_gemini(question: str, chunks: list[tuple[Document, float]], api_key: str) -> str:
    from langchain_google_genai import ChatGoogleGenerativeAI

    context = _format_context(chunks)
    user_message = f"""Context:
{context}

Question:
{question}"""

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=api_key,
        temperature=0.2,
    )
    response = llm.invoke(
        [
            ("system", SYSTEM_PROMPT),
            ("human", user_message),
        ],
    )
    content = response.content
    return content if isinstance(content, str) else str(content)


def _build_result(question: str, chunks: list[tuple[Document, float]]) -> RAGResult:
    if not chunks:
        return RAGResult(
            question=question,
            answer=RETRIEVAL_UNAVAILABLE,
            fallback=True,
            confidence="Low",
            mode="retrieval",
        )

    if not ENABLE_GEMINI:
        return _retrieval_result(question, chunks)

    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.warning("Gemini enabled but API key missing — using retrieval answer")
        return _retrieval_result(question, chunks, fallback=True)

    try:
        answer = _invoke_gemini(question, chunks, api_key).strip()
        if not answer:
            logger.warning("Gemini returned an empty response — using retrieval answer")
            return _retrieval_result(question, chunks, fallback=True)
    except Exception:
        logger.exception("Gemini call failed — using retrieval answer")
        return _retrieval_result(question, chunks, fallback=True)

    return RAGResult(
        question=question,
        answer=answer,
        chunks=chunks,
        fallback=False,
        sources=build_sources(chunks),
        confidence=compute_confidence(chunks),
        mode="gemini",
    )


def rag_query_profiled(question: str, k: int = DEFAULT_TOP_K) -> tuple[RAGResult, QueryTimings]:
    """Run RAG pipeline and return answer plus per-phase timings (milliseconds)."""
    log_ai_mode()

    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")

    wall_start = time.perf_counter()
    was_initialized = resources_initialized()

    query_embedding_ms = 0.0
    retrieval_ms = 0.0

    try:
        retrieved = retrieve_timed(question, k=k)
        chunks = retrieved.chunks
        query_embedding_ms = retrieved.query_embedding_ms
        retrieval_ms = retrieved.retrieval_ms
    except Exception as exc:
        logger.exception("Document retrieval failed")
        from retriever_debug import is_enabled, log_retrieval_error

        if is_enabled():
            log_retrieval_error(exc)
        chunks = []

    format_start = time.perf_counter()
    result = _build_result(question, chunks)
    answer_format_ms = (time.perf_counter() - format_start) * 1000

    init = get_init_timings()
    timings = build_query_timings(
        wall_start=wall_start,
        was_initialized=was_initialized,
        init_embedding_ms=init.embedding_model_ms,
        init_chroma_ms=init.chroma_init_ms,
        query_embedding_ms=query_embedding_ms,
        retrieval_ms=retrieval_ms,
        answer_format_ms=answer_format_ms,
    )

    return result, timings


def rag_query(question: str, k: int = DEFAULT_TOP_K) -> RAGResult:
    """
    retrieval mode: Question → Chroma → format answer
    gemini mode:    Question → Chroma → Gemini → answer (retrieval fallback on failure)
    """
    result, _timings = rag_query_profiled(question, k=k)
    return result