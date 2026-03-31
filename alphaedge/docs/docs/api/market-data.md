# Market Data API

Market data endpoints do not require authentication.

## Get Quote

```http
GET /api/v1/market/quote/AAPL
```

**Response (200):**

```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "price": 175.50,
    "previous_close": 174.20,
    "open": 174.80,
    "day_high": 176.00,
    "day_low": 174.00,
    "volume": 52000000,
    "market_cap": 2700000000000,
    "name": "Apple Inc.",
    "currency": "USD"
  }
}
```

## Get Historical Data

```http
GET /api/v1/market/history/AAPL?period=1mo&interval=1d
```

**Valid periods:** `1d`, `5d`, `1mo`, `3mo`, `6mo`, `1y`, `2y`, `5y`, `10y`, `ytd`, `max`

**Valid intervals:** `1m`, `2m`, `5m`, `15m`, `30m`, `60m`, `90m`, `1h`, `1d`, `5d`, `1wk`, `1mo`, `3mo`

## Search Symbols

```http
GET /api/v1/market/search?q=apple
```
