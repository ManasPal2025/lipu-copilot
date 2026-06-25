#!/usr/bin/env python3
"""
Run a retrieval with full [RETRIEVER] debug output.

Usage (from lipu-platform/rag/):
    python debug_retrieve.py "What is UPVC?"
    RAG_RETRIEVER_DEBUG=1 python debug_retrieve.py "What is UPVC?"
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("RAG_RETRIEVER_DEBUG", "1")

from chain import rag_query  # noqa: E402
from resources import initialize_resources  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Debug retrieval for a question")
    parser.add_argument("question", nargs="?", default="What is UPVC?")
    parser.add_argument("--json", action="store_true", help="Print API-shaped JSON to stdout")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    initialize_resources()
    result = rag_query(args.question)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"\nResult: {len(result.sources)} sources, confidence={result.confidence}")
        print(f"Answer preview: {result.answer[:200]}…")

    return 0


if __name__ == "__main__":
    sys.exit(main())
