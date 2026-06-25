#!/usr/bin/env sh
# Railway startup wrapper — binds public interface and uses Railway PORT.
set -eu
PORT="${PORT:-8100}"
exec python server.py --host 0.0.0.0 --port "$PORT"
