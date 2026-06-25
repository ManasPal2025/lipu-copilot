"""Log active AI mode once per process."""

from __future__ import annotations

import sys

from config import ENABLE_GEMINI

_logged = False


def log_ai_mode() -> None:
    global _logged
    if _logged:
        return
    _logged = True
    label = "Gemini Enabled" if ENABLE_GEMINI else "Retrieval Only"
    print(f"[AI MODE] {label}", file=sys.stderr, flush=True)
