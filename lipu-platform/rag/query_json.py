#!/usr/bin/env python3
"""JSON output for API integrations — stdout only, errors logged to stderr."""

from __future__ import annotations

import json
import logging
import sys

from dotenv import load_dotenv

from ai_mode import log_ai_mode
from config import AI_MODE

load_dotenv()

logging.basicConfig(
    level=logging.WARNING,
    stream=sys.stderr,
    format="%(levelname)s %(name)s — %(message)s",
)

logger = logging.getLogger(__name__)

GENERIC_ANSWER = (
    "We're having trouble answering right now. "
    "Please try again in a moment, or request a consultation and our team will help you directly."
)


def _generic_payload(question: str) -> dict:
    return {
        "question": question,
        "answer": GENERIC_ANSWER,
        "fallback": True,
        "confidence": "Low",
        "mode": AI_MODE if AI_MODE in ("retrieval", "gemini") else "retrieval",
        "sources": [],
    }


def _emit(payload: dict) -> None:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False))


def main() -> int:
    log_ai_mode()

    question = " ".join(sys.argv[1:]).strip()
    if not question:
        logger.error("query_json invoked without a question")
        _emit(_generic_payload(""))
        return 0

    try:
        from chain import rag_query

        result = rag_query(question)
        _emit(result.to_dict())
        return 0
    except ValueError as exc:
        logger.warning("Invalid question: %s", exc)
        _emit(_generic_payload(question))
        return 0
    except Exception:
        logger.exception("RAG query failed unexpectedly")
        _emit(_generic_payload(question))
        return 0


if __name__ == "__main__":
    sys.exit(main())
