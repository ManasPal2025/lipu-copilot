# LIPU UPVC Windows & Doors - System Architecture

**Document Version:** 1.0  
**Date:** 2026-06-24  
**Status:** Architecture Phase  
**Author:** Principal Software Architect

---

## Table of Contents

1. [Executive Overview](#executive-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack Justification](#technology-stack-justification)
4. [Architectural Patterns](#architectural-patterns)
5. [Security Architecture](#security-architecture)
6. [Scalability Strategy](#scalability-strategy)
7. [Data Architecture](#data-architecture)
8. [AI/ML Architecture](#aiml-architecture)
9. [Deployment Architecture](#deployment-architecture)
10. [Integration Points](#integration-points)

---

## Executive Overview

### Project Vision
Build a world-class, production-grade UPVC windows and doors e-commerce platform with AI-powered features that compete with international brands like VEKA, REHAU, and Andersen.

### Strategic Objectives
- **Market Presence**: Professional, modern, luxury design
- **Lead Generation**: Convert website visitors to qualified leads
- **AI Differentiation**: AI-powered sales agents, visualizations, and quote generation
- **Enterprise Scale**: Support multi-user scenarios with role-based access
- **Data Insights**: Comprehensive analytics for decision-making

### Core Success Metrics
- Page load time < 2.5s (Core Web Vitals)
- 99.9% uptime SLA
- Support 10,000+ concurrent users
- AI response latency < 3s
- Mobile conversion rate optimization

---

## System Architecture

### 3-Tier + Microservices Hybrid Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  Next.js 15 (SSG/ISR/SSR)                                   │
│  ├─ Public Website (Static + ISR)                           │
│  ├─ Customer Portal (SSR + Auth)                            │
│  └─ Admin Dashboard (CSR + Real-time)                       │
└─────────────────────────────────────────────────────────────┘
                          ↓ (API Gateway)
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  FastAPI (Python)                                           │
│  ├─ Core API Service                                        │
│  ├─ AI Service (LangGraph, LangChain)                       │
│  ├─ Image Processing Service (House Visualization)         │
│  ├─ Document Processing Service (RAG)                      │
│  ├─ Analytics Service                                       │
│  └─ Webhook Service                                         │
└─────────────────────────────────────────────────────────────┘
       ↓              ↓              ↓              ↓
┌──────────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐
│ PostgreSQL   │ │  Redis   │ │ Qdrant   │ │  AWS S3    │
│ (Primary DB) │ │ (Cache)  │ │ (Vector) │ │ (Storage)  │
└──────────────┘ └──────────┘ └──────────┘ └────────────┘
```

### Component Breakdown

#### Frontend (Next.js 15)
- **Public Website**: 
  - Landing page (SSG)
  - Product catalog (ISR)
  - Gallery & Projects (ISR)
  - Blog (ISR)
  - FAQ (ISR)
  - AI Chatbot (CSR)
  - Request Quote (SSR)

- **Customer Portal**:
  - Protected routes (SSR)
  - Real-time project updates
  - Saved designs (client-side state + server)
  - AI conversation history (SSR + streaming)

- **Admin Dashboard**:
  - Complex data tables (CSR)
  - Real-time analytics (WebSocket)
  - Inventory management (optimistic updates)
  - Drag-and-drop workflows

#### Backend (FastAPI)

**Core Services:**
1. **Product Service**: CRUD operations, catalog, variants
2. **Quote Service**: Quote generation, pricing logic
3. **Order Service**: Order management, fulfillment
4. **Customer Service**: CRM, profiles, history
5. **Inventory Service**: Stock tracking, alerts
6. **Project Service**: Site visits, timelines, documentation
7. **Analytics Service**: Dashboards, reporting
8. **File Service**: Upload, processing, delivery

**AI Services:**
1. **RAG Service**: Document ingestion, retrieval, Q&A
2. **Quote Generator**: AI-powered pricing
3. **Design Consultant**: Style recommendations
4. **House Visualizer**: Image detection & manipulation
5. **Sales Agent**: Conversational commerce

#### Data Layer
- **PostgreSQL**: OLTP (operational data)
- **Redis**: Session, cache, real-time data
- **Qdrant**: Vector embeddings (RAG, recommendations)
- **AWS S3**: Images, documents, brochures

---

## Technology Stack Justification

### Frontend: Next.js 15 + TypeScript

**Why Next.js 15?**
- **App Router**: Modern, nested layouts, easier state management
- **Server Components**: Reduced JS bundle, better SEO
- **ISR**: Static + dynamic content on same page
- **Image Optimization**: Automatic WebP, responsive images
- **Built-in Middleware**: Authentication, redirects
- **Streaming**: Faster TTFB, progressive rendering
- **Image Component**: Automatic optimization + lazy loading

**Why TypeScript?**
- Type safety across 1000s of components
- Better IDE support, fewer bugs at compile time
- Documentation through types
- Refactoring confidence

**Why Tailwind CSS?**
- Utility-first: Faster development
- No runtime CSS-in-JS (better performance)
- Purging unused styles automatically
- Dark mode support built-in
- Mobile-first responsive design

**Why Shadcn UI?**
- Unstyled, accessible components
- Copy-paste philosophy (not npm installed)
- Customizable for luxury brand design
- Built on Radix UI (accessible primitives)
- Headless component model

**Why Framer Motion?**
- Declarative animations (not imperative)
- GPU-accelerated
- Layout animations
- Gesture animations (mobile gestures)
- Performance-optimized

### Backend: FastAPI + Python

**Why FastAPI?**
- **Async-first**: High throughput, concurrent requests
- **Auto-generated docs**: Swagger UI out of box
- **Type hints**: FastAPI validates automatically
- **Fast performance**: Near parity with Node.js
- **AI ecosystem**: Best-in-class ML libraries
- **LangChain/LangGraph**: Native Python integration

**Why Python?**
- LangChain, LangGraph, OpenAI libraries
- Image processing (PIL, OpenCV, etc.)
- Document processing (PyPDF, python-docx)
- Data science libraries (NumPy, Pandas)
- Scikit-learn for ML
- SQLAlchemy ORM

### Database: PostgreSQL

**Why PostgreSQL?**
- **Full-Text Search**: Built-in FTS without Elasticsearch
- **JSONB**: Flexible schema where needed
- **Vector Extension (pgvector)**: Native vector storage for RAG
- **ACID Compliance**: Data integrity
- **Replication**: High availability
- **Window Functions**: Complex analytics queries
- **Mature**: 20+ years, enterprise-proven

### Authentication: Clerk

**Why Clerk?**
- **No infrastructure**: Zero-knowledge architecture
- **Multi-social login**: Google, GitHub, Microsoft, etc.
- **Enterprise SSO**: Okta, Azure AD integration
- **Admin controls**: Role-based access built-in
- **Security**: OWASP Top 10 covered, compliance-ready
- **Developer experience**: Excellent SDK, quick integration

### Caching: Redis

**Why Redis?**
- **Fast**: In-memory access
- **Session store**: Distributed session management
- **Cache**: Reduce DB load
- **Real-time**: Pub/Sub for notifications
- **Rate limiting**: Built-in patterns
- **Atomic operations**: Transaction-like operations

### Vector Storage: Qdrant

**Why Qdrant?**
- **Filtering**: Filter by metadata + vector similarity
- **Scalability**: Sharding support
- **Performance**: Sub-millisecond search
- **Python SDK**: Excellent integration
- **REST API**: Language agnostic
- **Self-hosted**: Data privacy

### Storage: AWS S3

**Why AWS S3?**
- **Scalable**: Unlimited storage
- **CDN**: CloudFront integration
- **Lifecycle policies**: Auto-archive old files
- **Versioning**: History & recovery
- **Signed URLs**: Temporary access
- **Multipart upload**: Large file support

---

## Architectural Patterns

### 1. Domain-Driven Design (DDD)
```
bounded_contexts/
├── Products/
│   ├── Domain/
│   ├── Application/
│   ├── Infrastructure/
│   └── Presentation/
├── Orders/
├── Customers/
├── AI/
└── Analytics/
```

### 2. Event-Driven Architecture

**Events:**
```
OrderCreated
OrderApproved
OrderShipped
OrderDelivered
QuoteGenerated
ProjectCreated
ProjectCompleted
InventoryLow
CustomerEngaged
AIConversationStarted
```

**Benefits:**
- Loose coupling
- Audit trail
- Real-time notifications
- Analytics pipeline
- Workflow automation

### 3. CQRS (Command Query Responsibility Segregation)

**Commands (Write):**
- CreateOrder
- UpdateInventory
- GenerateQuote

**Queries (Read):**
- GetProductCatalog
- GetCustomerHistory
- GetAnalyticsReport

**Benefits:**
- Optimized read path
- Separate scaling concerns
- Event sourcing ready
- Complex queries simplified

### 4. API Gateway Pattern

```
Client → API Gateway (Authentication, Rate Limiting, Logging) → Services
```

### 5. Circuit Breaker Pattern

For external AI services (OpenAI, Gemini):
- Failure detection
- Graceful degradation
- Fallback responses

### 6. Cache-Aside Pattern

```
1. Check cache
2. If miss, fetch from DB
3. Populate cache
4. Return data
```

---

## Security Architecture

### Authentication & Authorization

```
┌─────────────────────────────────────────┐
│  Clerk Authentication                   │
├─────────────────────────────────────────┤
│  ├─ JWT Tokens (Session)                │
│  ├─ Role-Based Access Control           │
│  ├─ Multi-factor Authentication         │
│  └─ Enterprise SSO                      │
└─────────────────────────────────────────┘
           ↓ (Enforced in middleware)
┌─────────────────────────────────────────┐
│  Next.js Middleware                     │
├─────────────────────────────────────────┤
│  ├─ Protected routes                    │
│  ├─ Role validation                     │
│  ├─ Audit logging                       │
│  └─ Rate limiting                       │
└─────────────────────────────────────────┘
```

### Data Protection

**In Transit:**
- TLS 1.3 for all connections
- HSTS headers
- Certificate pinning (mobile apps future)

**At Rest:**
- PostgreSQL encryption (pgcrypto)
- S3 encryption (KMS keys)
- Sensitive fields hashed (passwords, PII)
- Backup encryption

**Application Level:**
- Input validation (Pydantic, Zod)
- Output encoding (XSS prevention)
- CSRF tokens (Form submissions)
- SQL injection prevention (SQLAlchemy ORM)

### Compliance

- GDPR: Data deletion, consent tracking
- PCI-DSS: Payment processing (Stripe integration)
- ISO 27001: Security standards
- SOC 2 Type II: Third-party compliance

### Audit & Logging

```
Event Log:
├─ User login/logout
├─ Data modifications (what, who, when)
├─ Failed auth attempts
├─ API errors
├─ AI model usage
└─ Admin actions
```

---

## Scalability Strategy

### Horizontal Scaling

**Frontend (Vercel):**
- Auto-scaling CDN
- Serverless functions
- Edge middleware

**Backend (Docker + Kubernetes):**
```
API Service: ┌──────┐  ┌──────┐  ┌──────┐
             │Pod 1 │  │Pod 2 │  │Pod 3 │
             └──────┘  └──────┘  └──────┘
              ↓          ↓          ↓
            (Load Balancer)
```

**Database:**
- Read replicas for analytics
- Sharding strategy (by customer_id or region)
- Connection pooling

**Redis:**
- Cluster mode
- Sentinel for failover

### Caching Strategy

**Layers:**
1. **Browser cache**: Static assets (1 year)
2. **CDN cache**: Images, media (7 days)
3. **API response cache**: Popular queries (1 hour)
4. **Database query cache**: Product catalog (24 hours)
5. **Full-page cache**: Public pages (ISR)

### Database Query Optimization

- Indexing strategy (on foreign keys, frequent filters)
- Query analysis (EXPLAIN ANALYZE)
- Materialized views for complex reports
- Read replicas for analytics

### Monitoring & Observability

```
Application Metrics:
├─ Response time (p50, p95, p99)
├─ Error rate
├─ Throughput (requests/sec)
├─ Resource usage (CPU, memory, disk)
├─ Database connections
└─ Cache hit ratio

Business Metrics:
├─ Lead conversion rate
├─ Quote acceptance rate
├─ Order fulfillment time
├─ Customer satisfaction
└─ AI model accuracy
```

---

## Data Architecture

### Entity Relationships (Conceptual)

```
Company
├── Products
│   ├── Variants (Color, Glass, Hardware)
│   ├── Pricing
│   ├── Inventory
│   └── Documentation
├── Customers
│   ├── Contact Info
│   ├── Projects
│   ├── Orders
│   ├── Quotes
│   └── Designs
├── Employees
│   ├── Roles
│   ├── Permissions
│   └── Activities
└── Analytics
    ├── Leads
    ├── Sales
    ├── Inventory
    └── AI Usage
```

### Data Classification

**Public:**
- Product information
- Blog posts
- Gallery images
- Testimonials

**Customer Private:**
- Profile information
- Projects
- Designs
- Quotes & Orders

**Admin Only:**
- Inventory levels
- Pricing details
- Employee data
- Analytics reports

**Audit/Compliance:**
- All user actions
- Data access logs
- Changes history

---

## AI/ML Architecture

### RAG System (Retrieval-Augmented Generation)

```
Document Ingestion Pipeline:
┌──────────────┐  ┌──────────┐  ┌────────┐  ┌────────────┐
│Documents     │→ │Parse     │→ │Chunk   │→ │Embed       │
│(PDF, DOCX)   │  │(PyPDF)   │  │(500    │  │(OpenAI API)│
│              │  │          │  │tokens) │  │            │
└──────────────┘  └──────────┘  └────────┘  └────────────┘
                                                    ↓
                                            ┌────────────────┐
                                            │Qdrant Vector DB│
                                            └────────────────┘

Query Pipeline:
┌──────────┐  ┌───────────┐  ┌────────┐  ┌──────────┐  ┌──────┐
│User Query│→ │Embed Query│→ │Search  │→ │Retrieve  │→ │LLM   │
│          │  │(OpenAI)   │  │Similar │  │Top K     │  │Call  │
└──────────┘  └───────────┘  └────────┘  └──────────┘  └──────┘
```

### AI Services Integration

**LangGraph for Agentic Workflows:**

```
State Machine:
START → Analysis → Decision → Action → Response → END

Example - Sales Agent:
START
  ↓
(User asks: "Which window for coastal weather?")
  ↓
Analysis: Classify question intent
  ↓
Decision: Query RAG system
  ↓
Action: Retrieve relevant documents
  ↓
Response: Generate answer using LLM
  ↓
END
```

**LangChain for Prompt Management:**
- Prompt templates
- Chain orchestration
- Memory management
- Tool integration

### AI Models Strategy

**Current:**
- OpenAI GPT-4: Primary LLM
- OpenAI DALL-E: Image generation
- OpenAI Embeddings: Vector representation

**Future Expansion:**
- Gemini: Fallback, multimodal
- Claude: Complex reasoning
- Flux/Stable Diffusion: Self-hosted image generation
- ControlNet: Precise image manipulation

### House Visualization Pipeline

```
1. Image Upload
   ↓
2. Detect Windows/Doors (YOLO or Vision API)
   ↓
3. Segment Areas
   ↓
4. AI Image Manipulation (Flux/ControlNet)
   ↓
5. Replace with UPVC Design
   ↓
6. Generate Preview Images
   ↓
7. Store & Return to User
```

---

## Deployment Architecture

### Multi-Environment Strategy

```
Development:
├── Localhost
├── Docker compose (DB, Redis, Qdrant)
└── Mock AI services

Staging:
├── AWS EC2 instances
├── AWS RDS PostgreSQL
├── AWS ElastiCache (Redis)
├── AWS Qdrant managed
└── Real AI service calls (test keys)

Production:
├── Vercel (Frontend)
├── AWS ECS (Backend)
├── AWS RDS (Multi-AZ)
├── AWS ElastiCache (Cluster mode)
├── AWS Qdrant (Managed)
├── AWS CloudFront (CDN)
└── Real AI service calls (prod keys)
```

### CI/CD Pipeline

```
GitHub Push
  ↓
GitHub Actions
  ├─ Linting (ESLint, Black)
  ├─ Type checking (TypeScript, mypy)
  ├─ Unit tests
  ├─ Integration tests
  └─ E2E tests
    ↓
  [If tests pass]
    ↓
  ├─ Build Docker image
  ├─ Push to ECR
  └─ Deploy to staging
    ↓
  [Manual approval for production]
    ↓
  ├─ Deploy frontend to Vercel
  ├─ Deploy backend to ECS
  ├─ Run migrations
  └─ Smoke tests
    ↓
  Rollback on failure
```

### Disaster Recovery

**Backup Strategy:**
- Database: Automated daily snapshots (30-day retention)
- Files: S3 versioning + cross-region replication
- Configuration: Infrastructure as Code (Terraform)

**Recovery Time Objectives (RTO):**
- Frontend: < 5 minutes (DNS + Vercel failover)
- Backend: < 15 minutes (RDS failover + ECS rollback)
- Database: < 1 hour (from snapshot)

**Recovery Point Objectives (RPO):**
- Database: 1 hour
- Files: Point-in-time (S3 versioning)
- Logs: 7 days

---

## Integration Points

### External Services

**Payment Processing:**
- Stripe/Razorpay for payments
- Webhook handling for updates
- PCI-DSS compliance

**Email Service:**
- SendGrid for transactional emails
- Subscription management
- Deliverability tracking

**SMS Service:**
- Twilio for order notifications
- OTP for 2FA

**Video Hosting:**
- Vimeo or YouTube for product videos
- Embed in product pages

**CRM Integration:**
- Salesforce/Pipedrive for leads
- Webhook events: OrderCreated, QuoteGenerated
- Automated lead scoring

**Analytics:**
- Mixpanel/Amplitude for user behavior
- PostHog for product analytics
- Sentry for error tracking

### Internal Service Mesh

```
Frontend ← → API Gateway ← → Service 1
           ← → Service 2
           ← → Service 3
           ← → Message Queue (Redis Pub/Sub)
```

---

## Next Steps

1. ✅ **System Architecture** (THIS DOCUMENT)
2. 📋 **Database Schema** (with relationships, constraints)
3. 📋 **API Contracts** (OpenAPI/Swagger specifications)
4. 📋 **Folder Structure** (monorepo vs. separate repos)
5. 📋 **User Journeys** (wireflows for each module)
6. 📋 **Wireframes** (UI layouts)
7. 📋 **Implementation Roadmap** (phase-by-phase)
8. 📋 **Sprint Plan** (2-week sprints, team allocation)

---

**Document Status:** Ready for review by stakeholders  
**Next Review:** After database schema design
