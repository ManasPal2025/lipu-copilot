# Backend - FastAPI Application

FastAPI backend for LIPU platform.

## Setup

```bash
cd apps/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment
cp .env.example .env.local
```

## Development

```bash
# Run dev server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest

# Run with coverage
pytest --cov=app

# Lint
black --check .
flake8 .
mypy .
```

## Database

```bash
# Run migrations
alembic upgrade head

# Create migration
alembic revision --autogenerate -m "Description"

# Rollback
alembic downgrade -1
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
