"""MCP tool wrapper — audit log (read-only)."""
from apps.fincept_aiops.audit_logger import AuditLogger

_audit = AuditLogger()


def get_audit_log(n: int = 20) -> dict:
    return {"records": _audit.recent(int(n))}
