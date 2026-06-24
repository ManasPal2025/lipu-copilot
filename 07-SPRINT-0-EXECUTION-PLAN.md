# Sprint 0 Execution Plan - Technical Blueprint

**Document Version:** 1.0  
**Role:** Lead Architect + Senior Full Stack Engineer  
**Date:** June 24, 2026  
**Status:** Architecture Review Complete - Ready for Implementation  

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Final Monorepo Structure](#final-monorepo-structure)
3. [Exact Folder Hierarchy](#exact-folder-hierarchy)
4. [Backend Project Structure](#backend-project-structure)
5. [Frontend Project Structure](#frontend-project-structure)
6. [Shared Packages Structure](#shared-packages-structure)
7. [Infrastructure Structure](#infrastructure-structure)
8. [Docker Architecture](#docker-architecture)
9. [Environment Variables Required](#environment-variables-required)
10. [CI/CD Workflow Design](#cicd-workflow-design)
11. [Local Development Setup](#local-development-setup)
12. [Design Gap Analysis](#design-gap-analysis)

---

## Executive Summary

### Architecture Review Status: ✅ COMPLETE

After comprehensive analysis of all architectural documents (00-ARCHITECTURE through 06-SPRINT-PLAN), the system is architecturally sound with **no critical gaps**. The following minor gaps have been identified and addressed in this plan:

**Minor Gaps Identified & Addressed:**
1. ✅ WebSocket connection pooling configuration - Added to backend structure
2. ✅ Rate limiter Redis key schema - Specified in environment section
3. ✅ Database read replica configuration - Noted for Phase 7
4. ✅ Background task queue configuration - Added to backend
5. ✅ Health check endpoints specification - Added to API structure
6. ✅ Error tracking configuration (Sentry) - Added to infrastructure
7. ✅ Logging aggregation strategy - Specified in Docker config
8. ✅ Development vs Production environment distinction - Clarified in Docker
9. ✅ Frontend state management trigger patterns - Added to store section
10. ✅ API versioning migration strategy - Documented in backend routes

---

## Final Monorepo Structure

### Root Level Architecture

```
lipu-platform/                          # GitHub Repository (monorepo root)
├── .github/                            # GitHub specific configurations
├── packages/                           # Shared packages (npm workspaces)
├── apps/                               # Main applications (npm workspaces)
├── docs/                               # Architecture documentation
├── scripts/                            # Utility scripts for development
├── docker-compose.yml                  # Local development orchestration
├── package.json                        # Root workspace definition
├── turbo.json                          # Turborepo configuration (optional)
├── .gitignore                          # Version control exclusions
├── .prettierrc                         # Code formatting
├── .editorconfig                       # Editor configuration
├── README.md                           # Project overview
├── CONTRIBUTING.md                     # Contribution guidelines
└── LICENSE                             # Project license
```

### NPM Workspace Organization

```json
{
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

**Workspace Benefits:**
- Single `node_modules` directory (faster installs)
- Atomic commits across services
- Shared type definitions
- Unified CI/CD pipeline
- Simplified dependency management
- Internal package references

---

## Exact Folder Hierarchy

### Complete Directory Tree

```
lipu-platform/
│
├── .github/
│   ├── workflows/
│   │   ├── lint.yml                    # ESLint + Black linting
│   │   ├── build.yml                   # Docker build & ECR push
│   │   ├── test.yml                    # Unit tests (parallel)
│   │   ├── deploy-staging.yml          # Deploy to staging
│   │   ├── deploy-prod.yml             # Deploy to production
│   │   └── security-scan.yml           # OWASP/security checks
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md        # PR template
│
├── packages/                           # Shared code (private packages)
│   ├── types/                          # Shared TypeScript types
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── api/                    # API response types
│   │   │   │   ├── products.ts
│   │   │   │   ├── orders.ts
│   │   │   │   ├── quotes.ts
│   │   │   │   ├── customers.ts
│   │   │   │   ├── ai.ts
│   │   │   │   └── common.ts
│   │   │   ├── models/                 # Database model types
│   │   │   │   ├── product.ts
│   │   │   │   ├── order.ts
│   │   │   │   └── ...
│   │   │   ├── enums/                  # Shared enumerations
│   │   │   │   ├── order-status.ts
│   │   │   │   ├── user-role.ts
│   │   │   │   └── ...
│   │   │   └── forms/                  # Form validation schemas
│   │   │       ├── product.ts
│   │   │       ├── quote-request.ts
│   │   │       └── ...
│   │   └── tsconfig.json
│   │
│   ├── utils/                          # Shared utilities
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── validators/             # Input validation
│   │   │   │   ├── email.ts
│   │   │   │   ├── phone.ts
│   │   │   │   ├── currency.ts
│   │   │   │   └── ...
│   │   │   ├── formatters/             # Data formatting
│   │   │   │   ├── currency.ts
│   │   │   │   ├── date.ts
│   │   │   │   ├── phone.ts
│   │   │   │   └── ...
│   │   │   ├── constants/              # Global constants
│   │   │   │   ├── api-endpoints.ts
│   │   │   │   ├── regex-patterns.ts
│   │   │   │   └── limits.ts
│   │   │   └── helpers/                # Helper functions
│   │   │       ├── array.ts
│   │   │       ├── object.ts
│   │   │       └── ...
│   │   └── tsconfig.json
│   │
│   └── ui/                             # Shared UI components (optional)
│       ├── package.json
│       ├── src/
│       │   ├── button/
│       │   ├── card/
│       │   ├── modal/
│       │   └── ... (shadcn/ui wrappers)
│       └── tsconfig.json
│
├── apps/
│   ├── web/                            # Main frontend (Next.js)
│   │   ├── package.json
│   │   ├── app/                        # Next.js App Router (routes)
│   │   ├── components/                 # React components (by domain)
│   │   ├── lib/                        # Utilities & hooks
│   │   ├── store/                      # Zustand state management
│   │   ├── styles/                     # Global styles
│   │   ├── public/                     # Static assets
│   │   ├── __tests__/                  # Test files
│   │   ├── middleware.ts               # Next.js middleware
│   │   ├── next.config.js              # Next.js configuration
│   │   ├── tailwind.config.ts          # Tailwind CSS config
│   │   ├── tsconfig.json               # TypeScript config
│   │   ├── .env.example                # Example environment
│   │   ├── .env.local                  # Local environment (gitignored)
│   │   └── README.md
│   │
│   ├── admin/                          # Admin dashboard (future)
│   │   └── (same structure as web/)
│   │
│   └── api/                            # Backend (FastAPI)
│       ├── pyproject.toml              # Python project config
│       ├── requirements.txt            # Python dependencies
│       ├── app/                        # FastAPI application
│       │   ├── __init__.py
│       │   ├── main.py                 # FastAPI initialization
│       │   ├── core/                   # Core configs
│       │   ├── db/                     # Database (ORM models)
│       │   ├── schemas/                # Pydantic schemas (DTOs)
│       │   ├── api/                    # API routes (by version)
│       │   ├── services/               # Business logic
│       │   ├── ai/                     # AI/ML services
│       │   ├── tasks/                  # Background tasks
│       │   ├── events/                 # Event handlers
│       │   ├── middleware/             # Custom middleware
│       │   ├── utils/                  # Utilities
│       │   ├── webhooks/               # Webhook handlers
│       │   └── websocket/              # WebSocket handlers
│       ├── migrations/                 # Alembic DB migrations
│       ├── tests/                      # Test suite
│       ├── alembic.ini                 # Alembic configuration
│       ├── .env.example                # Example environment
│       ├── .env.local                  # Local environment (gitignored)
│       ├── Dockerfile                  # Docker container
│       ├── pytest.ini                  # Pytest configuration
│       ├── .flake8                     # Flake8 linting
│       └── README.md
│
├── docs/
│   ├── architecture/
│   │   ├── 00-ARCHITECTURE.md
│   │   ├── 01-DATABASE-SCHEMA.md
│   │   ├── 02-API-CONTRACTS.md
│   │   ├── 03-FOLDER-STRUCTURE.md
│   │   ├── 04-USER-JOURNEYS.md
│   │   ├── 05-IMPLEMENTATION-ROADMAP.md
│   │   ├── 06-SPRINT-PLAN.md
│   │   └── 07-SPRINT-0-EXECUTION-PLAN.md
│   ├── guides/
│   │   ├── development-setup.md        # Local environment setup
│   │   ├── database-migrations.md      # How to create migrations
│   │   ├── api-development.md          # API endpoint creation
│   │   ├── testing-strategy.md         # Testing approach
│   │   └── deployment.md               # Deployment process
│   └── api/
│       └── openapi.json                # Generated API docs
│
├── scripts/
│   ├── setup.sh                        # First-time setup script
│   ├── docker-setup.sh                 # Docker environment setup
│   ├── seed-data.py                    # Development data seed
│   ├── run-tests.sh                    # Run all tests
│   └── format-code.sh                  # Format code
│
├── docker-compose.yml                  # Local dev environment
├── Dockerfile.api                      # Backend image (if separate)
├── Dockerfile.web                      # Frontend image (if separate)
├── package.json                        # Root workspace config
├── package-lock.json                   # Dependency lock file
├── turbo.json                          # Build orchestration
├── .gitignore                          # Git exclusions
├── .prettierrc                         # Code formatter config
├── .editorconfig                       # Editor conventions
├── README.md                           # Project overview
├── CONTRIBUTING.md                     # Contribution guide
└── LICENSE                             # MIT License
```

**Total Directories in Sprint 0:** 45+ (organized by concern)

---

## Backend Project Structure

### Location: `apps/api/`

#### Core Structure (Detailed)

```
apps/api/
├── app/
│   ├── __init__.py                     # Package marker
│   ├── main.py                         # FastAPI app initialization
│   │                                   # - CORS configuration
│   │                                   # - Middleware setup
│   │                                   # - Route registration
│   │                                   # - Error handlers
│   │                                   # - Startup/shutdown events
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                   # Environment configuration
│   │   │                               # - Database URL
│   │   │                               # - Redis URL
│   │   │                               # - API keys (OpenAI, Stripe, etc)
│   │   │                               # - JWT secret
│   │   │                               # - Environment (dev/staging/prod)
│   │   │
│   │   ├── security.py                 # Security utilities
│   │   │                               # - JWT token creation/validation
│   │   │                               # - Password hashing (bcrypt)
│   │   │                               # - CORS settings
│   │   │                               # - CSRF protection
│   │   │
│   │   ├── constants.py                # Global constants
│   │   │                               # - API versions
│   │   │                               # - Error codes
│   │   │                               # - Status enums
│   │   │                               # - Limits & pagination defaults
│   │   │
│   │   └── logging.py                  # Logging configuration
│   │                                   # - Structured logging
│   │                                   # - Log levels by environment
│   │                                   # - Integration with services
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── session.py                  # SQLAlchemy session factory
│   │   │                               # - Connection pooling
│   │   │                               # - Session lifecycle
│   │   │                               # - Transaction management
│   │   │
│   │   ├── base.py                     # Base model class
│   │   │                               # - Declarative base
│   │   │                               # - Common columns (id, timestamps)
│   │   │                               # - Query helpers
│   │   │
│   │   └── models/                     # ORM models (by domain)
│   │       ├── __init__.py
│   │       ├── organization.py         # Organization, multi-tenant
│   │       ├── user.py                 # User, Clerk integration
│   │       ├── product.py              # Product, ProductVariant, Category
│   │       ├── order.py                # Order, OrderItem
│   │       ├── quote.py                # Quote, QuoteItem
│   │       ├── customer.py             # Customer, CustomerProject
│   │       ├── inventory.py            # Stock, Transactions
│   │       ├── ai.py                   # Documents, Chunks, Conversations
│   │       └── audit.py                # AuditLog (immutable)
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── base.py                     # Base schemas
│   │   │                               # - Response envelope
│   │   │                               # - Pagination schema
│   │   │                               # - Error schema
│   │   │
│   │   ├── product.py                  # Product DTOs
│   │   │                               # - ProductCreate
│   │   │                               # - ProductResponse
│   │   │                               # - ProductVariantResponse
│   │   │
│   │   ├── order.py                    # Order DTOs
│   │   ├── quote.py                    # Quote DTOs
│   │   ├── customer.py                 # Customer DTOs
│   │   ├── inventory.py                # Inventory DTOs
│   │   ├── ai.py                       # AI service DTOs
│   │   └── auth.py                     # Auth DTOs
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                 # POST /auth/callback, /auth/logout
│   │   │   ├── products.py             # GET/POST /products, /products/:id
│   │   │   ├── orders.py               # GET/POST /orders, /orders/:id
│   │   │   ├── quotes.py               # GET/POST /quotes, /quotes/:id
│   │   │   ├── customers.py            # GET/POST /customers, /customers/:id
│   │   │   ├── inventory.py            # GET/POST /inventory
│   │   │   ├── ai.py                   # POST /ai/chat, /ai/quote, /ai/visualize
│   │   │   ├── analytics.py            # GET /analytics/*
│   │   │   ├── uploads.py              # POST /uploads
│   │   │   ├── health.py               # GET /health (readiness/liveness)
│   │   │   └── websocket.py            # WS /ws/chat
│   │   └── v2/ (empty, for future)
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── product_service.py          # Product business logic
│   │   │                               # - get_products()
│   │   │                               # - create_product()
│   │   │                               # - search_products()
│   │   │
│   │   ├── order_service.py            # Order business logic
│   │   ├── quote_service.py            # Quote business logic
│   │   ├── customer_service.py         # Customer business logic
│   │   ├── inventory_service.py        # Inventory business logic
│   │   ├── payment_service.py          # Payment/Stripe integration
│   │   ├── email_service.py            # Email/SendGrid integration
│   │   ├── file_service.py             # S3 file operations
│   │   └── notification_service.py     # Notifications (email, SMS)
│   │
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── document_processor.py   # PDF/document ingestion
│   │   │   ├── embedder.py            # OpenAI embeddings
│   │   │   ├── retriever.py           # Qdrant search
│   │   │   └── vector_store.py        # Qdrant connection manager
│   │   │
│   │   ├── agents/
│   │   │   ├── __init__.py
│   │   │   ├── sales_agent.py         # LangGraph sales conversation
│   │   │   ├── quote_generator.py     # AI pricing logic
│   │   │   └── design_consultant.py   # Style recommendations
│   │   │
│   │   ├── vision/
│   │   │   ├── __init__.py
│   │   │   ├── window_detector.py     # YOLO or OpenAI Vision
│   │   │   └── image_generator.py     # DALL-E 3 integration
│   │   │
│   │   ├── llm/
│   │   │   ├── __init__.py
│   │   │   ├── client.py              # OpenAI + fallback logic
│   │   │   ├── prompts.py             # Prompt templates (LangChain)
│   │   │   └── chains.py              # LangChain chains/LangGraph workflows
│   │   │
│   │   └── models.py                   # Pydantic schemas for AI
│   │
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_config.py (if Celery)  # Celery configuration
│   │   ├── queue.py                   # Queue initialization
│   │   ├── email_tasks.py             # Email sending (async)
│   │   ├── inventory_tasks.py         # Low-stock alerts (async)
│   │   ├── analytics_tasks.py         # Aggregation jobs (async)
│   │   ├── ai_tasks.py                # Long-running AI tasks (async)
│   │   └── cleanup_tasks.py           # Data cleanup (async)
│   │
│   ├── events/
│   │   ├── __init__.py
│   │   ├── event_bus.py               # Event dispatcher
│   │   ├── order_events.py            # OrderCreated, OrderShipped, etc
│   │   ├── quote_events.py            # QuoteGenerated, QuoteAccepted
│   │   ├── inventory_events.py        # InventoryLow, StockReceived
│   │   └── ai_events.py               # AIConversationStarted, etc
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py         # JWT validation
│   │   ├── logging_middleware.py      # Request/response logging
│   │   ├── error_handler.py           # Global error handling
│   │   ├── rate_limiter.py            # Redis-based rate limiting
│   │   └── request_id.py              # Request tracing
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py              # Input validation helpers
│   │   ├── formatters.py              # Data formatting
│   │   ├── decorators.py              # Useful decorators
│   │   ├── helpers.py                 # Common helpers
│   │   └── exceptions.py              # Custom exceptions
│   │
│   ├── webhooks/
│   │   ├── __init__.py
│   │   ├── clerk.py                   # Clerk webhook handler
│   │   ├── stripe.py                  # Stripe webhook handler
│   │   └── external_services.py       # Other webhooks
│   │
│   └── websocket/
│       ├── __init__.py
│       ├── connection_manager.py      # WebSocket connection pooling
│       └── events.py                  # WebSocket event handlers
│
├── migrations/                         # Alembic migrations
│   ├── env.py
│   ├── script.py.mako
│   ├── versions/
│   │   ├── 0001_initial_schema.py
│   │   └── (future versions)
│   └── alembic.ini (root)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # pytest fixtures
│   ├── test_products.py                # Product tests
│   ├── test_orders.py                  # Order tests
│   ├── test_quotes.py                  # Quote tests
│   ├── test_ai_agent.py                # AI agent tests
│   └── e2e/ (future)
│
├── pyproject.toml                      # Python project metadata
├── requirements.txt                    # Python dependencies
├── requirements-dev.txt                # Dev dependencies
├── alembic.ini                         # Alembic config (symlink or copy)
├── pytest.ini                          # Pytest configuration
├── .flake8                             # Flake8 linting config
├── .env.example                        # Example environment file
├── .env.local                          # Local environment (gitignored)
├── Dockerfile                          # Docker image
├── .dockerignore                       # Docker build exclusions
└── README.md                           # Backend documentation
```

#### Backend Dependencies Organization

```
requirements.txt:
├── FastAPI (web framework)
├── SQLAlchemy (ORM)
├── Pydantic (validation)
├── alembic (migrations)
├── psycopg2-binary (PostgreSQL)
├── redis (caching)
├── python-jose (JWT)
├── langchain (AI chains)
├── langgraph (AI workflows)
├── openai (LLM)
├── qdrant-client (vector DB)
├── pillow (image processing)
├── opencv-python (vision)
├── pydantic-settings (env config)
├── python-multipart (file uploads)
├── httpx (async HTTP)
├── stripe (payments)
├── sendgrid (email)
├── twilio (SMS)
└── python-dotenv (env loading)

requirements-dev.txt:
├── pytest (testing)
├── pytest-asyncio (async tests)
├── pytest-cov (coverage)
├── black (formatting)
├── flake8 (linting)
├── mypy (type checking)
└── ipython (REPL)
```

---

## Frontend Project Structure

### Location: `apps/web/`

#### Detailed Component Organization

```
apps/web/
├── app/                                # Next.js App Router (routes & layouts)
│   ├── (marketing)/                    # Group: public pages
│   │   ├── layout.tsx                  # Marketing layout (navbar, footer)
│   │   ├── page.tsx                    # Homepage (/page)
│   │   ├── about/page.tsx              # /about
│   │   ├── products/
│   │   │   ├── page.tsx                # /products (listing)
│   │   │   └── [slug]/
│   │   │       └── page.tsx            # /products/:slug (detail)
│   │   ├── gallery/page.tsx            # /gallery
│   │   ├── projects/page.tsx           # /projects (portfolio)
│   │   ├── testimonials/page.tsx       # /testimonials
│   │   ├── blog/
│   │   │   ├── page.tsx                # /blog (list)
│   │   │   └── [slug]/page.tsx         # /blog/:slug (post detail)
│   │   ├── contact/page.tsx            # /contact
│   │   ├── faq/page.tsx                # /faq
│   │   ├── quote-request/page.tsx      # /quote-request (not authenticated)
│   │   ├── house-visualizer/page.tsx   # /house-visualizer
│   │   ├── sitemap.xml.ts              # Dynamic sitemap (SEO)
│   │   └── robots.txt.ts               # Robots file (SEO)
│   │
│   ├── (auth)/                         # Group: authentication pages
│   │   ├── layout.tsx                  # Auth layout (centered)
│   │   ├── login/page.tsx              # /login
│   │   ├── register/page.tsx           # /register
│   │   ├── callback/page.tsx           # /callback (Clerk redirect)
│   │   └── forgot-password/page.tsx    # /forgot-password
│   │
│   ├── (customer)/                     # Group: protected customer routes
│   │   ├── layout.tsx                  # Customer layout (sidebar, nav)
│   │   ├── dashboard/page.tsx          # /dashboard
│   │   ├── profile/page.tsx            # /profile
│   │   ├── projects/
│   │   │   ├── page.tsx                # /projects (list)
│   │   │   └── [id]/page.tsx           # /projects/:id (detail)
│   │   ├── quotes/
│   │   │   ├── page.tsx                # /quotes (list)
│   │   │   └── [id]/page.tsx           # /quotes/:id (detail)
│   │   ├── orders/
│   │   │   ├── page.tsx                # /orders (list)
│   │   │   └── [id]/page.tsx           # /orders/:id (tracking)
│   │   ├── invoices/page.tsx           # /invoices
│   │   ├── support-tickets/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── saved-designs/page.tsx      # /saved-designs
│   │   └── ai-conversations/
│   │       ├── page.tsx                # /ai-conversations (list)
│   │       └── [id]/page.tsx           # /ai-conversations/:id (detail)
│   │
│   ├── (admin)/                        # Group: protected admin routes
│   │   ├── layout.tsx                  # Admin layout (sidebar)
│   │   ├── dashboard/page.tsx          # /admin/dashboard
│   │   ├── inventory/
│   │   │   ├── page.tsx                # /admin/inventory
│   │   │   └── [id]/page.tsx           # /admin/inventory/:id
│   │   ├── products/
│   │   │   ├── page.tsx                # /admin/products
│   │   │   └── [id]/page.tsx
│   │   ├── orders/
│   │   │   ├── page.tsx
│   │   │   └── [id]/page.tsx
│   │   ├── quotes/page.tsx
│   │   ├── customers/page.tsx
│   │   ├── projects/page.tsx
│   │   ├── leads/page.tsx
│   │   ├── employees/page.tsx
│   │   ├── analytics/page.tsx
│   │   ├── reports/page.tsx
│   │   ├── content/page.tsx            # CMS
│   │   ├── ai-management/page.tsx      # AI configuration
│   │   ├── settings/page.tsx
│   │   └── audit-logs/page.tsx
│   │
│   ├── api/                            # Next.js API routes
│   │   ├── auth/
│   │   │   ├── callback/route.ts       # POST /api/auth/callback
│   │   │   └── logout/route.ts         # POST /api/auth/logout
│   │   ├── uploads/
│   │   │   └── route.ts                # POST /api/uploads
│   │   ├── webhooks/
│   │   │   ├── clerk/route.ts          # POST /api/webhooks/clerk
│   │   │   └── stripe/route.ts         # POST /api/webhooks/stripe
│   │   └── trpc/
│   │       └── [trpc]/route.ts         # tRPC endpoints (optional)
│   │
│   ├── layout.tsx                      # Root layout
│   ├── error.tsx                       # Error boundary
│   ├── not-found.tsx                   # 404 page
│   └── loading.tsx                     # Loading skeleton
│
├── components/                         # React components (by domain)
│   ├── ui/                             # Base UI components (Shadcn)
│   │   ├── button.tsx                  # Shadcn Button wrapper
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── form.tsx
│   │   ├── modal.tsx
│   │   ├── table.tsx
│   │   ├── tabs.tsx
│   │   ├── sidebar.tsx
│   │   ├── navbar.tsx
│   │   ├── dropdown.tsx
│   │   ├── toast.tsx
│   │   ├── skeleton.tsx
│   │   ├── breadcrumb.tsx
│   │   ├── pagination.tsx
│   │   └── ... (other UI components)
│   │
│   ├── marketing/                      # Marketing page components
│   │   ├── hero.tsx
│   │   ├── features.tsx
│   │   ├── testimonials.tsx
│   │   ├── cta-section.tsx
│   │   ├── pricing-table.tsx
│   │   ├── gallery-section.tsx
│   │   ├── blog-preview.tsx
│   │   └── footer.tsx
│   │
│   ├── customer/                       # Customer portal components
│   │   ├── dashboard-widget.tsx
│   │   ├── project-card.tsx
│   │   ├── quote-preview.tsx
│   │   ├── order-status-tracker.tsx
│   │   ├── invoice-viewer.tsx
│   │   ├── design-gallery.tsx
│   │   └── support-ticket-card.tsx
│   │
│   ├── admin/                          # Admin dashboard components
│   │   ├── data-table.tsx              # Reusable data table
│   │   ├── charts/
│   │   │   ├── sales-chart.tsx
│   │   │   ├── revenue-chart.tsx
│   │   │   └── trends-chart.tsx
│   │   ├── filters/
│   │   │   ├── date-range-picker.tsx
│   │   │   ├── status-filter.tsx
│   │   │   └── search-filter.tsx
│   │   ├── modals/
│   │   │   ├── create-product-modal.tsx
│   │   │   ├── edit-order-modal.tsx
│   │   │   └── add-inventory-modal.tsx
│   │   ├── widgets/
│   │   │   ├── revenue-widget.tsx
│   │   │   ├── orders-widget.tsx
│   │   │   └── inventory-widget.tsx
│   │   └── dashboard/
│   │       └── admin-dashboard.tsx
│   │
│   ├── ai/                             # AI feature components
│   │   ├── chat-interface.tsx          # Chat UI
│   │   ├── message-item.tsx            # Message display
│   │   ├── typing-indicator.tsx
│   │   ├── visualization-generator.tsx # House viz uploader
│   │   ├── quote-generator.tsx         # AI quote form
│   │   ├── design-consultant.tsx       # Style recommendations
│   │   └── ai-loading.tsx              # Loading state
│   │
│   ├── shared/                         # Reusable components
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   ├── breadcrumb.tsx
│   │   ├── pagination.tsx
│   │   ├── loading-spinner.tsx
│   │   ├── error-boundary.tsx
│   │   ├── toast-notification.tsx
│   │   ├── confirmation-dialog.tsx
│   │   ├── image-uploader.tsx
│   │   └── form-wrapper.tsx
│   │
│   └── icons/                          # Icon components
│       ├── product-icon.tsx
│       ├── cart-icon.tsx
│       ├── heart-icon.tsx
│       └── ... (SVG icon components)
│
├── lib/                                # Utility functions & hooks
│   ├── api.ts                          # Axios instance with interceptors
│   ├── auth.ts                         # Clerk/Auth utilities
│   ├── validation.ts                   # Zod schemas for forms
│   ├── formatting.ts                   # String/number/date formatting
│   ├── constants.ts                    # Global constants & enums
│   ├── hooks/
│   │   ├── useApi.ts                   # Custom API hook
│   │   ├── useAuth.ts                  # Auth hook (Clerk)
│   │   ├── useForm.ts                  # Form hook
│   │   ├── usePagination.ts            # Pagination hook
│   │   ├── useLocalStorage.ts
│   │   ├── useDebounce.ts
│   │   ├── useMobileDetect.ts
│   │   └── useWebSocket.ts             # WebSocket connection
│   └── utils/
│       ├── cn.ts                       # Tailwind class merge
│       ├── date.ts                     # Date utilities
│       ├── storage.ts                  # LocalStorage utilities
│       └── error-handler.ts            # Error parsing
│
├── store/                              # Zustand state management
│   ├── auth-store.ts                   # Authentication state
│   ├── cart-store.ts                   # Shopping cart state
│   ├── ui-store.ts                     # UI state (sidebar, theme)
│   ├── customer-store.ts               # Customer portal state
│   ├── admin-store.ts                  # Admin panel state
│   └── ai-store.ts                     # AI chat state
│
├── styles/
│   ├── globals.css                     # Global styles & resets
│   ├── variables.css                   # CSS variables (colors, spacing)
│   ├── animations.css                  # Global animations
│   └── themes.css                      # Theme definitions
│
├── public/                             # Static assets
│   ├── images/
│   │   ├── logo.svg
│   │   ├── logo-dark.svg
│   │   ├── products/
│   │   │   └── sample-images/
│   │   ├── testimonials/
│   │   ├── gallery/
│   │   └── ...
│   ├── videos/
│   │   └── product-demo.mp4
│   ├── documents/
│   │   └── brochures/
│   ├── icons/
│   └── fonts/
│       └── custom-fonts/
│
├── __tests__/                          # Test files
│   ├── unit/
│   │   ├── lib/
│   │   │   └── formatting.test.ts
│   │   └── utils/
│   │       └── validators.test.ts
│   ├── integration/
│   │   ├── auth/
│   │   │   └── login-flow.test.tsx
│   │   └── api/
│   │       └── product-listing.test.tsx
│   └── e2e/
│       ├── customer-flow.spec.ts
│       ├── admin-flow.spec.ts
│       └── quote-request.spec.ts
│
├── middleware.ts                       # Next.js middleware
│                                       # - Auth protection
│                                       # - Route redirects
│                                       # - Request logging
│
├── next.config.js                      # Next.js config
│                                       # - Image optimization
│                                       # - Redirects
│                                       # - Rewrites
│
├── tailwind.config.ts                  # Tailwind CSS config
│                                       # - Custom theme
│                                       # - Brand colors
│
├── postcss.config.js                   # PostCSS config (Tailwind)
├── tsconfig.json                       # TypeScript config
├── jest.config.js                      # Jest testing config
├── playwright.config.ts                # E2E testing config
├── .env.example                        # Example environment file
├── .env.local                          # Local environment (gitignored)
├── .env.staging                        # Staging environment (gitignored)
├── .env.production                     # Prod environment (gitignored)
├── package.json                        # NPM dependencies
├── package-lock.json                   # Dependency lock
├── README.md                           # Frontend documentation
└── Dockerfile                          # Docker image (optional)
```

---

## Shared Packages Structure

### Location: `packages/`

#### Package: `types/`

```
packages/types/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts                        # Barrel export
│   │
│   ├── api/                            # API response types
│   │   ├── common.ts                   # ResponseEnvelope, Pagination
│   │   ├── products.ts                 # ProductResponse, variants
│   │   ├── orders.ts                   # OrderResponse, OrderItem
│   │   ├── quotes.ts                   # QuoteResponse, items
│   │   ├── customers.ts                # CustomerResponse
│   │   ├── ai.ts                       # AI service responses
│   │   ├── inventory.ts                # Stock responses
│   │   └── errors.ts                   # Error response types
│   │
│   ├── models/                         # Database model types
│   │   ├── product.ts                  # Product type definitions
│   │   ├── order.ts
│   │   ├── quote.ts
│   │   ├── customer.ts
│   │   ├── inventory.ts
│   │   ├── user.ts
│   │   └── organization.ts
│   │
│   ├── enums/                          # Shared enumerations
│   │   ├── order-status.ts             # enum OrderStatus
│   │   ├── quote-status.ts
│   │   ├── user-role.ts                # enum UserRole
│   │   ├── inventory-status.ts
│   │   ├── payment-status.ts
│   │   └── ai-model-type.ts
│   │
│   ├── forms/                          # Form validation schemas (Zod)
│   │   ├── product.ts
│   │   ├── quote-request.ts
│   │   ├── contact.ts
│   │   ├── login.ts
│   │   └── profile-update.ts
│   │
│   └── constants/                      # Shared constants
│       ├── api-endpoints.ts
│       ├── regex-patterns.ts
│       ├── limits.ts
│       └── currencies.ts
│
└── dist/                               # Compiled output
```

#### Package: `utils/`

```
packages/utils/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts                        # Barrel export
│   │
│   ├── validators/                     # Input validation
│   │   ├── email.ts
│   │   ├── phone.ts
│   │   ├── currency.ts
│   │   ├── date.ts
│   │   ├── url.ts
│   │   └── index.ts
│   │
│   ├── formatters/                     # Data formatting
│   │   ├── currency.ts
│   │   ├── date.ts
│   │   ├── phone.ts
│   │   ├── address.ts
│   │   ├── truncate.ts
│   │   └── index.ts
│   │
│   ├── constants/                      # Global constants
│   │   ├── api-endpoints.ts
│   │   ├── regex-patterns.ts
│   │   ├── pagination.ts
│   │   └── index.ts
│   │
│   └── helpers/                        # Helper functions
│       ├── array.ts
│       ├── object.ts
│       ├── string.ts
│       ├── date.ts
│       └── index.ts
│
└── dist/                               # Compiled output
```

#### Package: `ui/` (Optional shared components)

```
packages/ui/
├── package.json
├── src/
│   ├── button/
│   │   ├── button.tsx
│   │   └── button.stories.tsx
│   ├── card/
│   │   ├── card.tsx
│   │   └── card.stories.tsx
│   ├── index.ts
│   └── ...
└── dist/
```

---

## Infrastructure Structure

### High-Level Infrastructure Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE LAYERS                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 1: CLIENT                                           │
│  ├─ Browser/Web Client                                     │
│  └─ Mobile Client (Future)                                 │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 2: CDN & API GATEWAY                                │
│  ├─ CloudFront (Images, static files)                      │
│  ├─ API Gateway (Rate limiting, auth, routing)            │
│  └─ DDoS Protection (AWS Shield)                           │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 3: APPLICATION                                      │
│  ├─ Frontend: Vercel (Next.js SPA)                         │
│  ├─ Backend: AWS ECS/Fargate (FastAPI containers)         │
│  └─ Load Balancer (Distribute traffic)                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 4: DATA LAYER                                       │
│  ├─ Primary DB: AWS RDS PostgreSQL (Multi-AZ)            │
│  ├─ Cache: AWS ElastiCache Redis                          │
│  ├─ Vector DB: Qdrant (Self-hosted or managed)            │
│  ├─ Object Storage: AWS S3                                │
│  └─ Search: PostgreSQL FTS (no Elasticsearch needed)      │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Layer 5: MONITORING & LOGGING                             │
│  ├─ Metrics: Prometheus/CloudWatch                        │
│  ├─ Logs: ELK Stack or CloudWatch Logs                    │
│  ├─ Tracing: Jaeger or AWS X-Ray                          │
│  ├─ Error Tracking: Sentry                                │
│  └─ Uptime Monitoring: Datadog or Uptime.com              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure for Infrastructure Code

```
infrastructure/                        # IaC (Infrastructure as Code)
├── terraform/                         # Terraform configs (if used)
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── networking.tf
│   ├── rds.tf
│   ├── redis.tf
│   ├── s3.tf
│   ├── ecs.tf
│   ├── iam.tf
│   └── environments/
│       ├── dev.tfvars
│       ├── staging.tfvars
│       └── production.tfvars
│
├── kubernetes/                        # K8s configs (if using)
│   ├── namespaces/
│   ├── deployments/
│   ├── services/
│   ├── configmaps/
│   ├── secrets/
│   └── ingress/
│
├── docker/                            # Docker configurations
│   ├── api.dockerfile
│   ├── web.dockerfile
│   └── nginx.dockerfile (reverse proxy)
│
└── monitoring/                        # Monitoring configs
    ├── prometheus-config.yml
    ├── grafana-dashboards/
    ├── alerts.yml
    └── elk-config/
```

---

## Docker Architecture

### Sprint 0 Local Development (docker-compose.yml)

```
Services in docker-compose.yml:

1. PostgreSQL 15
   ├─ Port: 5432 (internal), 5433 (host)
   ├─ Volume: postgres_data
   ├─ Environment: DATABASE_URL, POSTGRES_PASSWORD
   └─ Health check: pg_isready

2. Redis 7
   ├─ Port: 6379 (internal), 6380 (host)
   ├─ Volume: redis_data
   ├─ Configuration: redis.conf (persistence)
   └─ Health check: redis-cli PING

3. PgAdmin 4
   ├─ Port: 5050 (pgadmin.localhost)
   ├─ Purpose: Database GUI for development
   ├─ Credentials: PGADMIN_DEFAULT_EMAIL, PASSWORD
   └─ Volume: pgadmin_data

4. Qdrant (Vector DB)
   ├─ Port: 6333 (REST), 6334 (gRPC)
   ├─ Volume: qdrant_data
   ├─ Purpose: Vector embeddings storage
   └─ Snapshots: qdrant_snapshots

5. Localstack (AWS Simulation)
   ├─ Port: 4566 (all AWS services)
   ├─ Services: S3, SQS, SNS, etc.
   ├─ Volume: localstack_data
   └─ Purpose: Local AWS testing

6. FastAPI Backend
   ├─ Port: 8000
   ├─ Build: ./apps/api/Dockerfile
   ├─ Environment: Loaded from .env.local
   ├─ Dependencies: postgres, redis
   └─ Volumes: apps/api (code mount)

7. Next.js Frontend
   ├─ Port: 3000
   ├─ Build: ./apps/web/node_modules
   ├─ Environment: Loaded from .env.local
   ├─ Dependencies: backend (wait for health check)
   └─ Volumes: apps/web (code mount)

8. Nginx (Optional)
   ├─ Port: 80 (localhost), 443 (HTTPS)
   ├─ Purpose: Reverse proxy, SSL termination
   └─ Config: nginx.conf
```

### Dockerfile for Backend (apps/api/Dockerfile)

```dockerfile
Stages:
1. Builder Stage
   ├─ Base: python:3.11-slim
   ├─ Install: build dependencies
   ├─ Copy: requirements.txt
   └─ Build: pip install --user

2. Runtime Stage
   ├─ Base: python:3.11-slim
   ├─ Copy: --from=builder /root/.local
   ├─ Copy: app code
   ├─ Set: WORKDIR /app
   ├─ Expose: 8000
   ├─ CMD: uvicorn app.main:app --host 0.0.0.0 --port 8000
   └─ Health: /health endpoint
```

### Dockerfile for Frontend (apps/web/Dockerfile)

```dockerfile
Stages:
1. Builder Stage
   ├─ Base: node:20-alpine
   ├─ Copy: package.json, package-lock.json
   ├─ Run: npm ci
   ├─ Copy: app source
   └─ Run: npm run build

2. Runtime Stage
   ├─ Base: node:20-alpine
   ├─ Copy: --from=builder /app/.next
   ├─ Copy: public directory
   ├─ Copy: package.json
   ├─ Set: WORKDIR /app
   ├─ Expose: 3000
   ├─ CMD: npm run start
   └─ Health: http://localhost:3000/health
```

---

## Environment Variables Required

### Frontend Environment (.env.local)

```env
# API Configuration
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_API_TIMEOUT=30000

# Authentication (Clerk)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/login
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/register
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard

# Third-party Services
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=...

# Analytics & Monitoring
NEXT_PUBLIC_SENTRY_DSN=https://...
NEXT_PUBLIC_GA_ID=G-...

# File Upload
NEXT_PUBLIC_MAX_FILE_SIZE=10485760  # 10MB
NEXT_PUBLIC_ALLOWED_FILE_TYPES=image/jpeg,image/png,application/pdf

# Features
NEXT_PUBLIC_ENABLE_VISUALIZATION=true
NEXT_PUBLIC_ENABLE_AI_CHAT=true
NEXT_PUBLIC_ENABLE_HOUSE_TOUR=false

# Environment
NODE_ENV=development
```

### Backend Environment (.env.local)

```env
# Application
APP_NAME=LIPU API
APP_VERSION=0.1.0
APP_ENV=development
DEBUG=true

# Database
DATABASE_URL=postgresql://user:password@postgres:5432/lipu_dev
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_CACHE_TTL=3600
REDIS_SESSION_TTL=86400

# Qdrant (Vector DB)
QDRANT_URL=http://qdrant:6333
QDRANT_API_KEY=  # Optional if not secured

# Authentication
JWT_SECRET=your-super-secret-key-do-not-share
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
CLERK_FRONTEND_API=https://...
CLERK_API_KEY=sk_test_...

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_ORGANIZATION=org-...  # Optional

# AWS Services
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_REGION=us-east-1
AWS_S3_BUCKET=lipu-dev
AWS_S3_ENDPOINT_URL=http://localstack:4566  # For local dev
AWS_STORAGE_LOCATION=products/  # S3 prefix

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# SendGrid (Email)
SENDGRID_API_KEY=SG....
SENDGRID_FROM_EMAIL=noreply@lipu.com

# Twilio (SMS)
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
TWILIO_FROM_NUMBER=+1...

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=1000
RATE_LIMIT_WINDOW=3600

# Celery/Background Tasks
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
ALLOWED_HOSTS=localhost,127.0.0.1,api.local
```

### Database Environment (.env.local for postgres service)

```env
POSTGRES_USER=lipu_user
POSTGRES_PASSWORD=lipu_password_dev
POSTGRES_DB=lipu_dev
POSTGRES_INITDB_ARGS=--encoding=UTF8
```

### Docker Compose Environment (.env file for compose)

```env
COMPOSE_PROJECT_NAME=lipu-platform
POSTGRES_VERSION=15
REDIS_VERSION=7
QDRANT_VERSION=latest
NODE_VERSION=20
PYTHON_VERSION=3.11

# Service Ports
POSTGRES_PORT=5433
REDIS_PORT=6380
PGADMIN_PORT=5050
QDRANT_PORT=6333
BACKEND_PORT=8000
FRONTEND_PORT=3000

# Volumes
POSTGRES_DATA_PATH=./data/postgres
REDIS_DATA_PATH=./data/redis
QDRANT_DATA_PATH=./data/qdrant
```

---

## CI/CD Workflow Design

### GitHub Actions Workflows

#### 1. Lint Workflow (.github/workflows/lint.yml)

```yaml
Trigger:
├─ On: push, pull_request
├─ Branches: main, staging, develop
└─ Paths: changes to .ts, .tsx, .py files

Jobs:
├─ Frontend Lint (Node 20)
│  ├─ Checkout
│  ├─ Setup Node
│  ├─ npm ci (install dependencies)
│  ├─ npm run lint (ESLint)
│  ├─ npm run type-check (TypeScript)
│  └─ npm run format:check (Prettier)
│
└─ Backend Lint (Python 3.11)
   ├─ Checkout
   ├─ Setup Python
   ├─ pip install -r requirements.txt
   ├─ black --check (format check)
   ├─ flake8 (linting)
   └─ mypy (type checking)
```

#### 2. Build Workflow (.github/workflows/build.yml)

```yaml
Trigger:
├─ On: push (main branch)
└─ After: lint passes

Jobs:
├─ Build Backend Docker Image
│  ├─ Checkout
│  ├─ Setup Docker Buildx
│  ├─ Build image: ghcr.io/lipu/api:${GITHUB_SHA}
│  ├─ Build image: ghcr.io/lipu/api:latest
│  ├─ Run tests in container
│  └─ Push to GitHub Container Registry
│
└─ Build Frontend Docker Image
   ├─ Checkout
   ├─ Setup Docker Buildx
   ├─ Build image: ghcr.io/lipu/web:${GITHUB_SHA}
   ├─ Build image: ghcr.io/lipu/web:latest
   └─ Push to GitHub Container Registry
```

#### 3. Test Workflow (.github/workflows/test.yml)

```yaml
Trigger:
├─ On: push, pull_request
└─ Parallel: runs on multiple Python/Node versions

Jobs:
├─ Frontend Tests
│  ├─ Jest unit tests
│  ├─ React Testing Library
│  ├─ Coverage reports
│  └─ Fail if coverage < 80%
│
├─ Backend Tests
│  ├─ pytest unit tests
│  ├─ pytest integration tests
│  ├─ Coverage reports
│  └─ Fail if coverage < 80%
│
└─ E2E Tests (optional for PR)
   ├─ Start services (docker-compose)
   ├─ Playwright tests
   ├─ Screenshots on failure
   └─ Upload artifacts
```

#### 4. Deploy to Staging (.github/workflows/deploy-staging.yml)

```yaml
Trigger:
├─ On: push to staging branch (manual)
└─ After: lint + build pass

Steps:
├─ Build images
├─ Update AWS ECS task definition
├─ Update ECS service
├─ Run smoke tests
├─ Notify team on Slack
└─ Log deployment to audit trail
```

#### 5. Deploy to Production (.github/workflows/deploy-prod.yml)

```yaml
Trigger:
├─ On: release tag created (manual)
└─ Requires: approval + successful staging deployment

Steps:
├─ Verify version matches tag
├─ Build/push images
├─ Run database migrations
├─ Update ECS task definition
├─ Canary deployment (10% traffic)
├─ Health checks (2 min wait)
├─ Full rollout (100% traffic)
├─ Run smoke tests
├─ Notify stakeholders
└─ Log deployment
```

### Deployment Pipeline Stages

```
Development (Local)
       ↓
   Lint → Type Check → Tests
       ↓
Push to develop branch
       ↓
CI/CD Build (GitHub Actions)
       ↓
Staging Environment
       ↓
QA Testing (24 hours)
       ↓
Merge to main / Create Release
       ↓
CI/CD Build
       ↓
Production Environment (Canary → Full)
       ↓
Monitoring & Alerts
```

---

## Local Development Setup

### Initial Setup Process (Day 1)

#### Step 1: Prerequisites Installation
```
Required:
├─ Docker Desktop (4.0+)
├─ Node.js 20 LTS
├─ Python 3.11
├─ Git 2.30+
├─ VS Code (recommended)
└─ Postman or Insomnia (API testing)

Verification:
├─ docker --version
├─ node --version
├─ python --version
└─ git --version
```

#### Step 2: Repository Clone
```
git clone https://github.com/lipu/lipu-platform.git
cd lipu-platform
git checkout develop
```

#### Step 3: Environment Setup

**For Backend:**
```
cd apps/api
cp .env.example .env.local
# Edit .env.local with local values
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

**For Frontend:**
```
cd apps/web
cp .env.example .env.local
# Edit .env.local with Clerk credentials
npm install
```

#### Step 4: Docker Services

```
# From project root
docker-compose up -d

# Verify services
docker-compose ps
docker-compose logs postgres
docker-compose logs redis
```

#### Step 5: Database Initialization

```
# Run migrations
cd apps/api
alembic upgrade head

# Seed development data
python scripts/seed_data.py
```

#### Step 6: Start Development Servers

```
# Terminal 1: Backend
cd apps/api
source venv/bin/activate
uvicorn app.main:app --reload --port 8000

# Terminal 2: Frontend
cd apps/web
npm run dev

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Development Workflow

```
Daily workflow:

1. Start: docker-compose up -d
2. Checkout: git checkout -b feature/feature-name
3. Make changes
4. Test: npm run test (frontend), pytest (backend)
5. Lint: npm run lint, black --check
6. Commit: git add . && git commit -m "..."
7. Push: git push origin feature/feature-name
8. Create PR on GitHub
9. Wait for CI/CD to pass
10. Merge after review
11. Deploy to staging
```

### Troubleshooting Guide

```
Common Issues:

1. Docker port conflicts
   Solution: docker-compose down, docker system prune
   
2. Database connection refused
   Solution: docker-compose logs postgres, ensure DB is running
   
3. Redis connection error
   Solution: docker-compose restart redis
   
4. Node_modules issues
   Solution: rm -rf node_modules, npm ci (clean install)
   
5. Python dependency conflicts
   Solution: pip install --upgrade pip, pip install -r requirements.txt
   
6. Environment variables not loaded
   Solution: Verify .env.local exists, source venv/bin/activate
```

---

## Design Gap Analysis

### Comprehensive Review Results

**Overall Assessment:** ✅ **ARCHITECTURE IS SOUND**

#### Analysis Summary

After thorough analysis of all documents (00-ARCHITECTURE through 06-SPRINT-PLAN), the system architecture demonstrates:

✅ **Strengths:**
- Comprehensive service layering (3-tier + microservices)
- Well-defined API contracts with OpenAPI spec
- Detailed database schema with optimization
- Clear user journeys and personas
- Production-ready technology choices
- Well-organized folder structure

---

### Identified Gaps & Solutions

#### Gap 1: WebSocket Connection Pooling ❌ → ✅ FIXED

**Issue:** Connection pooling strategy for WebSocket connections not specified.

**Solution Added to Backend Structure:**
```
apps/api/app/websocket/
├── connection_manager.py    # Manages active connections
├── events.py               # WebSocket event handlers
└── pools.py               # Connection pooling strategy

Configuration:
├─ Max connections: 1,000 per instance
├─ Timeout: 30 seconds idle
├─ Heartbeat: Every 15 seconds
└─ Graceful disconnect handling
```

---

#### Gap 2: Rate Limiter Redis Schema ❌ → ✅ FIXED

**Issue:** Redis key schema for rate limiting not defined.

**Solution Added to Backend:**
```
Rate Limiter Redis Keys:
├─ Key format: rate_limit:{user_id}:{endpoint}
├─ TTL: Set to window duration (3600s)
├─ Value: request_count (integer)
├─ Sliding window: Epoch-based cleanup
└─ Example: rate_limit:user_123:GET/products → 45

Implementation:
├─ Location: apps/api/app/middleware/rate_limiter.py
├─ Redis operation: INCR + EXPIRE
├─ Fallback: In-memory counter if Redis unavailable
└─ Test: apps/api/tests/test_rate_limiter.py
```

---

#### Gap 3: Database Read Replicas Not in Sprint 0 ❌ → ✅ NOTED

**Issue:** Read replica strategy not applicable to Sprint 0.

**Solution:** Documented for Phase 7 (Performance).

```
Phase 7 (Week 33-38): Scalability
├─ AWS RDS Read Replicas (1 per region)
├─ Query routing: write → primary, read → replica
├─ Replication lag monitoring (< 1s SLA)
├─ Failover automation: Promote read replica
└─ Analytics queries: Route to replica
```

---

#### Gap 4: Background Task Queue Configuration ❌ → ✅ FIXED

**Issue:** Background task execution not detailed.

**Solution Added to Backend:**
```
Options for Sprint 0:

Option A: APScheduler (simpler, monolithic)
├─ Configuration in: apps/api/app/core/config.py
├─ Scheduler instance in: apps/api/app/main.py
├─ Jobs in: apps/api/app/tasks/
└─ Best for: < 10 concurrent tasks

Option B: Celery (scalable, distributed)
├─ Broker: Redis (CELERY_BROKER_URL)
├─ Backend: Redis (CELERY_RESULT_BACKEND)
├─ Config: apps/api/app/tasks/celery_config.py
├─ Worker: celery -A app.tasks worker
└─ Best for: > 100 concurrent tasks

Sprint 0 Recommendation: APScheduler (lower complexity)
Future (Phase 4+): Migrate to Celery if needed
```

---

#### Gap 5: Health Check Endpoints Not Specified ❌ → ✅ FIXED

**Issue:** No health check endpoint specification.

**Solution Added to Backend API:**
```
Health Check Endpoints:

1. GET /health (Readiness Probe)
   └─ Checks: API responsive
   └─ Response: {"status": "healthy", "timestamp": "..."}
   └─ Use: Kubernetes readiness probe

2. GET /healthz (Liveness Probe)
   └─ Checks: API alive (no detailed checks)
   └─ Response: 200 OK
   └─ Use: Kubernetes liveness probe

3. GET /health/detailed (Deep Health Check)
   └─ Checks: 
       ├─ Database connectivity
       ├─ Redis connectivity
       ├─ Qdrant connectivity
       ├─ External API availability
       └─ Memory/CPU usage
   └─ Response: Detailed status object

Implementation:
├─ File: apps/api/app/api/v1/health.py
├─ Dependencies: SQLAlchemy, Redis, Qdrant clients
└─ Caching: 30-second cache to avoid overload
```

---

#### Gap 6: Error Tracking & Monitoring ❌ → ✅ FIXED

**Issue:** Error tracking service (Sentry) not configured.

**Solution Added to Backend:**
```
Error Tracking Stack:

Sentry Configuration:
├─ DSN: SENTRY_DSN environment variable
├─ Environment: development/staging/production
├─ Release: Linked to git tag
├─ Traces sample rate: 20% (dev), 5% (prod)
└─ Attachment: Request/response data

Logging Aggregation Options:

Option A: CloudWatch (AWS native)
├─ Cost-effective for AWS infrastructure
├─ Log groups: /lipu/api/, /lipu/web/
├─ Retention: 7 days (configurable)
└─ Query: CloudWatch Insights

Option B: ELK Stack (Self-hosted)
├─ Elasticsearch: Data storage
├─ Logstash: Log ingestion & processing
├─ Kibana: Visualization & querying
└─ Cost: Higher, but full control

Sprint 0: CloudWatch (simpler setup)
Production: Add Sentry + CloudWatch
```

---

#### Gap 7: Logging Aggregation Strategy ❌ → ✅ FIXED

**Issue:** No centralized logging strategy.

**Solution Added:**
```
Logging Architecture:

Frontend (Next.js):
├─ Logger: winston (structured logging)
├─ Transport: Console (dev), HTTP (prod to CloudWatch)
├─ Format: JSON for parsing
└─ Levels: error, warn, info, debug

Backend (FastAPI):
├─ Logger: Python logging module
├─ Format: Structured JSON
├─ Handlers:
    ├─ Console (development)
    ├─ CloudWatch (production)
    └─ File (local backup)
└─ Levels: ERROR, WARNING, INFO, DEBUG

Docker Compose Logging:
├─ Driver: json-file (built-in)
├─ Options:
    ├─ max-size: 10m
    ├─ max-file: 3
    └─ labels: service name
└─ Access: docker-compose logs <service>

Log Retention Policy:
├─ Development: 7 days
├─ Staging: 30 days
├─ Production: 90 days + archive to S3
```

---

#### Gap 8: Development vs Production Environment Clarity ❌ → ✅ FIXED

**Issue:** No clear separation of environment-specific configuration.

**Solution Added:**
```
Environment Configuration Strategy:

.env Files (Different per environment):
├─ .env.local (local development) - NOT committed
├─ .env.staging (staging secrets) - GH Secrets only
├─ .env.production (production secrets) - AWS Secrets Manager

Configuration Files:
├─ apps/api/app/core/config.py
│  └─ Reads from environment, validates with Pydantic
├─ apps/web/next.config.js
│  └─ Reads from process.env, validates at build
└─ docker-compose.override.yml (local only)

Environment-Specific Settings:
├─ DEBUG: true (dev), false (prod)
├─ LOG_LEVEL: DEBUG (dev), INFO (prod)
├─ DATABASE_POOL_SIZE: 5 (dev), 20 (prod)
├─ REDIS_CACHE_TTL: 300s (dev), 3600s (prod)
├─ API_TIMEOUT: 30s (dev), 60s (prod)
├─ SENTRY_SAMPLE_RATE: 1.0 (dev), 0.1 (prod)
└─ CORS_ORIGINS: localhost:3000 (dev), lipu.com (prod)

CI/CD Environment Passing:
├─ GitHub Secrets for staging/prod
├─ AWS Secrets Manager for production
├─ Environment-specific deployment workflows
└─ Validation before deployment
```

---

#### Gap 9: Frontend State Management Trigger Patterns ❌ → ✅ FIXED

**Issue:** State management synchronization between API and store not documented.

**Solution Added to Frontend:**
```
State Management Architecture:

Zustand Stores:
├─ auth-store.ts
│  ├─ State: user, token, permissions, loading
│  ├─ Triggers: On login/logout (Clerk webhook)
│  └─ Persistence: LocalStorage + SessionStorage
│
├─ customer-store.ts
│  ├─ State: selectedProject, activeQuote, orders
│  ├─ Sync: Fetch on component mount, invalidate on mutations
│  └─ Invalidation: Manual invalidate() call after mutations
│
└─ ui-store.ts
   ├─ State: theme, sidebarOpen, notifications
   └─ Persistence: LocalStorage

Synchronization Patterns:

1. Query Pattern (Read):
   ├─ useEffect(() => {
   │   if (user && !data) {
   │     fetchProducts().then(store.setProducts)
   │   }
   }, [user])

2. Mutation Pattern (Write):
   ├─ const { mutate } = useMutation(createOrder)
   ├─ mutate(data, {
   │   onSuccess: (newOrder) => {
   │     store.addOrder(newOrder)  // Optimistic update
   │     invalidateQueries(['orders'])  // Sync with server
   │   }
   │ })

3. Real-time Pattern (WebSocket):
   ├─ useEffect(() => {
   │   ws.on('orderUpdated', (order) => {
   │     store.updateOrder(order)
   │   })
   }, [])

Implementation Files:
├─ apps/web/store/
├─ apps/web/lib/hooks/useApi.ts (Query handling)
├─ apps/web/lib/hooks/useForm.ts (Mutation handling)
└─ apps/web/lib/hooks/useWebSocket.ts (Real-time)
```

---

#### Gap 10: API Versioning & Migration Strategy ❌ → ✅ FIXED

**Issue:** Future API versioning path not defined.

**Solution Added:**
```
API Versioning Strategy:

Current State (Sprint 0):
├─ /api/v1/ endpoints
├─ v1 routes in: apps/api/app/api/v1/
└─ OpenAPI docs: /docs (v1)

Future Migration (Phase 4+):

Step 1: Create v2 Directory
└─ apps/api/app/api/v2/
   ├─ __init__.py
   ├─ products.py (NEW endpoints)
   ├─ orders.py (NEW endpoints)
   └─ ...

Step 2: Maintain v1
├─ Keep v1 routes active
├─ Add deprecation warnings
├─ Support for 6 months
└─ Document migration path

Step 3: Gradual Migration
├─ Announce: v2 available
├─ Documentation: Migration guide
├─ Support: Dedicated v2 docs
├─ Deprecate: v1 endpoints after 6 months
└─ Timeline: Send emails to API consumers

Step 4: Sunset v1
├─ Date: 6 months after v2 release
├─ Notification: 30-day warning
├─ Return: 410 Gone or redirect to v2
└─ Logs: Track migration completion

Client Library Versioning:
├─ npm package: @lipu/api-client-v1, v2
└─ Python package: lipu-api-client[v1], [v2]
```

---

### Additional Recommendations

#### Priority 1: Before Sprint 0 Starts

✅ **Already Addressed:** All critical gaps fixed above.

#### Priority 2: During Sprint 0

1. **DevOps Focus:**
   - Validate docker-compose startup time < 2 minutes
   - Test all health checks
   - Document troubleshooting guide

2. **Backend Focus:**
   - Implement rate limiter immediately (middleware)
   - Setup Sentry early (error visibility)
   - Create seed data script

3. **Frontend Focus:**
   - Create Zustand store examples
   - Document API integration patterns
   - Setup type-safe API client

#### Priority 3: Before MVP (Week 14)

1. **Performance:**
   - Load test: 100 concurrent users
   - Profile: API response times
   - Optimize: Slow queries, N+1 problems

2. **Security:**
   - OWASP scan: Dependency vulnerabilities
   - Penetration: API endpoints
   - Compliance: GDPR cookie consent

3. **Monitoring:**
   - Sentry: Error alerts configured
   - CloudWatch: Log aggregation active
   - Datadog: Infrastructure monitoring

---

### Validation Checklist for Sprint 0 Completion

```
✅ Infrastructure Setup
  ├─ [ ] Docker-compose running all services
  ├─ [ ] PostgreSQL database initialized
  ├─ [ ] Redis cache operational
  ├─ [ ] Qdrant vector DB running
  ├─ [ ] PgAdmin accessible
  └─ [ ] All health checks passing

✅ Backend Foundation
  ├─ [ ] FastAPI app starts without errors
  ├─ [ ] SQLAlchemy ORM models created
  ├─ [ ] Database migrations working
  ├─ [ ] API documentation generated (/docs)
  ├─ [ ] Authentication middleware active
  ├─ [ ] Rate limiter functional
  ├─ [ ] Error handling in place
  ├─ [ ] Logging configured
  ├─ [ ] Health endpoints responding
  └─ [ ] Tests running (coverage > 50%)

✅ Frontend Foundation
  ├─ [ ] Next.js app starts on localhost:3000
  ├─ [ ] Tailwind CSS working
  ├─ [ ] Shadcn/ui components loading
  ├─ [ ] TypeScript type checking passing
  ├─ [ ] API client configured
  ├─ [ ] Zustand stores working
  ├─ [ ] Auth middleware protecting routes
  ├─ [ ] Environment variables loaded
  ├─ [ ] ESLint passing
  └─ [ ] Tests running

✅ CI/CD Pipeline
  ├─ [ ] GitHub workflows created
  ├─ [ ] Lint workflow passing
  ├─ [ ] Build workflow creating images
  ├─ [ ] Test workflow executing
  ├─ [ ] Status checks on PR
  └─ [ ] Deployment to staging manual trigger

✅ Documentation
  ├─ [ ] README updated with setup steps
  ├─ [ ] Contributing guide created
  ├─ [ ] API documentation complete
  ├─ [ ] Database schema documented
  ├─ [ ] Troubleshooting guide written
  └─ [ ] Team onboarding completed

✅ Development Workflow
  ├─ [ ] All team members can start dev environment
  ├─ [ ] Branching strategy defined
  ├─ [ ] Code review process established
  ├─ [ ] Commit message guidelines documented
  ├─ [ ] PR template working
  └─ [ ] Issue tracking configured
```

---

## Conclusion

### Architecture Assessment: ✅ PRODUCTION READY

The LIPU Platform architecture review is **complete**. The system demonstrates:

**Strengths:**
- Comprehensive multi-layer architecture
- Production-grade technology choices
- Well-defined data structures
- Clear API contracts
- Detailed operational guidelines
- Scalability built-in

**Gaps Addressed:**
- All 10 identified gaps have been documented and solutions provided
- Environment configuration clarified
- Logging and monitoring strategy defined
- Error handling and health checks specified
- Deployment pipeline documented

**Ready for Sprint 0:**
✅ Monorepo structure finalized  
✅ Docker architecture specified  
✅ Environment variables defined  
✅ CI/CD workflows designed  
✅ Development setup documented  
✅ All team members can start development

---

**Document Status:** ✅ Complete - Ready for Implementation  
**Approval:** Recommended for team distribution  
**Next Phase:** Begin Sprint 0 infrastructure setup

---

**Prepared by:** Lead Architect + Senior Full Stack Engineer  
**Date:** June 24, 2026  
**Version:** 1.0
