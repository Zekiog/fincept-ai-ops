"""MCP tool wrapper — daily briefing."""
from apps.fincept_aiops.daily_briefing import DailyBriefingGenerator

_briefing = DailyBriefingGenerator()


def build_briefing(extra: dict | None = None) -> dict:
    return _briefing.build(extra or {})
