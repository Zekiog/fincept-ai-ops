import os

os.environ["RATE_LIMIT_PER_MIN"] = "3"
os.environ["CORS_ORIGINS"] = "http://localhost:3000"
os.environ.setdefault("FINCEPT_API_KEY", "test-api-key")
os.environ.setdefault("APPROVAL_SECRET", "test-approval-secret")

import pytest
from fastapi.testclient import TestClient

from apps.fincept_aiops.app import app


@pytest.fixture(autouse=True)
def _reset_rate_limit_state():
    """RateLimitMiddleware keeps an in-memory per-IP counter that leaks across
    tests. Reset it before every test so the per-test budget is honored."""
    for mw in app.user_middleware:
        if mw.cls.__name__ == "RateLimitMiddleware":
            inst = getattr(mw, "kwargs", {})  # not directly reachable; rely on instance below
    # The actual instance is created by Starlette at first request. Easiest:
    # access through the middleware stack after the app is built.
    if app.middleware_stack is not None:
        stack = app.middleware_stack
        while stack is not None and hasattr(stack, "app"):
            if type(stack).__name__ == "RateLimitMiddleware":
                stack._counts.clear()
                break
            stack = getattr(stack, "app", None)
    yield


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)


def test_health_under_rate_limit(client):
    for _ in range(3):
        r = client.get("/health")
        assert r.status_code == 200


def test_rate_limit_trips_on_fourth_request(client):
    for _ in range(3):
        assert client.get("/health").status_code == 200
    assert client.get("/health").status_code == 429


def test_cors_origin_header_present(client):
    r = client.get("/health", headers={"Origin": "http://localhost:3000"})
    assert r.status_code == 200


def test_request_too_large(client):
    big_payload = {"research_note": {"asset": "A" * 2_000_000}}
    r = client.post(
        "/research/run",
        json=big_payload,
        headers={"Content-Length": str(2_000_000)},
    )
    assert r.status_code in (413, 422)
