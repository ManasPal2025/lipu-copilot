# Development Setup Guide

Complete guide to set up your development environment.

## Prerequisites

- Docker Desktop 4.0+
- Node.js 20 LTS
- Python 3.11
- Git 2.30+
- VS Code (recommended)

### Installation

**Windows:**
- Download Docker Desktop from https://www.docker.com/products/docker-desktop
- Download Node.js from https://nodejs.org
- Download Python from https://www.python.org
- Download Git from https://git-scm.com

**macOS:**
```bash
brew install docker
brew install node
brew install python@3.11
brew install git
```

**Linux (Ubuntu):**
```bash
sudo apt-get install docker.io nodejs python3.11 git
```

## Setup Steps

### 1. Clone Repository

```bash
git clone https://github.com/lipu/lipu-platform.git
cd lipu-platform
git checkout develop
```

### 2. Setup Environment Variables

```bash
cp .env.example .env.local
# Edit .env.local with your credentials
```

### 3. Start Docker Services

```bash
docker-compose up -d

# Verify services
docker-compose ps

# View logs
docker-compose logs -f
```

Services will be available at:
- PostgreSQL: localhost:5433
- Redis: localhost:6380
- Qdrant: localhost:6333
- PgAdmin: localhost:5050
- LocalStack: localhost:4566

### 4. Backend Setup

```bash
cd apps/api

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Setup environment
cp .env.example .env.local

# Run migrations (future)
# alembic upgrade head
```

### 5. Frontend Setup

```bash
cd apps/web

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
```

### 6. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd apps/api
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd apps/web
npm run dev
```

**Terminal 3 - Optional - Root Commands:**
```bash
# Run all dev servers
npm run dev
```

### 7. Access Applications

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database GUI: http://localhost:5050

## Troubleshooting

### Docker issues

```bash
# Restart services
docker-compose restart

# Remove and recreate
docker-compose down
docker-compose up -d

# Clean everything
docker-compose down -v
```

### Python issues

```bash
# Recreate virtual environment
rm -rf apps/api/venv
python -m venv apps/api/venv
source apps/api/venv/bin/activate
pip install -r apps/api/requirements.txt
```

### Node issues

```bash
# Clear cache
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### Port conflicts

If ports are already in use, edit `.env` file and change ports, or:

```bash
# Find process on port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

## Next Steps

- Read [docs/guides/](../guides/) for specific guides
- Check [CONTRIBUTING.md](../../CONTRIBUTING.md) for development standards
- Review [docs/architecture/](../architecture/) for architecture details
