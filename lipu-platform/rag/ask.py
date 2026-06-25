#!/usr/bin/env python3
"""
RAG Q&A — Question -> Retriever -> Gemini Flash -> Answer

Usage (from lipu-platform/rag/):
    set GOOGLE_API_KEY=your-key
    python ask.py "Is double glazing worth it in Bhubaneswar?"
    python ask.py --show-chunks "Which window for a road-facing bedroom?"
    python ask.py --retrieval-only "Is double glazing worth it in Bhubaneswar?"
    python ask.py
"""

from __future__ import annotations

import argparse
import sys
import textwrap

from dotenv import load_dotenv
from langchain_core.documents import Document

from config import DEFAULT_TOP_K

load_dotenv()

SEPARATOR = "-" * 72


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RAG Q&A with Gemini Flash (no memory)")
    parser.add_argument("question", nargs="?", help="Question to ask")
    parser.add_argument(
        "-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of chunks to retrieve (default: {DEFAULT_TOP_K})",
    )
    parser.add_argument(
        "--show-chunks",
        action="store_true",
        help="Print retrieved chunks before the answer",
    )
    parser.add_argument(
        "--retrieval-only",
        action="store_true",
        help="Retrieve and print chunks only — no Gemini call",
    )
    return parser.parse_args()


def _print_retrieval_results(question: str, chunks: list[tuple[Document, float]]) -> None:
    print(SEPARATOR)
    print(f"Question: {question}")
    print(f"Top {len(chunks)} chunks (lower score = closer match)")
    print(SEPARATOR)

    if not chunks:
        print("No results found.")
        print(SEPARATOR)
        return

    for index, (doc, score) in enumerate(chunks, start=1):
        meta = doc.metadata
        source = meta.get("id") or meta.get("source", "unknown")
        print(f"\n[{index}] score={score:.4f}")
        print(f"  source: {source}")
        if meta.get("category"):
            print(f"  category: {meta['category']}")
        section = meta.get("section_title") or meta.get("header_2")
        if section:
            print(f"  section: {section}")
        if meta.get("title"):
            print(f"  title: {meta['title']}")
        print()
        print(
            textwrap.fill(
                doc.page_content.strip(),
                width=70,
                initial_indent="  ",
                subsequent_indent="  ",
            ),
        )
        print(SEPARATOR)


def _print_sources(sources, confidence: str | None = None) -> None:
    if confidence:
        print(f"\nConfidence: {confidence}")
    if not sources:
        return
    print("\nSources:")
    for source in sources:
        print(f"  • {source.name}")


def main() -> int:
    args = parse_args()
    question = (args.question or input("Question: ")).strip()
    if not question:
        print("Error: question cannot be empty.", file=sys.stderr)
        return 1

    print("Retrieving context…", file=sys.stderr)
    try:
        if args.retrieval_only:
            from retriever import retrieve

            chunks = retrieve(question, k=args.k)
            _print_retrieval_results(question, chunks)
            return 0

        from chain import rag_query

        result = rag_query(question, k=args.k)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print("Run `python ingest.py --reset` first.", file=sys.stderr)
        return 1

    if args.show_chunks:
        _print_retrieval_results(result.question, result.chunks)

    if result.fallback:
        print("\nNote: showing knowledge base recommendations.\n", file=sys.stderr)

    print(f"\nQuestion: {result.question}\n")
    print(result.answer)
    _print_sources(result.sources, result.confidence)
    return 0


if __name__ == "__main__":
    sys.exit(main())
