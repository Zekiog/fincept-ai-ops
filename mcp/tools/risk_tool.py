"""MCP tool wrapper — risk policy evaluation."""
from apps.fincept_aiops.risk_policy import RiskPolicy

_policy = RiskPolicy()


def evaluate_risk(order_intent: dict, portfolio_context: dict | None = None) -> dict:
    return _policy.evaluate(order_intent, portfolio_context or {})
