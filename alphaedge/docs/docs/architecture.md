# Architecture

## System Overview

```
┌──────────────────────────────────────────────────────────┐
│                    Nginx (Reverse Proxy)                  │
├───────────────┬──────────────────┬───────────────────────┤
│  Next.js App  │  FastAPI Backend  │  WebSocket Server     │
│  (Frontend)   │  (REST API)       │  (Real-time feeds)    │
├───────────────┴──────────────────┴───────────────────────┤
│                 Redis (Cache + Pub/Sub + Queue)           │
├──────────────────────────────────────────────────────────┤
│                 PostgreSQL (Primary Database)             │
├──────────────────────────────────────────────────────────┤
│            Celery Workers (Background Tasks)              │
└──────────────────────────────────────────────────────────┘
```

## Backend Structure

| Layer | Purpose |
|-------|---------|
| **API Endpoints** | HTTP handlers, request validation, response formatting |
| **Services** | Business logic (market data, trading engine) |
| **Repositories** | Data access layer, database queries |
| **Models** | SQLAlchemy ORM models |
| **Schemas** | Pydantic request/response validation |
| **Tasks** | Celery background tasks (strategy execution, alerts) |
| **WebSockets** | Real-time market feeds and notifications |

## Key Design Decisions

- **Async-first**: FastAPI + SQLAlchemy 2.0 async for high throughput
- **JWT Auth**: Stateless authentication with access + refresh tokens
- **Soft deletes**: `is_deleted` flag on all models for data safety
- **UUID primary keys**: Globally unique, safe for distributed systems
- **Paper/Live mode**: All trading features support both modes
- **yfinance for data**: Free market data with no API key requirement
