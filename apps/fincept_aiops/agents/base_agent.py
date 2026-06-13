"""BaseAgent — common ABC + thread-safe status enum for every agent."""
from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class AgentStatus(str, Enum):
    IDLE = "idle"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


class BaseAgent(ABC):
    """Abstract base class for every Fincept agent.

    Subclasses keep their domain verb (`evaluate`, `execute`, `log`, ...) but
    must implement `run()` as the canonical entrypoint and expose status via
    `get_status()`.

    Cancellation: `stop()` sets a `threading.Event` and updates status.
    Long-running `run()` implementations should poll `should_stop()` at safe
    points and return early when it's True. The status update alone does not
    interrupt execution.
    """

    def __init__(self) -> None:
        self._status = AgentStatus.IDLE
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

    def _set_status(self, status: AgentStatus) -> None:
        with self._lock:
            self._status = status

    def get_status(self) -> AgentStatus:
        with self._lock:
            return self._status

    def stop(self) -> None:
        """Signal cancellation. Run loops should check `should_stop()`."""
        self._stop_event.set()
        self._set_status(AgentStatus.STOPPED)

    def should_stop(self) -> bool:
        return self._stop_event.is_set()

    def wait_for_stop(self, timeout: float | None = None) -> bool:
        """Block up to ``timeout`` seconds or until stop is requested."""
        return self._stop_event.wait(timeout)

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Canonical entrypoint. Implementations should set status to RUNNING
        on entry, IDLE on success, and ERROR on exception."""
