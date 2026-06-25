#!/usr/bin/env python3
"""
Persistent RAG HTTP server — loads embedding model and Chroma once at startup.

Usage (from lipu-platform/rag/):
    python server.py
    python server.py --port 8100
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,
    format="%(levelname)s %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

resources_ready = False
startup_error: BaseException | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Persistent RAG HTTP server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8100)
    return parser.parse_args()


def load_resources_background() -> None:
    global resources_ready, startup_error

    from ai_mode import log_ai_mode
    from config import AI_MODE
    from resources import initialize_resources

    try:
        log_ai_mode()
        logger.info("Loading RAG resources at startup (AI_MODE=%s)...", AI_MODE)
        init = initialize_resources()
        logger.info(
            "Startup complete — embedding=%.0fms chroma=%.0fms total=%.0fms",
            init.embedding_model_ms,
            init.chroma_init_ms,
            init.total_ms,
        )
        resources_ready = True
    except Exception as exc:
        startup_error = exc
        logger.exception("Background resource loading failed")


class RagHandler(BaseHTTPRequestHandler):
    server_version = "LipuRAG/1.0"

    def log_message(self, format: str, *args: Any) -> None:
        logger.info("%s - %s", self.address_string(), format % args)

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/health":
            if startup_error is not None:
                self._send_json(
                    500,
                    {
                        "status": "failed",
                        "error": str(startup_error),
                    },
                )
                return

            if not resources_ready:
                self._send_json(
                    200,
                    {
                        "status": "starting",
                        "resources_loaded": False,
                    },
                )
                return

            from config import CHROMA_PERSIST_DIR, COLLECTION_NAME
            from resources import get_init_timings, get_vector_store, resources_initialized

            init = get_init_timings()
            health: dict[str, object] = {
                "status": "ok",
                "resources_loaded": resources_initialized(),
                "collection_name": COLLECTION_NAME,
                "persist_dir": str(CHROMA_PERSIST_DIR),
                "startup_timings_ms": {
                    "embedding_model": round(init.embedding_model_ms, 1),
                    "chroma_init": round(init.chroma_init_ms, 1),
                    "total": round(init.total_ms, 1),
                },
            }
            if resources_initialized():
                store = get_vector_store()
                health["vector_count"] = store._collection.count()  # noqa: SLF001
                health["chroma_collection"] = store._collection.name  # noqa: SLF001
            self._send_json(200, health)
            return

        self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/query":
            self._send_json(404, {"error": "Not found"})
            return

        if not resources_ready:
            self._send_json(503, {"error": "RAG resources still loading"})
            return

        api_received = time.perf_counter()
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"

        try:
            body = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send_json(400, {"error": "Invalid JSON body"})
            return

        question = str(body.get("question", "")).strip()
        if not question:
            self._send_json(400, {"error": "question is required"})
            return

        logger.info("POST /query received — question=%r", question[:120])

        profile = parse_qs(parsed.query).get("profile", ["0"])[0] == "1"

        try:
            from chain import rag_query_profiled

            result, timings = rag_query_profiled(question)
            timings.api_received_ms = (time.perf_counter() - api_received) * 1000

            payload = result.to_dict()
            if profile:
                payload["timings_ms"] = timings.to_dict()
            self._send_json(200, payload)
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception:
            logger.exception("Query failed")
            self._send_json(
                500,
                {
                    "answer": (
                        "We're having trouble answering right now. "
                        "Please try again in a moment."
                    ),
                    "confidence": "Low",
                    "mode": "retrieval",
                    "sources": [],
                    "fallback": True,
                },
            )


def main() -> int:
    args = parse_args()

    httpd = ThreadingHTTPServer((args.host, args.port), RagHandler)
    threading.Thread(
        target=load_resources_background,
        daemon=True,
    ).start()

    logger.info("RAG server listening on http://%s:%s", args.host, args.port)
    print(f"[RAG SERVER] http://{args.host}:{args.port}", file=sys.stderr, flush=True)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down")
        httpd.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
