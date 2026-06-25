"""Map retrieval scores to user-facing confidence levels."""

from __future__ import annotations

from langchain_core.documents import Document

ConfidenceLevel = str  # "High" | "Medium" | "Low"


def compute_confidence(chunks: list[tuple[Document, float]]) -> ConfidenceLevel:
    """
    Estimate answer confidence from Chroma L2 distances (lower = closer match).
    Thresholds tuned for BGE-small-en-v1.5 on the LIPU knowledge base.
    """
    if not chunks:
        return "Low"

    top_score = chunks[0][1]
    top_three = [score for _, score in chunks[:3]]
    avg_top = sum(top_three) / len(top_three)

    if top_score <= 0.45 and avg_top <= 0.52:
        return "High"
    if top_score <= 0.58 and avg_top <= 0.68:
        return "Medium"
    return "Low"
