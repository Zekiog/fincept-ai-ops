"""
MCP Tool definitions for Fincept AI Ops.
Closes issue #15.

Each tool follows the Model Context Protocol (MCP) schema.
These are registered with the N8N MCP connector and FastAPI /mcp/tools endpoint.
"""
from typing import Any, Dict, List


MCP_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "get_market_data",
        "description": "Fetch real-time or historical market data for a given ticker symbol.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "ticker": {"type": "string", "description": "Stock ticker, e.g. AAPL, TSLA"},
                "interval": {"type": "string", "enum": ["1m", "5m", "1h", "1d"], "default": "1d"},
                "limit": {"type": "integer", "default": 30, "maximum": 500}
            },
            "required": ["ticker"]
        }
    },
    {
        "name": "run_backtest",
        "description": "Run a supervised paper-trading backtest over historical data.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "strategy_id": {"type": "string", "description": "ID of the registered strategy"},
                "start_date": {"type": "string", "format": "date", "description": "YYYY-MM-DD"},
                "end_date": {"type": "string", "format": "date", "description": "YYYY-MM-DD"},
                "initial_capital": {"type": "number", "default": 10000}
            },
            "required": ["strategy_id", "start_date", "end_date"]
        }
    },
    {
        "name": "get_audit_log",
        "description": "Retrieve the audit log for agent actions and trade decisions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "agent_name": {"type": "string", "description": "Filter by agent name (optional)"},
                "limit": {"type": "integer", "default": 50},
                "since": {"type": "string", "format": "date-time"}
            }
        }
    },
    {
        "name": "approve_trade",
        "description": "Human-in-the-loop trade approval endpoint. Approves or rejects a pending trade signal.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "trade_id": {"type": "string"},
                "decision": {"type": "string", "enum": ["approve", "reject"]},
                "reason": {"type": "string"}
            },
            "required": ["trade_id", "decision"]
        }
    },
    {
        "name": "list_strategies",
        "description": "List all registered trading strategies with their status and performance metrics.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["active", "paused", "all"], "default": "all"}
            }
        }
    }
]


def get_tool_by_name(name: str) -> Dict[str, Any] | None:
    """Look up an MCP tool definition by name."""
    return next((t for t in MCP_TOOLS if t["name"] == name), None)
