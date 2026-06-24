# LIPU — Local Development

Run the full stack locally: **Postgres + Redis** in Docker, **API** and **Web** on the host.

## Prerequisites

- **Node.js 20+** (required by Next.js 15)
- Python 3.11+
- Docker Desktop (for database & Redis)

## Quick start (recommended)

### 1. Infrastructure

```powershell
cd lipu-platform
docker compose -f docker-compose.infra.yml up -d
```

Postgres: `localhost:5433` · Redis: `localhost:6380`

### 2. Backend API

```powershell
cd lipu-platform\apps\api
copy .env.example .env.local
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs  
Health: http://localhost:8000/api/v1/health/ready

### 3. Frontend

```powershell
cd lipu-platform
npm install
cd apps\web
copy .env.example .env.local
npm run dev
```

Website: http://localhost:3000

---

## All-in-one Docker (optional)

Runs Postgres, Redis, Qdrant, LocalStack, API, and Web in containers:

```powershell
cd lipu-platform
copy .env.example .env
docker compose up -d
```

---

## Integration decision

**Source of truth:** `lipu-platform/` monorepo  
**API location:** `lipu-platform/apps/api/` (migrated from root `backend/`)

Root `backend/` is deprecated. Do not develop there.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| DB connection refused | Ensure `docker compose -f docker-compose.infra.yml up -d` and use port **5433** in `.env.local` |
| Redis connection refused | Use port **6380** in `.env.local` |
| `ModuleNotFoundError: fastapi` | Activate venv and `pip install -r requirements.txt` |
| Frontend build errors | Run `npm install` from `lipu-platform` root (workspaces) |
