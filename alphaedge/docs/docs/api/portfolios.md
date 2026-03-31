# Portfolios API

All portfolio endpoints require authentication via `Authorization: Bearer <token>`.

## List Portfolios

```http
GET /api/v1/portfolios
```

**Response (200):**

```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "name": "My Portfolio",
      "description": "",
      "initial_capital": "10000.00",
      "cash_balance": "10000.00",
      "is_paper": true,
      "created_at": "2026-01-01T00:00:00Z"
    }
  ]
}
```

## Create Portfolio

```http
POST /api/v1/portfolios
```

```json
{
  "name": "Growth Portfolio",
  "description": "Long-term growth stocks",
  "initial_capital": "50000.00",
  "is_paper": true
}
```

## Get Portfolio

```http
GET /api/v1/portfolios/{portfolio_id}
```

## List Positions

```http
GET /api/v1/portfolios/{portfolio_id}/positions
```
