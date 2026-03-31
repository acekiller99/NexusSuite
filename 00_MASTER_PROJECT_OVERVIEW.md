# NexusSuite — Master Project Overview

## Ecosystem Name: **NexusSuite**

A collection of independent, open-source microservice-based business applications designed to be self-hosted with zero licensing costs. Each project is standalone but follows shared conventions for easy integration.

---

## Project Registry

| # | Project Code | Project Name | Domain | Status |
|---|-------------|-------------|--------|--------|
| 1 | `alphaedge` | **AlphaEdge** | Automated Stock Trading Bot | Planned |
| 2 | `servepos` | **ServePOS** | Restaurant POS System | Planned |
| 3 | `wareflow` | **WareFlow** | Warehouse Management System (WMS) | Planned |
| 4 | `medicore` | **MediCore** | Hospital Management Information System | Planned |
| 5 | `finledger` | **FinLedger** | Finance & Accounting Management System | Planned |
| 6 | `visionguard` | **VisionGuard** | Visual Analysis Platform (CCTV/Webcam AI) | Planned |
| 7 | `codepathway` | **CodePathway** | Interactive IT Learning & Tutorial Platform | Planned |

---

## Shared Technology Principles

### Cost Policy
- **ALL libraries must be free and open-source** (MIT, Apache 2.0, BSD, GPL-compatible)
- No SaaS dependencies required for core functionality
- Self-hostable on any Linux/Windows server
- Domain and server rental costs are acceptable; software licensing costs are NOT

### Shared Tech Stack

| Layer | Technology | License | Why |
|-------|-----------|---------|-----|
| **Backend Framework** | Python FastAPI | MIT | Async, fast, auto-docs, huge ecosystem |
| **Frontend Framework** | Next.js 14+ (React) | MIT | SSR, API routes, great DX |
| **Database** | PostgreSQL 16+ | PostgreSQL License (free) | Robust, full-featured RDBMS |
| **Cache/Queue** | Redis 7+ (via Valkey or KeyDB) | BSD/Apache | In-memory store, pub/sub, task queue |
| **Task Queue** | Celery (Python) | BSD | Distributed task processing |
| **API Protocol** | REST + WebSocket | — | Universal compatibility |
| **Auth** | JWT + OAuth2 (via FastAPI) | — | Stateless, scalable auth |
| **ORM** | SQLAlchemy 2.0 + Alembic | MIT | Async support, migrations |
| **Containerization** | Docker + Docker Compose | Apache 2.0 | Consistent deployment |
| **Reverse Proxy** | Nginx / Caddy | BSD/Apache | TLS termination, load balancing |
| **Monitoring** | Prometheus + Grafana | Apache 2.0 | Metrics and dashboards |
| **Logging** | Loki + Promtail | AGPL (self-host OK) | Centralized logging |
| **CI/CD** | GitHub Actions (free for public repos) | — | Automated testing and deployment |
| **Documentation** | MkDocs Material | MIT | Beautiful project docs |

### Shared Architecture Pattern

All projects follow this microservice pattern:

```
┌──────────────────────────────────────────────────────────┐
│                    Nginx / Caddy (Reverse Proxy)          │
├───────────────┬──────────────────┬───────────────────────┤
│  Next.js App  │  FastAPI Backend  │  WebSocket Server     │
│  (Frontend)   │  (REST API)       │  (Real-time events)   │
├───────────────┴──────────────────┴───────────────────────┤
│                 Redis (Cache + Pub/Sub + Queue)           │
├──────────────────────────────────────────────────────────┤
│                 PostgreSQL (Primary Database)             │
├──────────────────────────────────────────────────────────┤
│            Celery Workers (Background Tasks)              │
├──────────────────────────────────────────────────────────┤
│       Prometheus + Grafana + Loki (Observability)         │
└──────────────────────────────────────────────────────────┘
```

### Shared Conventions

1. **API Versioning**: All APIs use `/api/v1/` prefix
2. **Authentication**: JWT Bearer tokens, refresh token rotation
3. **Response Format**: Standardized JSON envelope
   ```json
   {
     "success": true,
     "data": {},
     "message": "Operation completed",
     "errors": [],
     "meta": { "page": 1, "total": 100 }
   }
   ```
4. **Error Codes**: HTTP standard + custom business error codes
5. **Database**: UUID primary keys, soft deletes, audit columns (`created_at`, `updated_at`, `created_by`)
6. **Multi-tenancy**: Schema-based or row-based tenant isolation
7. **Webhooks**: Outbound webhook system for 3rd-party integration
8. **Rate Limiting**: Per-tenant, per-endpoint rate limits
9. **CORS**: Configurable allowed origins per environment
10. **Health Checks**: `/api/v1/health` endpoint on every service

### Shared Folder Structure (per project)

```
project-name/
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic.ini
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app entry
│   │   ├── config.py            # Settings via pydantic-settings
│   │   ├── database.py          # DB engine, session
│   │   ├── dependencies.py      # Shared dependencies
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic request/response schemas
│   │   ├── api/
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── router.py    # Main v1 router
│   │   │   │   └── endpoints/   # Endpoint modules
│   │   │   └── deps.py          # API dependencies (auth, etc.)
│   │   ├── services/            # Business logic
│   │   ├── repositories/        # Data access layer
│   │   ├── tasks/               # Celery tasks
│   │   ├── utils/               # Helpers
│   │   └── websockets/          # WS handlers
│   └── tests/
│       ├── conftest.py
│       ├── unit/
│       └── integration/
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── src/
│   │   ├── app/                 # Next.js App Router
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── services/            # API client
│   │   ├── stores/              # Zustand stores
│   │   └── types/
│   └── public/
├── docs/
│   └── mkdocs.yml
└── scripts/
    ├── seed.py
    └── setup.sh
```

---

## Implementation Order (Recommended)

1. **AlphaEdge** (Stock Bot) — Immediate priority per user request
2. **ServePOS** (Restaurant POS) — High business value, well-defined domain
3. **WareFlow** (Warehouse) — Complements POS for supply chain
4. **FinLedger** (Finance) — Cross-cuts all business projects
5. **MediCore** (Hospital) — Complex domain, benefits from patterns established
6. **VisionGuard** (Visual AI) — Standalone, can be developed in parallel
7. **CodePathway** (IT Tutorial) — Standalone educational platform, can be developed anytime

---

## Cross-Project Integration Points

```
AlphaEdge ──── Webhook alerts ───► Any notification system
ServePOS  ──── Inventory sync ───► WareFlow
ServePOS  ──── Sales data ───────► FinLedger
WareFlow  ──── Stock levels ─────► ServePOS
WareFlow  ──── Purchase orders ──► FinLedger
MediCore  ──── Billing data ─────► FinLedger
VisionGuard ── People counting ──► ServePOS (queue analytics)
VisionGuard ── Security alerts ──► Any project via webhook
```

---

## Detailed Plans

Each project has its own detailed plan file:

- `01_ALPHAEDGE_STOCK_BOT.md` — Full trading bot specification
- `02_SERVEPOS_RESTAURANT_POS.md` — Restaurant POS system
- `03_WAREFLOW_WAREHOUSE_MIS.md` — Warehouse management system
- `04_MEDICORE_HOSPITAL_MIS.md` — Hospital information system
- `05_FINLEDGER_FINANCE_MIS.md` — Finance management system
- `06_VISIONGUARD_VISUAL_ANALYSIS.md` — CCTV/Webcam AI platform
- `07_CODEPATHWAY_IT_TUTORIAL.md` — Interactive IT learning platform
