"""MCP tool wrappers — single source of truth for tool implementations.

Each function here is what `mcp/server.py` dispatches to. Keep these thin —
business logic lives in `apps/fincept_aiops/`.
"""
from mcp.tools.audit_tool import get_audit_log
from mcp.tools.backtest_tool import run_backtest
from mcp.tools.briefing_tool import build_briefing
from mcp.tools.broker_tool import get_orders, get_portfolio_summary, get_positions
from mcp.tools.market_data import get_fundamentals, get_market_data, get_news
from mcp.tools.research_execution import get_paper_state, run_research_pipeline
from mcp.tools.risk_tool import evaluate_risk

__all__ = [
    "get_audit_log",
    "run_backtest",
    "build_briefing",
    "get_orders",
    "get_portfolio_summary",
    "get_positions",
    "get_fundamentals",
    "get_market_data",
    "get_news",
    "get_paper_state",
    "run_research_pipeline",
    "evaluate_risk",
]
