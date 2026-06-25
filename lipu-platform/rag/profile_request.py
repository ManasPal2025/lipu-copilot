#!/usr/bin/env python3
"""
Profile a single chatbot query lifecycle — subprocess vs persistent server.

Usage (from lipu-platform/rag/):
    python profile_request.py
    python profile_request.py --question "Is double glazing worth it?"
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAG_ROOT = Path(__file__).resolve().parent
DEFAULT_QUESTION = "Which window is best for my balcony?"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Profile RAG request lifecycle")
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    parser.add_argument("--server-url", default="http://127.0.0.1:8100")
    parser.add_argument("--skip-server", action="store_true", help="Skip server benchmark")
    return parser.parse_args()


def _python() -> Path:
    if sys.platform == "win32":
        return RAG_ROOT / ".venv" / "Scripts" / "python.exe"
    return RAG_ROOT / ".venv" / "bin" / "python"


def _print_timings(title: str, timings: dict, *, per_request: dict | None = None) -> None:
    print(f"\n{title}")
    print("=" * len(title))
    rows = [
        ("API request received", timings.get("api_received_ms", 0)),
        ("Embedding model load", timings.get("embedding_model_load_ms", 0)),
        ("ChromaDB initialization", timings.get("chroma_init_ms", 0)),
        ("Query embedding generation", timings.get("query_embedding_ms", 0)),
        ("Retrieval", timings.get("retrieval_ms", 0)),
        ("Answer formatting", timings.get("answer_format_ms", 0)),
        ("Total response time", timings.get("total_ms", 0)),
    ]
    for label, ms in rows:
        print(f"  {label:<30} {ms:>8.1f} ms")

    if per_request:
        print("\n  Resource loading per request:")
        for key, value in per_request.items():
            print(f"    {key}: {'YES' if value else 'no'}")


def profile_subprocess(question: str) -> dict:
    """Each call spawns a fresh Python process (legacy /api/chat path)."""
    python = _python()
    script = RAG_ROOT / "profile_subprocess.py"

    wall_start = time.perf_counter()
    proc = subprocess.run(
        [str(python), str(script), question],
        cwd=RAG_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    wall_ms = (time.perf_counter() - wall_start) * 1000

    if proc.returncode != 0:
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError(f"Subprocess profile failed (exit {proc.returncode})")

    payload = json.loads(proc.stdout)
    payload["timings_ms"]["api_received_ms"] = wall_ms
    payload["timings_ms"]["total_ms"] = wall_ms
    return payload


def profile_inprocess(question: str) -> dict:
    """Single process with application-level singleton (RAG server model)."""
    from chain import rag_query_profiled

    api_received = time.perf_counter()
    result, timings = rag_query_profiled(question)
    timings.api_received_ms = (time.perf_counter() - api_received) * 1000

    return {
        **result.to_dict(),
        "timings_ms": timings.to_dict(),
    }


def profile_server(question: str, server_url: str) -> dict | None:
    url = f"{server_url.rstrip('/')}/query?profile=1"
    body = json.dumps({"question": question}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    wall_start = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as exc:
        print(f"\nServer not reachable at {server_url} ({exc}).")
        print("Start it with: python server.py")
        return None

    wall_ms = (time.perf_counter() - wall_start) * 1000
    timings = payload.get("timings_ms", {})
    timings["api_received_ms"] = wall_ms
    timings["total_ms"] = wall_ms
    payload["timings_ms"] = timings
    return payload


def main() -> int:
    args = parse_args()
    question = args.question.strip()

    print(f"Question: {question}")

    print("\n--- FINDINGS (before warm server) ---")
    print("  Legacy path spawns a NEW Python process per /api/chat request.")
    print("  That reloads the embedding model and opens Chroma on every request.")

    sub = profile_subprocess(question)
    sub_timings = sub["timings_ms"]
    _print_timings(
        "A) Subprocess per request (legacy — cold process each time)",
        sub_timings,
        per_request={
            "embedding_model": sub_timings.get("embedding_loaded_per_request", True),
            "chromadb": sub_timings.get("chroma_loaded_per_request", True),
            "vector_store": sub_timings.get("vector_store_opened_per_request", True),
        },
    )

    warm_cold = profile_inprocess(question)
    warm_cold_timings = warm_cold["timings_ms"]
    _print_timings(
        "B) In-process first query (singleton — loads resources once)",
        warm_cold_timings,
        per_request={
            "embedding_model": warm_cold_timings.get("embedding_loaded_per_request", True),
            "chromadb": warm_cold_timings.get("chroma_loaded_per_request", True),
            "vector_store": warm_cold_timings.get("vector_store_opened_per_request", True),
        },
    )

    warm = profile_inprocess(question)
    warm_timings = warm["timings_ms"]
    _print_timings(
        "C) In-process warm query (singleton — resources reused)",
        warm_timings,
        per_request={
            "embedding_model": warm_timings.get("embedding_loaded_per_request", False),
            "chromadb": warm_timings.get("chroma_loaded_per_request", False),
            "vector_store": warm_timings.get("vector_store_opened_per_request", False),
        },
    )

    if not args.skip_server:
        server_payload = profile_server(question, args.server_url)
        if server_payload:
            server_timings = server_payload["timings_ms"]
            _print_timings(
                "D) Persistent RAG server HTTP request (resources pre-loaded at startup)",
                server_timings,
                per_request={
                    "embedding_model": server_timings.get("embedding_loaded_per_request", False),
                    "chromadb": server_timings.get("chroma_loaded_per_request", False),
                    "vector_store": server_timings.get("vector_store_opened_per_request", False),
                },
            )

    print("\n--- RECOMMENDATION ---")
    print("  Run `python server.py` alongside Next.js dev.")
    print("  Set RAG_SERVER_URL=http://127.0.0.1:8100 so /api/chat reuses warm resources.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
