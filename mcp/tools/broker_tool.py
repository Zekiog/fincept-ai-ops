"""MCP tool wrapper — paper broker (paper mode only; never live)."""
from apps.fincept_aiops.paper_broker import PaperBrokerAdapter

_broker = PaperBrokerAdapter()


def get_positions() -> dict:
    return {"positions": _broker.get_positions()}


def get_orders() -> dict:
    return {"orders": _broker.get_orders()}


def get_portfolio_summary() -> dict:
    return _broker.get_summary()
