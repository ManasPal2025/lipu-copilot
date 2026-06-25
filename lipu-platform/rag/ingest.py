#!/usr/bin/env python3
"""
Ingest LIPU knowledge-base markdown into a local ChromaDB vector store.

Usage (from lipu-platform/rag/):
    python ingest.py
    python ingest.py --reset
    python ingest.py --documents ../documents
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from config import CHROMA_PERSIST_DIR, COLLECTION_NAME, DOCUMENTS_DIR
from embeddings import create_embeddings
from loader import load_documents
from splitter import split_documents
from vectorstore import create_vector_store

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger("ingest")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest LIPU documents into ChromaDB")
    parser.add_argument(
        "--documents",
        type=Path,
        default=DOCUMENTS_DIR,
        help=f"Path to markdown knowledge base (default: {DOCUMENTS_DIR})",
    )
    parser.add_argument(
        "--persist-dir",
        type=Path,
        default=CHROMA_PERSIST_DIR,
        help=f"Chroma persistence directory (default: {CHROMA_PERSIST_DIR})",
    )
    parser.add_argument(
        "--collection",
        default=COLLECTION_NAME,
        help=f"Chroma collection name (default: {COLLECTION_NAME})",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete existing local vector store before ingesting",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    logger.info("Loading documents from %s", args.documents)
    documents = load_documents(args.documents)
    if not documents:
        logger.error("No documents to ingest. Check %s", args.documents)
        return 1

    logger.info("Splitting documents into chunks")
    chunks = split_documents(documents)
    if not chunks:
        logger.error("No chunks produced after splitting")
        return 1

    logger.info("Loading embedding model (first run downloads weights)")
    embeddings = create_embeddings()

    logger.info("Building Chroma vector store")
    create_vector_store(
        chunks,
        embeddings,
        persist_directory=args.persist_dir,
        collection_name=args.collection,
        reset=args.reset,
    )

    logger.info(
        "Done — %d documents → %d chunks → %s",
        len(documents),
        len(chunks),
        args.persist_dir,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
