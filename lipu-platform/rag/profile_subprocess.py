#!/usr/bin/env python3
"""Profile helper — run one query in an isolated process (simulates legacy spawn)."""

from __future__ import annotations

import json
import sys

from dotenv import load_dotenv

load_dotenv()


def main() -> int:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print("question required", file=sys.stderr)
        return 1

    from chain import rag_query_profiled

    result, timings = rag_query_profiled(question)
    sys.stdout.write(json.dumps({**result.to_dict(), "timings_ms": timings.to_dict()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
