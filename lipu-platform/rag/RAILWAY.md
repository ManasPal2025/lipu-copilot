# Deploy the LIPU RAG server to Railway

Target architecture:

```
Vercel (Next.js /api/chat)  →  Railway (server.py)  →  Chroma (persistent volume)
```

This guide deploys **only** `lipu-platform/rag` — no changes to retrieval logic, Chroma schema, embeddings, or API contract.

---

## Prerequisites

| Item | Detail |
|------|--------|
| **Railway account** | [railway.app](https://railway.app) |
| **Railway CLI** | `npm i -g @railway/cli` (optional, for volume seeding) |
| **Local RAG working** | `python server.py` returns answers with 540 vectors |
| **Local Chroma index** | `lipu-platform/rag/data/chroma/` (gitignored, ~4–5 MB) |
| **Git repo** | Connected to Railway |

---

## 1. Railway service setup

### Create project

1. Railway Dashboard → **New Project** → **Deploy from GitHub repo**
2. Select this repository
3. Add a **new service** for the RAG server

### Root directory (critical)

Set the service **Root Directory** to:

```
lipu-platform/rag
```

Railway must build and start from this folder so `config.py` paths resolve correctly:

- `CHROMA_PERSIST_DIR` → `./data/chroma`
- `COLLECTION_NAME` → `lipu_knowledge`

### Config files (already in repo)

| File | Purpose |
|------|---------|
| `requirements.txt` | Python dependencies |
| `runtime.txt` | Python 3.11.9 |
| `railway.toml` | Start command, health check, build |
| `Procfile` | Alternative start command (Heroku-compatible) |
| `scripts/start-railway.sh` | Shell wrapper for `$PORT` binding |

### Startup command

Railway sets `$PORT`. The server must bind `0.0.0.0` (not `127.0.0.1`):

```bash
python server.py --host 0.0.0.0 --port $PORT
```

Configured in `railway.toml` → `deploy.startCommand`.

**Cold start:** `initialize_resources()` loads BGE embeddings + Chroma before accepting traffic (~60–120s first deploy).

### Resources

| Setting | Recommended |
|---------|-------------|
| **RAM** | ≥ 2 GB |
| **CPU** | 1 vCPU minimum |
| **Region** | Closest to Vercel deployment (e.g. Singapore / Mumbai if available) |

---

## 2. Persistent Chroma storage

Chroma data lives at `data/chroma/` (relative to `rag/`). It is **gitignored** — Railway will not receive it from Git.

### Volume mount path

Create a Railway **Volume** on the RAG service:

| Setting | Value |
|---------|-------|
| **Mount path** | `/app/data/chroma` |

Railway places your app in `/app`. `config.py` writes to `RAG_ROOT / "data" / "chroma"` → `/app/data/chroma` when the volume is mounted.

CLI:

```bash
cd lipu-platform/rag
railway link
railway volume add --mount-path /app/data/chroma
```

### Seed the 540-vector index (one-time)

Copy your **local** working index to the volume **before** or **immediately after** first deploy.

**Option A — Railway CLI + tar (recommended)**

From your dev machine (PowerShell / bash), with a working local index:

```bash
cd lipu-platform/rag

# Pack local Chroma (includes chroma.sqlite3 + HNSW binaries)
tar -czf /tmp/lipu-chroma.tar.gz -C data chroma

# Open a shell on the running service and extract into the volume
railway run sh -c 'mkdir -p /app/data && tar -xzf - -C /app/data' < /tmp/lipu-chroma.tar.gz
```

If `railway run` cannot stream stdin, use a one-off deploy script or Railway **Volume file browser** in the dashboard to upload the contents of `data/chroma/`.

**Option B — Re-ingest on Railway (only if you also deploy documents)**

Requires copying `lipu-platform/documents/` into the container and running `python ingest.py --reset`. This **rebuilds** the index and is only needed if you cannot upload the existing volume. Not required if you preserve the local 540-chunk index via Option A.

### Verify Chroma after seeding

```bash
./scripts/verify-health.sh https://YOUR-SERVICE.up.railway.app
```

Expected:

```json
{
  "status": "ok",
  "resources_loaded": true,
  "collection_name": "lipu_knowledge",
  "vector_count": 540,
  "chroma_collection": "lipu_knowledge"
}
```

### Optional: Hugging Face model cache volume

To avoid re-downloading `BAAI/bge-small-en-v1.5` on every redeploy:

| Mount path | Purpose |
|------------|---------|
| `/app/.cache/huggingface` | Embedding model cache |

Set env: `HF_HOME=/app/.cache/huggingface`

---

## 3. Environment variables

Set in **Railway → RAG service → Variables**:

| Variable | Required | Default / notes |
|----------|----------|-----------------|
| `PORT` | Auto | Set by Railway — do not override |
| `AI_MODE` | No | Controlled in `config.py` (`retrieval` or `gemini`) — change in code before deploy if needed |
| `GOOGLE_API_KEY` | Only for Gemini | Required when `AI_MODE=gemini` in `config.py` |
| `GEMINI_API_KEY` | Alt to above | Same as `GOOGLE_API_KEY` |
| `RAG_RETRIEVER_DEBUG` | No | `1` for `[RETRIEVER]` logs (optional) |
| `HF_TOKEN` | No | Hugging Face token — faster model downloads |
| `HF_HOME` | No | `/app/.cache/huggingface` if using cache volume |

**Do not set** `RAG_SERVER_URL` on Railway — that is for Vercel only.

### Vercel variables (web app)

After Railway deploy, set on **Vercel → Project → Environment Variables**:

| Variable | Value |
|----------|-------|
| `AI_ENABLED` | `true` |
| `AI_MODE` | `retrieval` |
| `RAG_SERVER_URL` | `https://YOUR-SERVICE.up.railway.app` (no trailing slash) |

Redeploy Vercel after adding variables.

---

## 4. API contract (unchanged)

### `GET /health`

```http
GET /health
```

Response `200`:

```json
{
  "status": "ok",
  "resources_loaded": true,
  "collection_name": "lipu_knowledge",
  "persist_dir": "/app/data/chroma",
  "vector_count": 540,
  "chroma_collection": "lipu_knowledge",
  "startup_timings_ms": { "embedding_model": 9000, "chroma_init": 250, "total": 9250 }
}
```

### `POST /query`

```http
POST /query
Content-Type: application/json

{"question": "What is UPVC?"}
```

Response `200`:

```json
{
  "question": "What is UPVC?",
  "answer": "...",
  "fallback": false,
  "confidence": "Medium",
  "mode": "retrieval",
  "sources": [{ "name": "...", "id": "..." }]
}
```

Optional profiling: `POST /query?profile=1` adds `timings_ms`.

---

## 5. Health endpoint verification

### Automated script

```bash
chmod +x scripts/verify-health.sh
./scripts/verify-health.sh https://YOUR-SERVICE.up.railway.app
```

### Manual checks

```bash
# Health
curl -sS https://YOUR-SERVICE.up.railway.app/health | jq .

# Query smoke test
curl -sS -X POST https://YOUR-SERVICE.up.railway.app/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Which window is best for my balcony?"}' | jq .
```

### Railway dashboard

- **Settings → Health Check Path:** `/health`
- **Timeout:** 300 seconds (configured in `railway.toml`)
- Deployment should turn **Healthy** after model load completes

### End-to-end (Vercel → Railway)

```bash
curl -sS -X POST https://YOUR-VERCEL-DOMAIN/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What is UPVC?"}' | jq .
```

Expect non-empty `answer` and `sources` when `AI_ENABLED=true` and `RAG_SERVER_URL` points to Railway.

---

## 6. Deploy checklist

- [ ] Railway service root = `lipu-platform/rag`
- [ ] Volume mounted at `/app/data/chroma`
- [ ] Local Chroma index copied to volume (`vector_count: 540`)
- [ ] RAM ≥ 2 GB
- [ ] Health check `/health` returns 200 with `resources_loaded: true`
- [ ] `POST /query` returns answer + sources locally on Railway URL
- [ ] Vercel `RAG_SERVER_URL` set to Railway public URL
- [ ] Vercel `AI_ENABLED=true`
- [ ] `/consult` page returns real answers in production

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Health check timeout | Model download slow | Increase `healthcheckTimeout`; set `HF_TOKEN`; add HF cache volume |
| `vector_count: 0` or missing | Empty volume | Seed `data/chroma` from local machine |
| `Vector store not found` | Volume not mounted | Confirm mount path `/app/data/chroma` |
| Vercel still shows fallback | `AI_ENABLED=false` or wrong URL | Set Vercel env vars; redeploy |
| OOM crash on start | Insufficient RAM | Upgrade Railway plan / memory |
| Connection refused from Vercel | Server bound to 127.0.0.1 | Use `--host 0.0.0.0` (already in `railway.toml`) |

---

## 8. What is NOT deployed

These stay local / on Vercel only:

- Python subprocess fallback (`query_json.py`) — Vercel production uses HTTP only
- `lipu-platform/documents/` — not needed at runtime if Chroma volume is seeded
- `.venv/` — Railway builds fresh from `requirements.txt`

Retrieval behavior, chunk count, and answer formatting are identical to local `python server.py` when the same Chroma files are on the volume.
