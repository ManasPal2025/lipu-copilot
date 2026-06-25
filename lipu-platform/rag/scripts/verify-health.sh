#!/usr/bin/env sh
# Verify the RAG server health endpoint after Railway deploy.
# Usage: ./scripts/verify-health.sh https://your-service.up.railway.app

set -eu

BASE_URL="${1:-http://127.0.0.1:8100}"
BASE_URL="${BASE_URL%/}"

echo "GET ${BASE_URL}/health"
HTTP_CODE=$(curl -sS -o /tmp/rag-health.json -w "%{http_code}" "${BASE_URL}/health")

echo "HTTP ${HTTP_CODE}"
cat /tmp/rag-health.json
echo

if [ "$HTTP_CODE" != "200" ]; then
  echo "FAIL: expected HTTP 200" >&2
  exit 1
fi

python3 - <<'PY'
import json, sys
data = json.load(open("/tmp/rag-health.json"))
assert data.get("status") == "ok", data
assert data.get("resources_loaded") is True, data
assert data.get("collection_name") == "lipu_knowledge", data
count = data.get("vector_count")
assert isinstance(count, int) and count > 0, f"vector_count invalid: {count!r}"
print(f"OK: lipu_knowledge has {count} vectors")
PY

echo
echo "POST ${BASE_URL}/query (smoke test)"
curl -sS -X POST "${BASE_URL}/query" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is UPVC?"}' | python3 -m json.tool

echo
echo "Health verification complete."
