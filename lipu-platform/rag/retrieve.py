#!/usr/bin/env python3
"""
Retrieval test — top-k chunks for a user question (no LLM).

Usage (from lipu-platform/rag/):
    python retrieve.py "What glass works best for coastal homes in Puri?"
    python retrieve.py -k 5 "How long is the warranty?"
    python retrieve.py                              # interactive prompt
"""

from __future__ import annotations

import argparse
import sys
import textwrap

from config import CHROMA_PERSIST_DIR, COLLECTION_NAME
from embeddings import create_embeddings, embed_query_text
from vectorstore import load_vector_store

DEFAULT_TOP_K = 5
SEPARATOR = "-" * 72


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Retrieve top document chunks from local Chroma (no LLM)",
    )
    parser.add_argument(
        "question",
        nargs="?",
        help="User question to search for",
    )
    parser.add_argument(
        "-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of chunks to return (default: {DEFAULT_TOP_K})",
    )
    parser.add_argument(
        "--persist-dir",
        default=str(CHROMA_PERSIST_DIR),
        help="Chroma persistence directory",
    )
    parser.add_argument(
        "--collection",
        default=COLLECTION_NAME,
        help="Chroma collection name",
    )
    return parser.parse_args()


def _meta_line(metadata: dict) -> str:
    parts = [
        metadata.get("id") or metadata.get("source", "unknown"),
        metadata.get("category", ""),
        metadata.get("section_title") or metadata.get("header_2") or "",
    ]
    return " | ".join(p for p in parts if p)


def print_results(question: str, results: list[tuple], top_k: int) -> None:
    print(SEPARATOR)
    print(f"Question: {question}")
    print(f"Top {min(len(results), top_k)} chunks (lower score = closer match)")
    print(SEPARATOR)

    if not results:
        print("No results found.")
        return

    for rank, (doc, score) in enumerate(results[:top_k], start=1):
        meta = doc.metadata
        print(f"\n[{rank}] score={score:.4f}  {_meta_line(meta)}")
        if meta.get("title"):
            print(f"    title: {meta['title']}")
        if meta.get("summary"):
            print(f"    summary: {meta['summary']}")
        print()
        wrapped = textwrap.fill(
            doc.page_content.strip(),
            width=70,
            initial_indent="    ",
            subsequent_indent="    ",
        )
        print(wrapped)
        print(SEPARATOR)


def main() -> int:
    args = parse_args()
    question = (args.question or input("Question: ")).strip()
    if not question:
        print("Error: question cannot be empty.", file=sys.stderr)
        return 1

    from pathlib import Path

    persist_dir = Path(args.persist_dir)

    print("Loading embedding model…", file=sys.stderr)
    embeddings = create_embeddings()

    print("Loading vector store…", file=sys.stderr)
    try:
        vectorstore = load_vector_store(
            embeddings,
            persist_directory=persist_dir,
            collection_name=args.collection,
        )
    except (FileNotFoundError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print("Searching…", file=sys.stderr)
    search_query = embed_query_text(question)
    results = vectorstore.similarity_search_with_score(search_query, k=args.k)
    print_results(question, results, args.k)
    return 0


if __name__ == "__main__":
    sys.exit(main())
