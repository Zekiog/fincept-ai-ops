import re
from typing import Any, Dict

from apps.fincept_aiops.agents.base_agent import AgentStatus, BaseAgent
from apps.fincept_aiops.audit_logger import AuditLogger
from apps.fincept_aiops.connectors.registry import get_connector

audit = AuditLogger()

# Allowlist: only alphanumeric ticker symbols (1-6 chars)
_SYMBOL_RE = re.compile(r'^[A-Z0-9]{1,6}$')

# Safe keyword sets — lowercase, no user-controlled input
_BULL_KEYWORDS = frozenset(["beat", "growth", "expand", "record", "profit", "upgrade", "raise"])
_BEAR_KEYWORDS = frozenset(["miss", "decline", "loss", "recall", "risk", "downgrade", "cut"])


class ResearchAgent(BaseAgent):
    """Agent 1 — pulls market + news + fundamentals, builds a research note.

    Security:
    - Symbol input validated against strict alphanumeric allowlist
    - News titles sanitized before keyword matching (strip, lowercase, max 200 chars)
    - Confidence score capped at 0.90, minimum floor 0.40
    - No user input is interpolated into executed code paths
    """

    def run(self, symbol: str, timeframe: str = "1d") -> Dict[str, Any]:
        self._set_status(AgentStatus.RUNNING)
        try:
            result = self._build_note(symbol, timeframe)
            self._set_status(AgentStatus.IDLE)
            return result
        except Exception:
            self._set_status(AgentStatus.ERROR)
            raise

    def _build_note(self, symbol: str, timeframe: str = "1d") -> Dict[str, Any]:
        # --- Input validation ---
        symbol = symbol.strip().upper()
        if not _SYMBOL_RE.match(symbol):
            return {"ok": False, "error": "invalid_symbol", "symbol": symbol}
        safe_timeframes = {"1d", "5d", "1mo", "3mo", "6mo", "1y"}
        if timeframe not in safe_timeframes:
            timeframe = "1d"

        market = get_connector("market_data").fetch({"symbol": symbol, "period": timeframe})
        news = get_connector("news").fetch({"symbol": symbol, "limit": 5})
        fundamentals = get_connector("fundamentals").fetch({"symbol": symbol})

        if not market.get("ok"):
            return {"ok": False, "error": "market_data_unavailable", "symbol": symbol}

        close = market.get("close", 0)
        prev_open = market.get("open", close)
        price_change_pct = round((close - prev_open) / prev_open * 100, 4) if prev_open else 0

        bull_case, bear_case, key_risks = [], [], ["macro rate environment"]

        pe = fundamentals.get("pe_ratio")
        roe = fundamentals.get("roe")

        if pe and isinstance(pe, (int, float)) and pe < 25:
            bull_case.append(f"PE ratio {pe} — reasonable valuation")
        if pe and isinstance(pe, (int, float)) and pe > 40:
            bear_case.append(f"PE ratio {pe} — stretched valuation")
        if roe and isinstance(roe, (int, float)) and roe > 0.20:
            bull_case.append(f"ROE {round(roe * 100, 1)}% — strong returns")
        if price_change_pct > 1.0:
            bull_case.append(f"Price up {price_change_pct}% — positive momentum")
        elif price_change_pct < -1.0:
            bear_case.append(f"Price down {abs(price_change_pct)}% — negative momentum")

        # --- Sanitized news keyword matching ---
        for item in (news.get("items") or [])[:3]:
            raw_title = item.get("title", "")
            if not isinstance(raw_title, str):
                continue
            title = raw_title.strip().lower()[:200]  # max 200 chars, no interpolation
            if any(w in title for w in _BULL_KEYWORDS):
                bull_case.append(f"News signal: {raw_title[:100]}")
            elif any(w in title for w in _BEAR_KEYWORDS):
                bear_case.append(f"News signal: {raw_title[:100]}")

        if not bull_case and not bear_case:
            bear_case.append("insufficient directional signal")

        # --- Capped confidence score ---
        raw_confidence = 0.40 + len(bull_case) * 0.08 + len(bear_case) * 0.03
        confidence = round(min(0.90, max(0.40, raw_confidence)), 3)

        sources = ["market_data", "news"] + (["fundamentals"] if fundamentals.get("ok") else [])
        note = {
            "asset": symbol,
            "timeframe": timeframe,
            "summary": f"{symbol} closed at {close}. Change: {price_change_pct}%. PE: {pe}. ROE: {roe}.",
            "bull_case": bull_case,
            "bear_case": bear_case,
            "key_risks": key_risks,
            "confidence": confidence,
            "sources_checked": sources,
            "market_snapshot": market,
            "fundamentals_snapshot": fundamentals,
            "news_snapshot": (news.get("items") or [])[:3],
        }
        audit.append({"actor": "research_agent", "action": "research_note_built", "asset": symbol})
        return {"ok": True, "research_note": note}
