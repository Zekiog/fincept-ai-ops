import os
from typing import Any, Dict

from apps.fincept_aiops.connectors.base import BaseConnector
from apps.fincept_aiops.connectors.retry import with_retry


class NewsConnector(BaseConnector):
    name = "news"

    def fetch(self, params: Dict[str, Any]) -> Dict[str, Any]:
        symbol = str(params.get("symbol", "")).upper()
        limit = int(params.get("limit", 5))
        if os.getenv("MARKET_DATA_PROVIDER", "stub") == "stub" or not symbol:
            return self._stub(symbol, limit)
        try:
            return self._fetch_live(symbol, limit)
        except Exception as e:
            return {"ok": False, "error": str(e), "symbol": symbol}

    @with_retry()
    def _fetch_live(self, symbol: str, limit: int) -> Dict[str, Any]:
        import yfinance as yf

        news = yf.Ticker(symbol).news or []
        items = [
            {
                "title": n.get("title", ""),
                "publisher": n.get("publisher", ""),
                "link": n.get("link", ""),
                "published_at": n.get("providerPublishTime", ""),
            }
            for n in news[:limit]
        ]
        return {"ok": True, "symbol": symbol, "count": len(items), "items": items}

    def _stub(self, symbol: str, limit: int) -> Dict[str, Any]:
        """Returns stub data for testing. URLs are null — do not follow."""
        stub_symbol = symbol or "STUB"
        return {
            "ok": True,
            "symbol": stub_symbol,
            "stub": True,
            "count": 2,
            "items": [
                {
                    "title": f"{stub_symbol} beats earnings estimates",
                    "publisher": "Reuters [stub]",
                    "link": None,
                    "published_at": "2026-05-22"
                },
                {
                    "title": f"{stub_symbol} expands into new markets",
                    "publisher": "Bloomberg [stub]",
                    "link": None,
                    "published_at": "2026-05-21"
                },
            ]
        }
