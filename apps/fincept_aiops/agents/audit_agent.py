from typing import Any, Dict

from apps.fincept_aiops.agents.base_agent import AgentStatus, BaseAgent
from apps.fincept_aiops.audit_logger import AuditLogger


class AuditAgent(BaseAgent):
    """Agent 6 — append-only audit trail."""

    def __init__(self) -> None:
        super().__init__()
        self.logger = AuditLogger()

    def log(self, record: Dict[str, Any]) -> None:
        self.logger.append(record)

    def recent(self, n: int = 50):
        return self.logger.recent(n)

    def run(self, record: Dict[str, Any] | None = None, n: int = 50) -> Any:
        """Canonical entrypoint: append a record if given, else return recent."""
        self._set_status(AgentStatus.RUNNING)
        try:
            if record is not None:
                self.log(record)
                result = {"ok": True}
            else:
                result = {"records": self.recent(n)}
            self._set_status(AgentStatus.IDLE)
            return result
        except Exception:
            self._set_status(AgentStatus.ERROR)
            raise
