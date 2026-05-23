"""Security middleware — API key auth, rate limiting, CORS hardening, request size limits."""
import os
import time
from collections import defaultdict
from fastapi import Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# ---------------------------------------------------------------------------
# API Key Authentication
# ---------------------------------------------------------------------------
_API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)

_UNPROTECTED_PATHS = {"/", "/health", "/docs", "/openapi.json", "/redoc"}


def get_api_key(api_key: str = Depends(_API_KEY_HEADER)) -> str:
    """FastAPI dependency — validates X-API-Key header against FINCEPT_API_KEY env var."""
    expected = os.getenv("FINCEPT_API_KEY", "")
    if not expected:
        raise HTTPException(
            status_code=500,
            detail={"ok": False, "error": "FINCEPT_API_KEY not configured on server"}
        )
    if not api_key or api_key != expected:
        raise HTTPException(
            status_code=401,
            detail={"ok": False, "error": "invalid_or_missing_api_key"},
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key


# ---------------------------------------------------------------------------
# Rate Limiting
# ---------------------------------------------------------------------------
class RateLimitMiddleware(BaseHTTPMiddleware):
    WINDOW_SECONDS = 60
    MAX_REQUESTS = int(os.getenv("RATE_LIMIT_PER_MIN", "60"))

    def __init__(self, app):
        super().__init__(app)
        self._counts: dict = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self.WINDOW_SECONDS
        self._counts[ip] = [t for t in self._counts[ip] if t > window_start]
        if len(self._counts[ip]) >= self.MAX_REQUESTS:
            return JSONResponse(
                {"ok": False, "error": "rate_limit_exceeded", "retry_after": self.WINDOW_SECONDS},
                status_code=429,
                headers={"Retry-After": str(self.WINDOW_SECONDS)},
            )
        self._counts[ip].append(now)
        return await call_next(request)


# ---------------------------------------------------------------------------
# Request Size Limit
# ---------------------------------------------------------------------------
class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    MAX_BYTES = int(os.getenv("MAX_REQUEST_BYTES", str(1 * 1024 * 1024)))

    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > self.MAX_BYTES:
            return JSONResponse({"ok": False, "error": "request_too_large"}, status_code=413)
        return await call_next(request)


# ---------------------------------------------------------------------------
# CORS Origins
# ---------------------------------------------------------------------------
def get_cors_origins() -> list:
    """Returns allowed CORS origins. Never returns wildcard '*' in production."""
    raw = os.getenv("CORS_ORIGINS", "")
    env = os.getenv("APP_ENV", "development").lower()
    if not raw:
        if env == "production":
            # Production must have explicit CORS_ORIGINS set
            raise RuntimeError("CORS_ORIGINS must be explicitly set in production. Wildcard '*' is not allowed.")
        return ["http://localhost:3000", "http://localhost:8000"]
    if raw.strip() == "*":
        if env == "production":
            raise RuntimeError("CORS_ORIGINS='*' is not allowed in production.")
        return ["*"]  # dev/test only
    return [o.strip() for o in raw.split(",") if o.strip()]
