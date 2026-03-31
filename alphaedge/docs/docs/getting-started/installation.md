# Installation

## Prerequisites

- Docker & Docker Compose v2
- Git

## Quick Start

```bash
git clone https://github.com/your-org/alphaedge.git
cd alphaedge

# Copy and edit environment config
cp .env.example .env

# Start all services
docker compose up -d

# Run database migrations
docker compose exec backend alembic upgrade head

# Seed demo data (optional)
docker compose exec backend python scripts/seed.py
```

## Services

| Service | URL |
|---------|-----|
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |
| Frontend | http://localhost:3000 |
| PostgreSQL | localhost:5432 |
| Redis | localhost:6379 |

## Demo Credentials

After running the seed script:

- **Email**: `demo@alphaedge.local`
- **Password**: `demo1234`
