"""FastAPI Server with SSE Event Streaming for CloudOps Swarm."""
import asyncio
import json
import time
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .swarm import CloudOpsSwarm
from .harness.hitl import HITLApprovalGateway
from .harness.cost_tracker import TokenCostTracker
from .chaos.fault_injector import ChaosFaultInjector
from .tools.exporters import export_to_slack_block_kit, export_to_jira_issue
from .web_dashboard import get_dashboard_html

app = FastAPI(
    title="CloudOps Autonomous Swarm API",
    description="Multi-Agent Incident Triaging & Self-Healing Service backed by Strands SDK & Amazon Bedrock",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

swarm = CloudOpsSwarm()
approval_gw = HITLApprovalGateway()
cost_tracker = TokenCostTracker()

class TriggerIncidentRequest(BaseModel):
    alarm_description: str
    region: Optional[str] = "us-east-1"

class ChaosRequest(BaseModel):
    fault_type: str
    target_service: Optional[str] = "checkout-service"

class ApprovalRequest(BaseModel):
    request_id: str
    approver: Optional[str] = "SRE_LEAD"

@app.get("/", response_class=HTMLResponse)
@app.get("/dashboard", response_class=HTMLResponse)
def get_dashboard():
    """Serves the interactive web dashboard for observing the multi-agent swarm."""
    return get_dashboard_html()

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CloudOps Swarm Engine",
        "bedrock_provider": "Anthropic Claude 3.5 Sonnet / Haiku",
        "timestamp": time.time()
    }

@app.post("/api/incident/trigger")
def trigger_incident(req: TriggerIncidentRequest):
    """Triggers end-to-end multi-agent autonomous triage and recovery."""
    result = swarm.handle_incident(req.alarm_description)
    cost = cost_tracker.record_usage(
        model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
        input_tokens=1420,
        output_tokens=580
    )
    result["finops_cost"] = {
        "incident_cost_usd": cost,
        "cumulative_summary": cost_tracker.get_summary()
    }
    result["slack_payload"] = export_to_slack_block_kit(result["incident_id"], req.alarm_description, result["final_post_mortem"])
    return result

@app.post("/api/chaos/inject")
def inject_chaos(req: ChaosRequest):
    """Injects a simulated chaos fault and executes the autonomous swarm response."""
    try:
        fault_data = ChaosFaultInjector.inject_fault(req.fault_type, req.target_service)
        result = swarm.handle_incident(fault_data["simulated_alarm"])
        result["chaos_injection"] = fault_data
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/approval/approve")
def approve_action(req: ApprovalRequest):
    """Human-in-the-Loop approval gateway for high-risk actions."""
    token = approval_gw.approve(req.request_id, req.approver)
    if not token:
        raise HTTPException(status_code=404, detail="Request ID not found or already processed.")
    return {"status": "APPROVED", "token": token}

