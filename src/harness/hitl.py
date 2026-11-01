"""Human-in-the-Loop (HITL) Authorization and Token Gateway for Strands SDK."""
import hmac
import hashlib
import time
from typing import Dict, Any, Optional

class HITLApprovalGateway:
    """Enforces cryptographic approval tokens for high-risk autonomous infrastructure actions."""

    def __init__(self, secret_key: str = "aws-hackathon-strands-safety-secret"):
        self.secret_key = secret_key.encode("utf-8")
        self.pending_requests: Dict[str, Dict[str, Any]] = {}

    def request_approval(self, action: str, parameters: Dict[str, Any], risk_rating: str) -> str:
        """Generates a pending approval request and returns a unique request ID."""
        request_id = f"REQ-{int(time.time())}-{hash(action) % 10000}"
        token = hmac.new(self.secret_key, f"{request_id}:{action}".encode("utf-8"), hashlib.sha256).hexdigest()[:16]

        self.pending_requests[request_id] = {
            "request_id": request_id,
            "action": action,
            "parameters": parameters,
            "risk_rating": risk_rating,
            "token": token,
            "status": "PENDING_APPROVAL",
            "created_at": time.time(),
        }
        return request_id

    def approve(self, request_id: str, approver_role: str = "SRE_LEAD") -> Optional[str]:
        """Approves a pending request and issues an execution token."""
        if request_id not in self.pending_requests:
            return None

        req = self.pending_requests[request_id]
        req["status"] = "APPROVED"
        req["approved_by"] = approver_role
        req["approved_at"] = time.time()
        return req["token"]

    def verify_token(self, request_id: str, token: str) -> bool:
        """Verifies whether an execution token is authentic and authorized."""
        if request_id not in self.pending_requests:
            return False
        req = self.pending_requests[request_id]
        return req["status"] == "APPROVED" and hmac.compare_digest(req["token"], token)

