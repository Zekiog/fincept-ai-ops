import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from apps.fincept_aiops.state_store import StateStore
from apps.fincept_aiops.audit_logger import AuditLogger

router = APIRouter(tags=["approval"])
state = StateStore()
audit = AuditLogger()


class ApprovalRequest(BaseModel):
    approved: bool
    approver_id: str
    reason: str = ""


_INSECURE_DEFAULTS = {"", "changeme"}


def _resolve_approval_secret() -> str:
    """Resolve APPROVAL_SECRET; reject empty/'changeme' in production."""
    secret = os.getenv("APPROVAL_SECRET", "")
    if os.getenv("APP_ENV", "development").lower() == "production" and secret in _INSECURE_DEFAULTS:
        raise RuntimeError(
            "APPROVAL_SECRET must be set to a non-default value in production. "
            "Generate with: openssl rand -hex 32"
        )
    return secret


@router.post("/approval/webhook")
def handle_approval(req: ApprovalRequest, x_approval_secret: str = Header(default="")):
    expected = _resolve_approval_secret()
    if not expected or x_approval_secret != expected:
        raise HTTPException(status_code=403, detail="invalid_secret")
    record = {"human_approved": req.approved, "approver_id": req.approver_id,
               "approved_at": datetime.utcnow().isoformat() + "Z", "reason": req.reason}
    state.save("latest_approval", record)
    audit.append({"actor": req.approver_id, "action": "approval_decision",
                  "approved": req.approved, "reason": req.reason})
    return {"ok": True, "record": record}
