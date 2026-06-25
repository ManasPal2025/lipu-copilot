#!/usr/bin/env python3
"""
Benchmark RAG response latency — retrieval-only vs Gemini path.

Usage (from lipu-platform/rag/):
    python benchmark_ai.py
    python benchmark_ai.py --runs 5
"""

from __future__ import annotations

import argparse
import statistics
import sys
import time

from ai_mode import log_ai_mode
from config import AI_MODE, ENABLE_GEMINI

SAMPLE_QUESTIONS = [
    "Is double glazing worth it in Bhubaneswar?",
    "Which window is best for my balcony?",
    "How much noise reduction near NH16?",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Benchmark RAG latency")
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Timed runs per question after warm-up (default: 3)",
    )
    parser.add_argument(
        "--warmup",
        type=int,
        default=1,
        help="Warm-up queries before timing (default: 1)",
    )
    return parser.parse_args()


def _percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(len(ordered) * pct))
    return ordered[index]


def _run_timed(question: str) -> tuple[float, str]:
    from chain import rag_query

    start = time.perf_counter()
    result = rag_query(question)
    elapsed = time.perf_counter() - start
    return elapsed, result.mode


def _bench_label() -> str:
    return "Gemini (retrieval + LLM)" if ENABLE_GEMINI else "Retrieval-only (current config)"


def _print_stats(label: str, times: list[float]) -> None:
    print(f"\n{label}")
    print("-" * len(label))
    print(f"  Runs:     {len(times)}")
    print(f"  Mean:     {statistics.mean(times):.3f}s")
    print(f"  Median:   {statistics.median(times):.3f}s")
    print(f"  Min:      {min(times):.3f}s")
    print(f"  Max:      {max(times):.3f}s")
    print(f"  P95:      {_percentile(times, 0.95):.3f}s")
    under_3 = sum(1 for t in times if t < 3.0)
    print(f"  < 3s:     {under_3}/{len(times)} ({100 * under_3 / len(times):.0f}%)")


def main() -> int:
    args = parse_args()
    log_ai_mode()

    print(f"Config AI_MODE={AI_MODE!r}  ENABLE_GEMINI={ENABLE_GEMINI}")
    print(f"Sample questions: {len(SAMPLE_QUESTIONS)}")

    from chain import rag_query  # noqa: F401 — load stack

    for _ in range(args.warmup):
        rag_query(SAMPLE_QUESTIONS[0])

    print("\nWarm-up complete — embedding model loaded.")

    times: list[float] = []
    modes: set[str] = set()

    for question in SAMPLE_QUESTIONS:
        for _ in range(args.runs):
            elapsed, mode = _run_timed(question)
            times.append(elapsed)
            modes.add(mode)

    _print_stats(_bench_label(), times)
    print(f"\n  Answer modes observed: {', '.join(sorted(modes))}")

    print("\nComparison notes")
    print("-" * 16)
    print("  Retrieval-only: Chroma + local BGE embeddings — no external API calls.")
    print("  Gemini path:    adds network round-trip + LLM latency (typically 2–8s+).")
    if not ENABLE_GEMINI:
        print("\n  Gemini path is OFF (AI_MODE='retrieval'). To benchmark Gemini, set AI_MODE='gemini' in config.py.")
    if statistics.median(times) < 3.0:
        print("\n  Result: median latency meets sub-3s goal for retrieval-only mode.")
    else:
        print("\n  Result: median latency exceeds 3s — first-run model load may dominate; re-run after warm-up.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
