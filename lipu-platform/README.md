# LIPU Platform - AI-Powered UPVC Windows & Doors E-commerce

A production-grade, enterprise-scale e-commerce platform for UPVC windows and doors with AI-powered features including intelligent sales agents, house visualization, and design recommendations.

## 🏗️ Architecture

- **Frontend:** Next.js 15 + React 19 + TypeScript + Tailwind CSS
- **Backend:** FastAPI + Python + SQLAlchemy
- **Database:** PostgreSQL 15 + Redis 7
- **Vector DB:** Qdrant (AI embeddings & RAG)
- **AI/ML:** LangChain + LangGraph + OpenAI
- **Infrastructure:** Docker + GitHub Actions + AWS

## 📁 Project Structure

```
lipu-platform/
├── packages/
│   ├── types/           # Shared TypeScript types
│   ├── utils/           # Shared utilities
│   └── ui/              # Shared UI components
├── apps/
│   ├── web/             # Next.js frontend
│   ├── admin/           # Admin dashboard (future)
│   └── api/             # FastAPI backend
├── docs/                # Architecture & guides
├── scripts/             # Utility scripts
└── docker-compose.yml   # Local development
```

## 🚀 Getting Started

### Prerequisites

- Docker Desktop 4.0+
- Node.js 20 LTS
- Python 3.11
- Git 2.30+

### Quick Start

```bash
# Clone repository
git clone https://github.com/lipu/lipu-platform.git
cd lipu-platform

# Setup environment
cp .env.example .env.local
# Edit .env.local with your credentials

# Start services
docker-compose up -d

# Install dependencies
npm install

# Run backend
cd apps/api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Run frontend (new terminal)
cd apps/web
npm run dev

# Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🛠️ Development

### Available Commands

```bash
# Development
npm run dev          # Start all services
npm run web:dev      # Start only frontend
npm run api:dev      # Start only backend

# Build
npm run build        # Build all services
npm run web:build    # Build frontend
npm run api:build    # Build backend

# Code Quality
npm run lint         # Lint all code
npm run type-check   # Check types
npm run test         # Run tests
npm run format       # Format code
npm run format:check # Check formatting

# Cleanup
npm run clean        # Remove all artifacts
```

### Workspace Management

Using npm workspaces for monorepo management:

```bash
# Install dependency in specific workspace
npm install -w packages/types axios

# Install dev dependency
npm install -w apps/web -D tailwindcss

# Run script in specific workspace
npm run -w apps/web dev
```

## 📚 Documentation

Comprehensive architecture and development documentation:

- [00-ARCHITECTURE.md](docs/architecture/00-ARCHITECTURE.md) - System design & patterns
- [01-DATABASE-SCHEMA.md](docs/architecture/01-DATABASE-SCHEMA.md) - Database design
- [02-API-CONTRACTS.md](docs/architecture/02-API-CONTRACTS.md) - API specification
- [03-FOLDER-STRUCTURE.md](docs/architecture/03-FOLDER-STRUCTURE.md) - Code organization
- [04-USER-JOURNEYS.md](docs/architecture/04-USER-JOURNEYS.md) - User flows & personas
- [05-IMPLEMENTATION-ROADMAP.md](docs/architecture/05-IMPLEMENTATION-ROADMAP.md) - Development timeline
- [06-SPRINT-PLAN.md](docs/architecture/06-SPRINT-PLAN.md) - Sprint 0 details
- [07-SPRINT-0-EXECUTION-PLAN.md](docs/architecture/07-SPRINT-0-EXECUTION-PLAN.md) - Technical blueprint

See [docs/guides/](docs/guides/) for setup and development guides.

## 🔑 API Documentation

Interactive API documentation available at `http://localhost:8000/docs` when backend is running.

API specification: [02-API-CONTRACTS.md](docs/architecture/02-API-CONTRACTS.md)

## 🧪 Testing

```bash
# Frontend tests
npm run -w apps/web test

# Backend tests
cd apps/api && pytest

# Coverage
npm run -w apps/web test -- --coverage
cd apps/api && pytest --cov
```

## 🐳 Docker

### Local Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Clean up volumes
docker-compose down -v
```

### Services

- **PostgreSQL** - Port 5433 (5432 internal)
- **Redis** - Port 6380 (6379 internal)
- **Qdrant** - Port 6333 (vector DB)
- **PgAdmin** - Port 5050 (database GUI)
- **FastAPI** - Port 8000
- **Next.js** - Port 3000

## 📋 Environment Variables

See [.env.example](.env.example) for complete list of variables.

### Essential Variables

```env
# Clerk Auth
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# OpenAI
OPENAI_API_KEY=sk-...

# Stripe
STRIPE_SECRET_KEY=sk_test_...

# Database
DATABASE_URL=postgresql://...
```

## 🔒 Security

- TLS 1.3 for all communications
- JWT-based authentication with Clerk
- Role-based access control (RBAC)
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy
- CORS protection
- Rate limiting
- Audit logging

## 📊 CI/CD

GitHub Actions workflows:

- **lint.yml** - ESLint + Black + Type checking
- **build.yml** - Docker image builds
- **test.yml** - Unit & integration tests
- **deploy-staging.yml** - Deploy to staging
- **deploy-prod.yml** - Deploy to production

## 🎯 Current Sprint

**Sprint 0** (Weeks 1-2): Foundation & Infrastructure
- Repository setup
- Docker Compose environment
- CI/CD pipeline
- FastAPI scaffolding
- Next.js setup
- Basic API endpoints

See [06-SPRINT-PLAN.md](docs/architecture/06-SPRINT-PLAN.md) for details.

## 📈 Roadmap

- **Phase 1** (Weeks 1-4): Foundation
- **Phase 2** (Weeks 5-8): Public Website & Catalog
- **Phase 3** (Weeks 9-14): Customer Portal & MVP
- **Phase 4** (Weeks 15-20): AI Sales Agent
- **Phase 5** (Weeks 21-26): Advanced AI Features
- **Phase 6** (Weeks 27-32): Admin Dashboard
- **Phase 7** (Weeks 33-38): Performance & Scale
- **Phase 8** (Weeks 39-44): Enterprise & Compliance

See [05-IMPLEMENTATION-ROADMAP.md](docs/architecture/05-IMPLEMENTATION-ROADMAP.md) for full timeline.

## 🤝 Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for our code of conduct and development process.

### Code Standards

- **Frontend**: ESLint + Prettier + TypeScript strict mode
- **Backend**: Black + Flake8 + MyPy
- **Tests**: Jest (frontend), Pytest (backend) - 80%+ coverage
- **Types**: No `any` types allowed

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/feature-name

# Make changes and commit
git add .
git commit -m "feat: description of change"

# Push and create PR
git push origin feature/feature-name
```

## 📞 Support

- **Documentation**: See [docs/](docs/) directory
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

## 👥 Team

Built by the LIPU Development Team

---

**Project Status**: 🚧 In Development (Sprint 0)  
**Last Updated**: June 24, 2026  
**Version**: 0.1.0
