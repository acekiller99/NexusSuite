# Configuration

All configuration is managed via environment variables. Copy `.env.example` to `.env` and adjust as needed.

## Environment Variables

### General

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_NAME` | AlphaEdge | Application name |
| `APP_ENV` | development | Environment: development, staging, production |
| `DEBUG` | true | Enable debug mode |
| `SECRET_KEY` | — | Application secret key (change in production!) |

### Database (PostgreSQL)

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_HOST` | db | PostgreSQL hostname |
| `POSTGRES_PORT` | 5432 | PostgreSQL port |
| `POSTGRES_USER` | alphaedge | Database user |
| `POSTGRES_PASSWORD` | changeme | Database password |
| `POSTGRES_DB` | alphaedge | Database name |

### Redis

| Variable | Default | Description |
|----------|---------|-------------|
| `REDIS_HOST` | redis | Redis hostname |
| `REDIS_PORT` | 6379 | Redis port |

### JWT Authentication

| Variable | Default | Description |
|----------|---------|-------------|
| `JWT_SECRET_KEY` | — | JWT signing key (change in production!) |
| `JWT_ALGORITHM` | HS256 | JWT algorithm |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Access token lifetime |
| `JWT_REFRESH_TOKEN_EXPIRE_DAYS` | 7 | Refresh token lifetime |

### Trading

| Variable | Default | Description |
|----------|---------|-------------|
| `TRADING_MODE` | paper | `paper` or `live` |
| `ALPACA_API_KEY` | — | Alpaca API key (for live/paper trading) |
| `ALPACA_SECRET_KEY` | — | Alpaca secret key |
| `ALPACA_BASE_URL` | https://paper-api.alpaca.markets | Alpaca API base URL |

### CORS

| Variable | Default | Description |
|----------|---------|-------------|
| `CORS_ORIGINS` | http://localhost:3000 | Comma-separated list of allowed origins |
