"""Shared pytest fixtures."""
import os

# Make sure auth-required tests can import the FastAPI app without 500'ing.
os.environ.setdefault("FINCEPT_API_KEY", "test-api-key")
os.environ.setdefault("APPROVAL_SECRET", "test-approval-secret")
os.environ.setdefault("MARKET_DATA_PROVIDER", "stub")

import pytest


def _reset_in_memory_counters() -> None:
    """RateLimitMiddleware holds a per-process in-memory counter that leaks
    state across tests sharing the same FastAPI app. Walk the middleware stack
    and clear it before each test."""
    try:
        from apps.fincept_aiops.app import app
    except Exception:
        return
    stack = getattr(app, "middleware_stack", None)
    seen = 0
    while stack is not None and seen < 20:
        if type(stack).__name__ == "RateLimitMiddleware":
            counts = getattr(stack, "_counts", None)
            if counts is not None:
                counts.clear()
            break
        stack = getattr(stack, "app", None)
        seen += 1


@pytest.fixture(autouse=True)
def _autouse_reset_rate_limit():
    _reset_in_memory_counters()
    yield
    _reset_in_memory_counters()
