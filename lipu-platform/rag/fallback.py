"""Format retrieval-only answers when Gemini is unavailable."""

from __future__ import annotations

import re
from dataclasses import dataclass

from langchain_core.documents import Document

from config import FALLBACK_TOP_K

FALLBACK_INTRO = (
    "Based on our UPVC knowledge base, here are the most relevant recommendations."
)

_BOLD = re.compile(r"\*\*(.+?)\*\*")


@dataclass(frozen=True)
class SourceRef:
    id: str
    name: str
    label: str
    title: str
    section: str
    category: str
    score: float


def _plain(text: str) -> str:
    return _BOLD.sub(r"\1", text).strip()


def _source_id(meta: dict) -> str:
    return meta.get("id") or meta.get("source") or "unknown"


def _source_display_name(meta: dict) -> str:
    title = (meta.get("title") or "").strip()
    if title:
        return title

    doc_id = _source_id(meta)
    if doc_id == "unknown":
        return "Knowledge base"

    slug = doc_id.split("/")[-1]
    return slug.replace("-", " ").title()


def _source_label(meta: dict) -> str:
    parts: list[str] = []
    if meta.get("title"):
        parts.append(meta["title"])
    section = meta.get("section_title") or meta.get("header_2")
    if section and section not in parts:
        parts.append(section)
    if not parts:
        parts.append(_source_id(meta))
    return " — ".join(parts)


def build_sources(chunks: list[tuple[Document, float]], top_n: int = FALLBACK_TOP_K) -> list[SourceRef]:
    sources: list[SourceRef] = []
    seen: set[str] = set()

    for doc, score in chunks:
        meta = doc.metadata
        doc_id = _source_id(meta)
        if doc_id in seen:
            continue
        seen.add(doc_id)
        sources.append(
            SourceRef(
                id=doc_id,
                name=_source_display_name(meta),
                label=_source_label(meta),
                title=meta.get("title") or "",
                section=meta.get("section_title") or meta.get("header_2") or "",
                category=meta.get("category") or "",
                score=round(score, 4),
            ),
        )
        if len(sources) >= top_n:
            break

    return sources


def format_fallback_answer(
    question: str,
    chunks: list[tuple[Document, float]],
    *,
    top_n: int = FALLBACK_TOP_K,
) -> tuple[str, list[SourceRef]]:
    del question  # retained for call-site clarity
    selected = chunks[:top_n]
    sources = build_sources(chunks, top_n=top_n)

    if not selected:
        return (
            "We could not find relevant information in our knowledge base for that question. "
            "Please try rephrasing, or contact our team for a consultation.",
            [],
        )

    sections: list[str] = [
        FALLBACK_INTRO,
        "",
    ]

    for index, (doc, _score) in enumerate(selected, start=1):
        content = _plain(doc.page_content)
        if not content:
            continue
        label = sources[index - 1].label if index <= len(sources) else f"Note {index}"
        sections.append(f"{index}. {label}")
        sections.append("")
        sections.append(content)
        sections.append("")

    return "\n".join(sections).strip(), sources
