# Quick Reference

## Common Commands

### Development

```bash
# Start all services
npm run dev

# Start only frontend
npm run web:dev

# Start only backend
cd apps/api && uvicorn app.main:app --reload

# Install dependencies
npm install
```

### Building

```bash
# Build all
npm run build

# Build frontend
npm run web:build

# Build backend
npm run api:build
```

### Code Quality

```bash
# Lint all
npm run lint

# Check types
npm run type-check

# Run tests
npm run test

# Format code
npm run format
```

### Docker

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart postgres
```

### Database

```bash
# Run migrations
cd apps/api && alembic upgrade head

# Create migration
cd apps/api && alembic revision --autogenerate -m "Description"

# Seed data (coming soon)
cd apps/api && python scripts/seed_data.py
```

## Useful URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web application |
| Backend | http://localhost:8000 | API server |
| API Docs | http://localhost:8000/docs | Swagger UI |
| ReDoc | http://localhost:8000/redoc | API documentation |
| PgAdmin | http://localhost:5050 | Database management |
| Qdrant | http://localhost:6333 | Vector database |

## Important Files

| File | Purpose |
|------|---------|
| `docker-compose.yml` | Services configuration |
| `.env.example` | Environment template |
| `package.json` | Root workspace config |
| `apps/web/package.json` | Frontend config |
| `apps/api/pyproject.toml` | Backend config |
| `apps/api/requirements.txt` | Backend dependencies |

## Getting Help

1. Check [docs/guides/](guides/) for detailed guides
2. Read [CONTRIBUTING.md](../CONTRIBUTING.md)
3. Review [Architecture documentation](architecture/)
4. Search existing issues on GitHub
5. Create a new issue with details

---

**Last Updated**: June 24, 2026
