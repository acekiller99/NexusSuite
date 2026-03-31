# Orders API

All order endpoints require authentication.

## List Orders

```http
GET /api/v1/orders
GET /api/v1/orders?portfolio_id=uuid
```

## Create Order

```http
POST /api/v1/orders
```

```json
{
  "portfolio_id": "uuid",
  "symbol": "AAPL",
  "side": "buy",
  "order_type": "market",
  "quantity": 10
}
```

**Side:** `buy`, `sell`

**Order Types:** `market`, `limit`, `stop`, `stop_limit`

**Statuses:** `pending`, `submitted`, `filled`, `partially_filled`, `cancelled`, `rejected`

For `limit` orders, include `limit_price`. For `stop` orders, include `stop_price`.

## Get Order

```http
GET /api/v1/orders/{order_id}
```
