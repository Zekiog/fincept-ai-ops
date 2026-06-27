"""Smoke tests for MCP server tool dispatch."""
import os
os.environ["MARKET_DATA_PROVIDER"] = "stub"
os.environ["STATE_PATH"] = "/tmp/mcp_test_state"
os.environ["AUDIT_LOG_PATH"] = "/tmp/mcp_test_audit.jsonl"

import sys
sys.path.insert(0, ".")
from mcp.server import _call_tool, _tool_list


def test_tool_list_not_empty():
    result = _tool_list()
    assert len(result["tools"]) >= 6


def test_get_market_data_stub():
    r = _call_tool("get_market_data", {"symbol": "AAPL"})
    assert r.get("ok") is True
    assert r.get("stub") is True


def test_get_fundamentals_stub():
    r = _call_tool("get_fundamentals", {"symbol": "AAPL"})
    assert r.get("ok") is True


def test_get_news_stub():
    r = _call_tool("get_news", {"symbol": "AAPL", "limit": 2})
    assert r.get("ok") is True


def test_run_research_pipeline_valid():
    r = _call_tool("run_research_pipeline", {"research_note": {
        "asset": "AAPL", "timeframe": "1d",
        "summary": "Strong earnings.", "confidence": 0.82,
        "sources_checked": ["bloomberg", "reuters"],
        "bull_case": ["EPS beat"], "bear_case": [],
    }})
    assert r.get("ok") is True


def test_get_paper_state():
    r = _call_tool("get_paper_state", {})
    assert isinstance(r, dict)


def test_run_backtest():
    r = _call_tool("run_backtest", {
        "signal": {"side": "buy", "size_pct": 0.05, "asset": "AAPL"},
        "price_series": [100.0, 110.0],
    })
    assert r.get("ok") is True


def test_evaluate_risk_approved():
    r = _call_tool("evaluate_risk", {
        "order_intent": {"asset": "AAPL", "side": "buy", "thesis": "EPS beat", "size_pct": 0.05},
    })
    assert r.get("status") == "approved"
    assert "score" in r
    assert "limits_applied" in r


def test_evaluate_risk_rejected_size():
    r = _call_tool("evaluate_risk", {
        "order_intent": {"asset": "AAPL", "side": "buy", "thesis": "EPS beat", "size_pct": 0.50},
    })
    assert r.get("status") == "rejected"
    assert "size_too_large" in r.get("reason_codes", [])


def test_build_briefing():
    r = _call_tool("build_briefing", {})
    assert isinstance(r, dict)
    assert "date" in r
    assert "pending_actions" in r


def test_build_briefing_with_extra():
    r = _call_tool("build_briefing", {"extra": {"market_summary": "Bull run"}})
    assert r.get("market_summary") == "Bull run"


def test_get_audit_log_empty():
    r = _call_tool("get_audit_log", {"n": 5})
    assert "records" in r
    assert isinstance(r["records"], list)


def test_get_portfolio_summary():
    r = _call_tool("get_portfolio_summary", {})
    assert isinstance(r, dict)
    assert "open_positions" in r
    assert "realized_pnl" in r


def test_tool_list_includes_required_tools():
    """Verify the tool list exposes at least all 7 required tool categories."""
    result = _tool_list()
    names = {t["name"] for t in result["tools"]}
    required = {
        "get_market_data",
        "run_research_pipeline",
        "get_portfolio_summary",
        "run_backtest",
        "evaluate_risk",
        "build_briefing",
        "get_audit_log",
    }
    assert required.issubset(names), f"Missing tools: {required - names}"


def test_unknown_tool_returns_error():
    r = _call_tool("nonexistent_tool", {})
    assert "error" in r
