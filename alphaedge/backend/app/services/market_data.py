import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import yfinance as yf

_executor = ThreadPoolExecutor(max_workers=4)


class MarketDataService:
    """Service for fetching market data via yfinance (free, no API key needed)."""

    async def get_quote(self, symbol: str) -> dict[str, Any] | None:
        """Get current quote for a symbol."""
        def _fetch() -> dict[str, Any] | None:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            if not info or "regularMarketPrice" not in info:
                return None
            return {
                "symbol": symbol,
                "price": info.get("regularMarketPrice"),
                "previous_close": info.get("previousClose"),
                "open": info.get("regularMarketOpen"),
                "day_high": info.get("dayHigh"),
                "day_low": info.get("dayLow"),
                "volume": info.get("regularMarketVolume"),
                "market_cap": info.get("marketCap"),
                "name": info.get("shortName"),
                "currency": info.get("currency"),
            }

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(_executor, _fetch)

    async def get_history(
        self, symbol: str, period: str = "1mo", interval: str = "1d"
    ) -> list[dict[str, Any]]:
        """Get historical price data."""
        def _fetch() -> list[dict[str, Any]]:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            if df.empty:
                return []
            df = df.reset_index()
            records = []
            for _, row in df.iterrows():
                records.append({
                    "date": str(row.get("Date", row.get("Datetime", ""))),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]),
                })
            return records

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(_executor, _fetch)

    async def search_symbols(self, query: str) -> list[dict[str, Any]]:
        """Search for symbols by name or ticker."""
        def _fetch() -> list[dict[str, Any]]:
            # yfinance doesn't have a direct search; use a basic approach
            ticker = yf.Ticker(query)
            info = ticker.info
            if info and info.get("shortName"):
                return [{
                    "symbol": query.upper(),
                    "name": info.get("shortName", ""),
                    "exchange": info.get("exchange", ""),
                    "type": info.get("quoteType", ""),
                }]
            return []

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(_executor, _fetch)
