from apps.fincept_aiops.agents.base_agent import AgentStatus, BaseAgent
from apps.fincept_aiops.daily_briefing import DailyBriefingGenerator


class BriefingAgent(BaseAgent):
    """Agent 5 — composes and persists daily briefing packet."""

    def __init__(self) -> None:
        super().__init__()
        self.generator = DailyBriefingGenerator()

    def run(self, extra: dict | None = None) -> dict:
        self._set_status(AgentStatus.RUNNING)
        try:
            result = self.generator.build(extra or {})
            self._set_status(AgentStatus.IDLE)
            return result
        except Exception:
            self._set_status(AgentStatus.ERROR)
            raise
