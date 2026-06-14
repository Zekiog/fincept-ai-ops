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

    def run(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """Canonical entrypoint: append a record. Use recent() for reads."""
        self._set_status(AgentStatus.RUNNING)
        try:
            self.log(record)
            self._set_status(AgentStatus.IDLE)
            return {"ok": True}
        except Exception:
            self._set_status(AgentStatus.ERROR)
            raise
