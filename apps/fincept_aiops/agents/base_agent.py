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
    """

    def __init__(self) -> None:
        self._status = AgentStatus.IDLE
        self._lock = threading.Lock()

    def _set_status(self, status: AgentStatus) -> None:
        with self._lock:
            self._status = status

    def get_status(self) -> AgentStatus:
        with self._lock:
            return self._status

    def stop(self) -> None:
        self._set_status(AgentStatus.STOPPED)

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Canonical entrypoint. Implementations should set status to RUNNING
        on entry and IDLE/ERROR on exit."""
