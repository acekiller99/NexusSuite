# AlphaEdge — Automated Stock Trading Bot

Part of the **NexusSuite** ecosystem.

AlphaEdge is a self-hosted, open-source automated stock trading platform. It supports paper trading and live trading via broker APIs, with configurable strategies, backtesting, and real-time market data.

## Quick Start

```bash
# 1. Copy environment config
cp .env.example .env
# Edit .env with your settings

# 2. Start all services
docker compose up -d

# 3. Run database migrations
docker compose exec backend alembic upgrade head

# 4. Seed initial data (optional)
docker compose exec backend python scripts/seed.py
```

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000

## Architecture

```
Next.js (Dashboard) → FastAPI (REST + WS) → PostgreSQL
                                           → Redis (cache/queue)
                                           → Celery (strategies/orders)
```

## Key Features

- **Strategy Engine** — Define and run custom trading strategies
- **Backtesting** — Test strategies against historical data
- **Paper Trading** — Risk-free practice trading
- **Live Trading** — Connect to brokers (Alpaca, etc.)
- **Real-time Data** — WebSocket-powered market feeds
- **Portfolio Tracking** — Positions, P&L, trade history
- **Alerts** — Price alerts and strategy notifications

## Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python FastAPI, SQLAlchemy 2.0, Celery |
| Frontend | Next.js 14+, React, Zustand |
| Database | PostgreSQL 16+ |
| Cache/Queue | Redis 7+ |
| Deploy | Docker Compose |

## License

MIT
