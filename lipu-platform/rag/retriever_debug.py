"""Detailed retrieval instrumentation — logs to stderr when RAG_RETRIEVER_DEBUG=1."""

from __future__ import annotations

import os
import sys
import traceback
from dataclasses import dataclass, field

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import CHROMA_PERSIST_DIR, COLLECTION_NAME, DEFAULT_TOP_K, FALLBACK_TOP_K

DEBUG_RAW_K = 10


def is_enabled() -> bool:
    return os.getenv("RAG_RETRIEVER_DEBUG", "0").strip() in {"1", "true", "yes", "on"}


def _emit(line: str = "") -> None:
    print(line, file=sys.stderr, flush=True)


def _preview(text: str, limit: int = 100) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= limit:
        return collapsed
    return collapsed[: limit - 1] + "…"


def _meta_field(meta: dict, *keys: str) -> str:
    for key in keys:
        value = meta.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return "(missing)"


@dataclass
class SourceFilterDecision:
    rank: int
    doc_id: str
    source: str
    score: float
    kept: bool
    reason: str


@dataclass
class RetrievalDebugReport:
    question: str
    ingest_collection: str = COLLECTION_NAME
    retrieval_collection: str = COLLECTION_NAME
    persist_dir: str = str(CHROMA_PERSIST_DIR)
    vector_count: int = 0
    requested_k: int = DEFAULT_TOP_K
    raw_match_count: int = 0
    chunks_after_k_limit: int = 0
    score_threshold: str = "none"
    confidence_filter: str = "none (label only — does not drop chunks or sources)"
    retrieval_error: str | None = None
    source_decisions: list[SourceFilterDecision] = field(default_factory=list)
    sources_kept: int = 0
    sources_discarded: int = 0


def collection_vector_count(store: Chroma) -> int:
    return int(store._collection.count())  # noqa: SLF001


def collection_name(store: Chroma) -> str:
    return str(store._collection.name)  # noqa: SLF001


def simulate_source_filter(
    chunks: list[tuple[Document, float]],
    *,
    top_n: int = FALLBACK_TOP_K,
) -> list[SourceFilterDecision]:
    """Mirror build_sources() dedup logic and record keep/discard reasons."""
    decisions: list[SourceFilterDecision] = []
    seen: set[str] = set()
    kept_count = 0

    for rank, (doc, score) in enumerate(chunks, start=1):
        meta = doc.metadata
        doc_id = meta.get("id") or meta.get("source") or "unknown"
        source = _meta_field(meta, "source", "id")

        if doc_id in seen:
            decisions.append(
                SourceFilterDecision(
                    rank=rank,
                    doc_id=doc_id,
                    source=source,
                    score=score,
                    kept=False,
                    reason="duplicate document id (build_sources dedup)",
                ),
            )
            continue

        seen.add(doc_id)

        if kept_count >= top_n:
            decisions.append(
                SourceFilterDecision(
                    rank=rank,
                    doc_id=doc_id,
                    source=source,
                    score=score,
                    kept=False,
                    reason=f"over FALLBACK_TOP_K limit ({top_n})",
                ),
            )
            continue

        kept_count += 1
        decisions.append(
            SourceFilterDecision(
                rank=rank,
                doc_id=doc_id,
                source=source,
                score=score,
                kept=True,
                reason="unique document id within top_n",
            ),
        )

    return decisions


def log_retrieval_error(exc: BaseException) -> None:
    if not is_enabled():
        return
    _emit()
    _emit("[RETRIEVER] RETRIEVAL FAILED")
    _emit(f"  Exception = {type(exc).__name__}: {exc}")
    _emit("  Traceback:")
    for line in traceback.format_exc().strip().splitlines():
        _emit(f"    {line}")
    _emit()


def log_retrieval_report(report: RetrievalDebugReport, raw_chunks: list[tuple[Document, float]]) -> None:
    if not is_enabled():
        return

    _emit()
    _emit("[RETRIEVER]")
    _emit(f"Question = {report.question!r}")
    _emit(f"Collection Name (Chroma) = {report.retrieval_collection}")
    _emit(f"Collection Name (config / ingest default) = {report.ingest_collection}")
    _emit(f"Persist Dir = {report.persist_dir}")
    _emit(f"Vector Count = {report.vector_count}")
    _emit()
    _emit("Verification:")
    _emit(f"  1. Ingest collection name = {report.ingest_collection}")
    _emit(f"  2. Retrieval collection name = {report.retrieval_collection}")
    match = report.ingest_collection == report.retrieval_collection
    _emit(f"     Match = {'YES' if match else 'NO — possible mismatch'}")
    _emit(f"  3. Chroma raw matches (before k={report.requested_k} limit) = {report.raw_match_count}")
    _emit(f"  4. Score threshold applied = {report.score_threshold}")
    _emit(f"  5. Confidence filtering = {report.confidence_filter}")
    _emit()

    if report.retrieval_error:
        _emit(f"Retrieval error: {report.retrieval_error}")
        _emit()
        return

    _emit(f"Top {min(DEBUG_RAW_K, len(raw_chunks))} raw matches (L2 distance — lower = closer):")
    if not raw_chunks:
        _emit("  (none — Chroma returned zero documents)")
    else:
        for index, (doc, score) in enumerate(raw_chunks[:DEBUG_RAW_K], start=1):
            meta = doc.metadata
            _emit(f"  {index}. document id = {_meta_field(meta, 'id')}")
            _emit(f"     source = {_meta_field(meta, 'source')}")
            _emit(f"     score = {score:.4f}")
            _emit(f"     preview = {_preview(doc.page_content)!r}")
    _emit()

    _emit(f"After k-limit (keeping top {report.requested_k} retrieval chunks): {report.chunks_after_k_limit} chunks")
    _emit()
    _emit(f"After source filtering (build_sources dedup, max {FALLBACK_TOP_K} unique ids):")
    _emit(f"  sources kept = {report.sources_kept}")
    _emit(f"  sources discarded = {report.sources_discarded}")
    _emit()

    if report.source_decisions:
        for decision in report.source_decisions:
            status = "KEPT" if decision.kept else "DISCARDED"
            _emit(
                f"  rank {decision.rank} [{status}] id={decision.doc_id!r} "
                f"source={decision.source!r} score={decision.score:.4f} — {decision.reason}",
            )
    else:
        _emit("  (no chunks reached source filtering)")

    _emit()
