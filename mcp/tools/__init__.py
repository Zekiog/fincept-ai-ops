"""
MCP Tool definitions for Fincept AI Ops.
Closes issue #15.

Each tool follows the Model Context Protocol (MCP) schema.
These are registered with the N8N MCP connector and FastAPI /mcp/tools endpoint.
"""
from typing import Any, Dict, List

from mcp.tools.market_data_tool import get_market_data, get_fundamentals, get_news
from mcp.tools.research_tool import run_research_pipeline, get_paper_state
from mcp.tools.broker_tool import get_positions, get_orders, get_portfolio_summary
from mcp.tools.backtest_tool import run_backtest
from mcp.tools.risk_tool import evaluate_risk
from mcp.tools.briefing_tool import build_briefing
from mcp.tools.audit_tool import get_audit_log

__all__ = [
    "get_market_data",
    "get_fundamentals",
    "get_news",
    "run_research_pipeline",
    "get_paper_state",
    "get_positions",
    "get_orders",
    "get_portfolio_summary",
    "run_backtest",
    "evaluate_risk",
    "build_briefing",
    "get_audit_log",
]

MCP_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "get_market_data",
        "description": "Fetch OHLCV price data for a symbol.",
        "inputSchema": {
            "type": "object",
            "required": ["symbol"],
            "properties": {
                "symbol": {"type": "string", "description": "Ticker symbol e.g. AAPL"},
                "period": {"type": "string", "description": "yfinance period e.g. 1d, 5d, 1mo", "default": "1d"},
            },
        },
    },
    {
        "name": "get_fundamentals",
        "description": "Fetch fundamental data (PE, ROE, market cap) for a symbol.",
        "inputSchema": {
            "type": "object",
            "required": ["symbol"],
            "properties": {"symbol": {"type": "string"}},
        },
    },
    {
        "name": "get_news",
        "description": "Fetch recent news headlines for a symbol.",
        "inputSchema": {
            "type": "object",
            "required": ["symbol"],
            "properties": {
                "symbol": {"type": "string"},
                "limit": {"type": "integer", "default": 5},
            },
        },
    },
    {
        "name": "run_research_pipeline",
        "description": "Run the full research pipeline on a pre-built research note.",
        "inputSchema": {
            "type": "object",
            "required": ["research_note"],
            "properties": {
                "research_note": {"type": "object"},
            },
        },
    },
    {
        "name": "get_paper_state",
        "description": "Get current paper trading state: signal, risk, briefing, approval.",
        "inputSchema": {"type": "object", "properties": {}},
    },
    {
        "name": "get_audit_log",
        "description": "Get the last N audit log records.",
        "inputSchema": {
            "type": "object",
            "properties": {"n": {"type": "integer", "default": 20}},
        },
    },
    {
        "name": "run_backtest",
        "description": "Run a simple vectorized backtest on a signal against a price series.",
        "inputSchema": {
            "type": "object",
            "required": ["signal", "price_series"],
            "properties": {
                "signal": {"type": "object"},
                "price_series": {"type": "array", "items": {"type": "number"}},
                "initial_equity": {"type": "number", "default": 10000.0},
            },
        },
    },
    {
        "name": "evaluate_risk",
        "description": "Evaluate an order intent against the risk policy.",
        "inputSchema": {
            "type": "object",
            "required": ["order_intent"],
            "properties": {
                "order_intent": {"type": "object"},
                "portfolio_context": {"type": "object"},
            },
        },
    },
    {
        "name": "build_briefing",
        "description": "Build today's briefing packet.",
        "inputSchema": {
            "type": "object",
            "properties": {"extra": {"type": "object"}},
        },
    },
    {
        "name": "get_portfolio_summary",
        "description": "Get the current paper portfolio summary (cash, exposure, P&L).",
        "inputSchema": {"type": "object", "properties": {}},
    },
]


def get_tool_by_name(name: str) -> Dict[str, Any] | None:
    """Look up an MCP tool definition by name."""
    return next((t for t in MCP_TOOLS if t["name"] == name), None)
