"""
BaseAgent — Abstract base class for all Fincept AI Ops agents.
Closes issue #14.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base class defining the contract for all Fincept agents."""

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        self.name = name
        self.config = config or {}
        self.logger = logging.getLogger(f"fincept.agent.{name}")
        self._initialized = False

    @abstractmethod
    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's primary task. Must be implemented by subclasses."""
        ...

    @abstractmethod
    def validate_input(self, payload: Dict[str, Any]) -> bool:
        """Validate input payload before execution."""
        ...

    def initialize(self) -> None:
        """Optional setup hook called before first run."""
        self._initialized = True
        self.logger.info(f"Agent '{self.name}' initialized.")

    def teardown(self) -> None:
        """Optional cleanup hook."""
        self.logger.info(f"Agent '{self.name}' teardown complete.")

    def emit_event(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Emit a structured audit event."""
        event = {
            "agent": self.name,
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "data": data
        }
        self.logger.info(json.dumps(event))
        return event

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}' initialized={self._initialized}>"
