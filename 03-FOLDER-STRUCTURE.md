# Project Folder Structure & Repository Strategy

**Document Version:** 1.0  
**Status:** Structure Design Phase  
**Decision:** Monorepo Structure (Recommended)

---

## Table of Contents

1. [Repository Strategy](#repository-strategy)
2. [Monorepo Structure](#monorepo-structure)
3. [Frontend (Next.js) Structure](#frontend-nextjs-structure)
4. [Backend (FastAPI) Structure](#backend-fastapi-structure)
5. [Shared Packages](#shared-packages)
6. [Configuration & Scripts](#configuration--scripts)
7. [Dependencies & Workspaces](#dependencies--workspaces)
8. [Development Workflow](#development-workflow)

---

## Repository Strategy

### Decision: Monorepo with Workspaces

**Why Monorepo?**

✅ Shared code between frontend & backend  
✅ Atomic commits across services  
✅ Simplified dependency management  
✅ Easier refactoring  
✅ Unified CI/CD pipeline  
✅ Single source of truth for types/schemas  

**Tools:**
- **Workspace Manager:** npm workspaces (built-in)
- **Build Tool:** Turborepo (optional, for build caching)
- **Version Control:** Single GitHub repository

### Monorepo Structure

```
lipu-platform/
├── .github/                    # GitHub workflows, templates
├── .vscode/                    # VS Code settings (shared)
├── packages/                   # Shared packages
│   ├── types/                 # TypeScript types, schemas
│   ├── utils/                 # Shared utilities
│   └── ui/                    # Shared UI components
├── apps/
│   ├── web/                   # Next.js frontend
│   ├── admin/                 # Admin dashboard (Next.js)
│   └── api/                   # FastAPI backend
├── docs/                      # Architecture, API docs
├── scripts/                   # Utility scripts
├── docker-compose.yml         # Local development
├── package.json              # Root workspace config
├── turbo.json                # Turborepo config (if using)
├── .gitignore
├── README.md
└── CONTRIBUTING.md
```

---

## Frontend (Next.js) Structure

### Location: `apps/web/`

```
apps/web/
├── app/                       # Next.js App Router (main application)
│   ├── (marketing)/          # Public marketing pages (grouped)
│   │   ├── page.tsx          # Homepage
│   │   ├── layout.tsx
│   │   ├── about/
│   │   │   └── page.tsx
│   │   ├── products/
│   │   │   ├── page.tsx      # Products listing
│   │   │   └── [slug]/
│   │   │       └── page.tsx  # Product detail
│   │   ├── gallery/
│   │   │   └── page.tsx
│   │   ├── projects/
│   │   │   ├── page.tsx
│   │   │   └── [slug]/
│   │   │       └── page.tsx
│   │   ├── testimonials/
│   │   │   └── page.tsx
│   │   ├── blog/
│   │   │   ├── page.tsx
│   │   │   └── [slug]/
│   │   │       └── page.tsx
│   │   ├── contact/
│   │   │   └── page.tsx
│   │   ├── faq/
│   │   │   └── page.tsx
│   │   └── sitemap.xml       # SEO
│   │
│   ├── (auth)/               # Auth pages (layout)
│   │   ├── layout.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── forgot-password/
│   │       └── page.tsx
│   │
│   ├── (customer)/           # Protected customer routes
│   │   ├── layout.tsx        # Customer layout (sidebar, nav)
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── profile/
│   │   │   └── page.tsx
│   │   ├── projects/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── quotes/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── orders/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── invoices/
│   │   │   └── page.tsx
│   │   ├── support-tickets/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── saved-designs/
│   │   │   └── page.tsx
│   │   └── ai-conversations/
│   │       ├── page.tsx
│   │       └── [id]/
│   │           └── page.tsx
│   │
│   ├── (admin)/              # Protected admin routes
│   │   ├── layout.tsx        # Admin layout
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── inventory/
│   │   │   ├── page.tsx
│   │   │   └── [id]/
│   │   │       └── page.tsx
│   │   ├── products/
│   │   ├── orders/
│   │   ├── customers/
│   │   ├── projects/
│   │   ├── leads/
│   │   ├── quotes/
│   │   ├── employees/
│   │   ├── analytics/
│   │   ├── reports/
│   │   ├── content/          # CMS
│   │   ├── ai-management/
│   │   ├── settings/
│   │   └── audit-logs/
│   │
│   ├── api/                  # API routes (Next.js API)
│   │   ├── auth/
│   │   ├── uploads/
│   │   ├── webhooks/
│   │   │   └── clerk/
│   │   │   └── stripe/
│   │   └── trpc/             # tRPC for frontend-backend sync
│   │
│   ├── layout.tsx            # Root layout
│   └── error.tsx             # Error boundaries
│
├── components/               # React components
│   ├── ui/                  # Shadcn UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── modal.tsx
│   │   ├── input.tsx
│   │   ├── form.tsx
│   │   ├── table.tsx
│   │   ├── tabs.tsx
│   │   ├── sidebar.tsx
│   │   ├── navbar.tsx
│   │   └── ... (other shadcn components)
│   │
│   ├── marketing/           # Marketing page components
│   │   ├── hero.tsx
│   │   ├── features.tsx
│   │   ├── testimonials.tsx
│   │   ├── cta-section.tsx
│   │   ├── pricing-table.tsx
│   │   └── footer.tsx
│   │
│   ├── customer/            # Customer portal components
│   │   ├── project-card.tsx
│   │   ├── quote-preview.tsx
│   │   ├── order-status.tsx
│   │   ├── invoice-viewer.tsx
│   │   └── design-gallery.tsx
│   │
│   ├── admin/               # Admin components
│   │   ├── data-table.tsx
│   │   ├── charts.tsx
│   │   ├── filters.tsx
│   │   ├── modals/
│   │   │   ├── create-product.tsx
│   │   │   ├── edit-order.tsx
│   │   │   └── add-inventory.tsx
│   │   └── dashboard-widgets/
│   │
│   ├── ai/                  # AI-related components
│   │   ├── chat-interface.tsx
│   │   ├── message-item.tsx
│   │   ├── typing-indicator.tsx
│   │   ├── visualization-generator.tsx
│   │   ├── quote-generator.tsx
│   │   └── design-consultant.tsx
│   │
│   ├── shared/              # Shared components
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   ├── breadcrumb.tsx
│   │   ├── pagination.tsx
│   │   ├── loading-spinner.tsx
│   │   ├── error-boundary.tsx
│   │   └── toast-notification.tsx
│   │
│   └── icons/               # Icon components
│       ├── product-icon.tsx
│       ├── cart-icon.tsx
│       └── ... (other icons)
│
├── lib/                     # Utility functions
│   ├── api.ts              # API client
│   ├── auth.ts             # Auth utilities
│   ├── validation.ts       # Input validation (Zod)
│   ├── formatting.ts       # String/number formatting
│   ├── constants.ts        # Constants, enums
│   ├── hooks/              # Custom React hooks
│   │   ├── useApi.ts
│   │   ├── useAuth.ts
│   │   ├── useForm.ts
│   │   ├── usePagination.ts
│   │   └── ... (other hooks)
│   └── utils/
│       ├── cn.ts           # Tailwind class merge
│       ├── date.ts
│       └── storage.ts      # LocalStorage utilities
│
├── store/                  # State management (Zustand/Redux)
│   ├── auth-store.ts
│   ├── cart-store.ts
│   ├── ui-store.ts
│   ├── customer-store.ts
│   └── ... (other stores)
│
├── styles/                 # Global styles
│   ├── globals.css
│   ├── variables.css       # CSS variables
│   └── animations.css
│
├── public/                 # Static assets
│   ├── images/
│   │   ├── logo.svg
│   │   ├── products/
│   │   ├── testimonials/
│   │   └── ...
│   ├── videos/
│   └── documents/
│
├── __tests__/              # Tests
│   ├── unit/
│   │   ├── lib/
│   │   └── utils/
│   ├── integration/
│   │   ├── auth/
│   │   └── api/
│   └── e2e/
│       ├── customer-flow.spec.ts
│       ├── admin-flow.spec.ts
│       └── quote-request.spec.ts
│
├── middleware.ts           # Next.js middleware
├── next.config.js
├── tailwind.config.ts
├── postcss.config.js
├── tsconfig.json
├── .env.example
├── .env.local
├── package.json
└── README.md
```

### Frontend Key Points

- **SEO Optimization:**
  - Static generation for marketing pages (ISR)
  - Dynamic meta tags for products
  - Structured data (Schema.org)
  - Sitemap generation

- **Performance:**
  - Image optimization (Next.js Image)
  - Code splitting by route
  - Font optimization
  - CSS extraction

- **Mobile-First:**
  - Responsive design (Tailwind breakpoints)
  - Touch-friendly UI
  - Mobile navigation

---

## Backend (FastAPI) Structure

### Location: `apps/api/`

```
apps/api/
├── app/                      # Main FastAPI application
│   ├── __init__.py
│   ├── main.py              # App initialization, middleware setup
│   │
│   ├── core/                # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py        # Environment config
│   │   ├── security.py      # JWT, auth utilities
│   │   ├── constants.py
│   │   └── logging.py       # Logging configuration
│   │
│   ├── db/                  # Database
│   │   ├── __init__.py
│   │   ├── session.py       # SQLAlchemy session
│   │   ├── base.py          # Base model class
│   │   └── models/          # ORM models (by domain)
│   │       ├── __init__.py
│   │       ├── organization.py
│   │       ├── user.py
│   │       ├── product.py
│   │       ├── order.py
│   │       ├── quote.py
│   │       ├── customer.py
│   │       ├── inventory.py
│   │       ├── ai.py        # AI-related models
│   │       └── audit.py
│   │
│   ├── schemas/             # Pydantic schemas (DTOs)
│   │   ├── __init__.py
│   │   ├── base.py          # Base schemas
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── quote.py
│   │   ├── customer.py
│   │   ├── inventory.py
│   │   ├── ai.py
│   │   └── auth.py
│   │
│   ├── api/                 # API routes (by feature)
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py      # /auth endpoints
│   │   │   ├── products.py  # /products endpoints
│   │   │   ├── orders.py    # /orders endpoints
│   │   │   ├── quotes.py    # /quotes endpoints
│   │   │   ├── customers.py # /customers endpoints
│   │   │   ├── inventory.py # /inventory endpoints
│   │   │   ├── ai.py        # /ai endpoints
│   │   │   ├── analytics.py # /analytics endpoints
│   │   │   ├── uploads.py   # /uploads endpoints
│   │   │   └── health.py    # /health endpoint
│   │   └── v2/              # Future versioning
│   │
│   ├── services/            # Business logic (by domain)
│   │   ├── __init__.py
│   │   ├── product_service.py
│   │   ├── order_service.py
│   │   ├── quote_service.py
│   │   ├── customer_service.py
│   │   ├── inventory_service.py
│   │   ├── payment_service.py
│   │   ├── email_service.py
│   │   ├── file_service.py
│   │   └── notification_service.py
│   │
│   ├── ai/                  # AI/ML services
│   │   ├── __init__.py
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── document_processor.py
│   │   │   ├── embedder.py
│   │   │   ├── retriever.py
│   │   │   └── vector_store.py
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── sales_agent.py
│   │   │   ├── quote_generator.py
│   │   │   └── design_consultant.py
│   │   ├── vision/
│   │   │   ├── __init__.py
│   │   │   ├── window_detector.py
│   │   │   └── image_generator.py
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   ├── prompts.py
│   │   │   └── chains.py
│   │   └── models.py        # AI model schemas
│   │
│   ├── tasks/               # Background tasks (Celery/APScheduler)
│   │   ├── __init__.py
│   │   ├── email_tasks.py
│   │   ├── inventory_tasks.py
│   │   ├── analytics_tasks.py
│   │   ├── ai_tasks.py
│   │   └── cleanup_tasks.py
│   │
│   ├── events/              # Event handlers
│   │   ├── __init__.py
│   │   ├── order_events.py
│   │   ├── quote_events.py
│   │   ├── inventory_events.py
│   │   └── ai_events.py
│   │
│   ├── middleware/          # Custom middleware
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   ├── logging_middleware.py
│   │   ├── error_handler.py
│   │   └── rate_limiter.py
│   │
│   ├── utils/               # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   ├── formatters.py
│   │   ├── decorators.py
│   │   ├── helpers.py
│   │   └── exceptions.py
│   │
│   ├── webhooks/            # Webhook handlers
│   │   ├── __init__.py
│   │   ├── clerk.py
│   │   ├── stripe.py
│   │   └── external_services.py
│   │
│   └── websocket/           # WebSocket handlers
│       ├── __init__.py
│       ├── connection_manager.py
│       └── events.py
│
├── migrations/              # Alembic database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_initial_schema.py
│       ├── 002_add_audit_logs.py
│       └── ...
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Pytest fixtures
│   ├── unit/
│   │   ├── services/
│   │   │   ├── test_product_service.py
│   │   │   ├── test_order_service.py
│   │   │   └── ...
│   │   ├── utils/
│   │   └── models/
│   ├── integration/
│   │   ├── test_api_products.py
│   │   ├── test_api_orders.py
│   │   ├── test_auth_flow.py
│   │   └── ...
│   └── fixtures/
│       ├── products.py
│       ├── orders.py
│       └── ...
│
├── __init__.py
├── requirements.txt         # Python dependencies
├── requirements-dev.txt     # Development dependencies
├── .env.example
├── .env.local
├── pyproject.toml          # Python project config
├── setup.py
├── alembic.ini             # Alembic config
├── pytest.ini              # Pytest config
├── docker-entrypoint.sh    # Docker startup script
├── Dockerfile
└── README.md
```

### Backend Key Points

- **Domain-Driven Design:** Services organized by business domain
- **Separation of Concerns:** Schemas, models, services, API routes
- **Type Safety:** Pydantic for request/response validation
- **Async-First:** FastAPI async/await for high concurrency
- **Testing:** Comprehensive unit and integration tests
- **Documentation:** Auto-generated OpenAPI docs

---

## Shared Packages

### Location: `packages/`

```
packages/
├── types/                    # Shared TypeScript types
│   ├── src/
│   │   ├── product.ts
│   │   ├── order.ts
│   │   ├── quote.ts
│   │   ├── customer.ts
│   │   ├── ai.ts
│   │   ├── api.ts           # API request/response types
│   │   └── index.ts         # Export all types
│   ├── package.json
│   └── tsconfig.json
│
├── utils/                    # Shared utility functions
│   ├── src/
│   │   ├── validation/
│   │   │   ├── product-validation.ts
│   │   │   ├── order-validation.ts
│   │   │   └── ...
│   │   ├── formatting/
│   │   │   ├── currency.ts
│   │   │   ├── date.ts
│   │   │   └── ...
│   │   ├── constants.ts
│   │   └── index.ts
│   ├── package.json
│   └── tsconfig.json
│
└── ui/                       # Shared UI components (optional)
    ├── src/
    │   ├── components/
    │   ├── hooks/
    │   ├── styles/
    │   └── index.ts
    ├── package.json
    └── tsconfig.json
```

---

## Configuration & Scripts

### Location: Root Directory

```
.github/
├── workflows/
│   ├── ci.yml              # Continuous Integration
│   ├── deploy-staging.yml  # Deploy to Staging
│   ├── deploy-prod.yml     # Deploy to Production
│   └── security-scan.yml   # Security scanning
└── ISSUE_TEMPLATE/
    └── bug-report.md

scripts/
├── setup.sh                # Initial project setup
├── dev.sh                  # Start development environment
├── test.sh                 # Run all tests
├── lint.sh                 # Lint and format code
├── deploy.sh               # Deployment script
└── migrate-db.sh           # Database migrations

.vscode/
├── extensions.json         # Recommended extensions
├── launch.json             # Debug configuration
├── settings.json           # Workspace settings
└── tasks.json              # Build tasks

.env.example               # Environment variables template
docker-compose.yml         # Local development setup
docker-compose.prod.yml    # Production setup
package.json              # Root workspace
tsconfig.json             # Root TypeScript config
turbo.json                # Turborepo config
```

---

## Dependencies & Workspaces

### Root `package.json`

```json
{
  "name": "lipu-platform",
  "version": "1.0.0",
  "private": true,
  "workspaces": [
    "apps/web",
    "apps/admin",
    "apps/api",
    "packages/types",
    "packages/utils",
    "packages/ui"
  ],
  "scripts": {
    "dev": "turbo run dev --parallel",
    "build": "turbo run build",
    "test": "turbo run test",
    "lint": "turbo run lint",
    "type-check": "turbo run type-check",
    "format": "turbo run format"
  },
  "devDependencies": {
    "turbo": "latest",
    "typescript": "^5.0.0",
    "prettier": "^3.0.0",
    "eslint": "^8.0.0"
  }
}
```

### Frontend `package.json`

```json
{
  "name": "@lipu/web",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "type-check": "tsc --noEmit",
    "format": "prettier --write ."
  },
  "dependencies": {
    "next": "15.0.0",
    "react": "19.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.0.0",
    "@shadcn/ui": "latest",
    "framer-motion": "^10.0.0",
    "zustand": "^4.0.0",
    "axios": "^1.0.0"
  }
}
```

### Backend `requirements.txt`

```
# Core
fastapi==0.109.0
uvicorn==0.27.0
python-dotenv==1.0.0

# Database
sqlalchemy==2.0.0
alembic==1.13.0
psycopg2-binary==2.9.0

# AI/ML
langchain==0.1.0
langgraph==latest
openai==1.0.0
qdrant-client==2.0.0

# Validation
pydantic==2.0.0

# Image processing
pillow==10.0.0
opencv-python==4.8.0

# Document processing
python-multipart==0.0.6
PyPDF2==3.0.0

# Testing
pytest==7.4.0
pytest-asyncio==0.21.0

# Monitoring
sentry-sdk==1.39.0
```

---

## Development Workflow

### 1. Setup

```bash
# Clone repository
git clone https://github.com/lipu/lipu-platform.git
cd lipu-platform

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit .env.local with your configuration

# Start development environment
docker-compose up -d
npm run dev
```

### 2. Development

```bash
# Frontend: http://localhost:3000
# Admin: http://localhost:3001
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### 3. Making Changes

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes in specific app
cd apps/web
npm run dev

# Run tests
npm run test

# Format and lint
npm run lint
npm run format

# Commit changes
git add .
git commit -m "feat: description"
git push
```

### 4. Git Workflow

```
main (production)
  ↑
staging (staging environment)
  ↑
develop (development)
  ↑
feature/*, bugfix/*, etc. (feature branches)
```

---

## Build & Deployment

### Frontend Build

```bash
# Next.js production build
cd apps/web
npm run build
npm run start
```

### Backend Build

```bash
# Docker containerization
cd apps/api
docker build -t lipu-api:latest .
```

### Deployment

- **Frontend:** Vercel
- **Backend:** AWS ECS + Docker
- **Database:** AWS RDS PostgreSQL
- **Cache:** AWS ElastiCache

---

## Environment Variables

### Frontend `.env.local`

```
NEXT_PUBLIC_API_URL=https://api.lipu.com/v1
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=...
NEXT_PUBLIC_GA_ID=...
```

### Backend `.env.local`

```
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
QDRANT_URL=http://localhost:6334
OPENAI_API_KEY=...
CLERK_SECRET_KEY=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

---

## Next Steps

- [ ] Initialize git repository
- [ ] Set up GitHub Actions CI/CD
- [ ] Create initial Next.js app
- [ ] Set up FastAPI project
- [ ] Configure PostgreSQL locally
- [ ] Set up development docker-compose.yml

---

**Document Status:** Ready for repository initialization  
**Last Updated:** 2026-06-24
