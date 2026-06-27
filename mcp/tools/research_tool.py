"""MCP tool wrapper — research pipeline execution."""
from apps.fincept_aiops.research_pipeline import ResearchPipeline
from apps.fincept_aiops.state_store import StateStore

_pipeline = ResearchPipeline()
_state = StateStore()


def run_research_pipeline(research_note: dict) -> dict:
    return _pipeline.run(research_note)


def get_paper_state() -> dict:
    return {
        "signal": _state.load("latest_signal_candidate"),
        "risk": _state.load("latest_risk"),
        "briefing": _state.load("latest_briefing"),
        "approval": _state.load("latest_approval"),
    }
