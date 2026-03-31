# Strategies API

All strategy endpoints require authentication.

## List Strategies

```http
GET /api/v1/strategies
```

## Create Strategy

```http
POST /api/v1/strategies
```

```json
{
  "name": "SMA Crossover",
  "description": "Simple moving average crossover strategy",
  "strategy_type": "sma_crossover",
  "symbols": ["AAPL", "MSFT", "GOOGL"],
  "parameters": {
    "short_window": 20,
    "long_window": 50
  },
  "is_paper": true
}
```

**Strategy Types:** `sma_crossover`, `rsi`, `macd`, `bollinger_bands`

**Statuses:** `draft`, `active`, `paused`, `stopped`

## Get Strategy

```http
GET /api/v1/strategies/{strategy_id}
```

## Update Strategy

```http
PATCH /api/v1/strategies/{strategy_id}
```

```json
{
  "status": "active",
  "parameters": { "short_window": 10, "long_window": 30 }
}
```
