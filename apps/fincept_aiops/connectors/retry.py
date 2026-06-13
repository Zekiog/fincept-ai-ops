"""Retry + circuit-breaker decorator for external connector calls."""
import logging
import os
from functools import wraps
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)


def _env_int(key: str, default: int) -> int:
    try:
        return int(os.getenv(key, str(default)))
    except (TypeError, ValueError):
        return default


def with_retry(stop_attempts: int | None = None, wait_min: float = 1.0, wait_max: float | None = None):
    """Decorator: retry up to ``stop_attempts`` times with exponential backoff.

    When invoked without explicit args, both ``stop_attempts`` and ``wait_max``
    fall back to env vars ``CONNECTOR_RETRY_ATTEMPTS`` (default 3) and
    ``CONNECTOR_RETRY_WAIT_MAX`` (default 10).
    """
    attempts = stop_attempts if stop_attempts is not None else _env_int("CONNECTOR_RETRY_ATTEMPTS", 3)
    wmax = wait_max if wait_max is not None else _env_int("CONNECTOR_RETRY_WAIT_MAX", 10)

    def decorator(fn):
        @retry(
            stop=stop_after_attempt(attempts),
            wait=wait_exponential(multiplier=1, min=wait_min, max=wmax),
            retry=retry_if_exception_type(Exception),
            reraise=True,
        )
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:
                logger.warning("connector call %s failed: %s — retrying", fn.__name__, exc)
                raise

        return wrapper

    return decorator
