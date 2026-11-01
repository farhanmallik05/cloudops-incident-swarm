"""CloudOps Multi-Agent Swarm Orchestrator."""
import time
from typing import Dict, Any, List
from .harness.models import BedrockModel
from .agents.triage import create_triage_agent
from .agents.diagnostic import create_diagnostic_agent
from .agents.remediation import create_remediation_agent
from .agents.commander import create_commander_agent

class CloudOpsSwarm:
    """Orchestrates 4 collaborating Strands agents across the incident lifecycle."""

    def __init__(self, region_name: str = "us-east-1"):
        # Model tiering: Sonnet for deep reasoning & Commander, Haiku for fast triage
        self.sonnet_model = BedrockModel(
            model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
            region_name=region_name,
            temperature=0.1
        )
        self.haiku_model = BedrockModel(
            model_id="anthropic.claude-3-5-haiku-20241022-v1:0",
            region_name=region_name,
            temperature=0.0
        )

        self.triage_agent = create_triage_agent(self.haiku_model)
        self.diagnostic_agent = create_diagnostic_agent(self.sonnet_model)
        self.remediation_agent = create_remediation_agent(self.sonnet_model)
        self.commander_agent = create_commander_agent(self.sonnet_model)

    def handle_incident(self, alarm_description: str) -> Dict[str, Any]:
        """Runs the 4-phase autonomous swarm response pipeline."""
        start_time = time.time()
        lifecycle_events: List[Dict[str, Any]] = []

        # Phase 1: Triage
        triage_prompt = f"Alarm Details: {alarm_description}\nInvestigate CloudWatch logs for service errors and affected endpoints."
        triage_output = self.triage_agent.run(triage_prompt)
        lifecycle_events.append({
            "stage": "TRIAGE",
            "agent": "Telemetry & Log Triage Specialist",
            "status": "COMPLETED",
            "summary": triage_output,
            "duration_ms": int((time.time() - start_time) * 1000)
        })

        # Phase 2: Root Cause Diagnostics
        diag_prompt = f"""Triage Findings:
{triage_output}

Correlate this stack trace with recent git deployments and verify AWS Health. Determine root cause."""
        diag_start = time.time()
        diag_output = self.diagnostic_agent.run(diag_prompt)
        lifecycle_events.append({
            "stage": "DIAGNOSTICS",
            "agent": "Deep Root Cause Diagnostic Specialist",
            "status": "COMPLETED",
            "summary": diag_output,
            "duration_ms": int((time.time() - diag_start) * 1000)
        })

        # Phase 3: Remediation & Safety Verification
        rem_prompt = f"""Diagnostic Result:
{diag_output}

Formulate a safe, zero-downtime remediation strategy and verify it with the safety engine."""
        rem_start = time.time()
        rem_output = self.remediation_agent.run(rem_prompt)
        lifecycle_events.append({
            "stage": "REMEDIATION",
            "agent": "Remediation & Recovery Specialist",
            "status": "COMPLETED",
            "summary": rem_output,
            "duration_ms": int((time.time() - rem_start) * 1000)
        })

        # Phase 4: Commander Executive Synthesis
        comm_start = time.time()
        commander_prompt = f"""Alarm: {alarm_description}

Triage Results:
{triage_output}

Diagnostic Results:
{diag_output}

Remediation Plan:
{rem_output}

Synthesize a comprehensive, executive Markdown SRE Incident Post-Mortem."""
        final_post_mortem = self.commander_agent.run(commander_prompt)
        lifecycle_events.append({
            "stage": "SYNTHESIS",
            "agent": "Incident Commander (Supervisor)",
            "status": "COMPLETED",
            "summary": "Executive Post-Mortem Generated",
            "duration_ms": int((time.time() - comm_start) * 1000)
        })

        total_duration_sec = round(time.time() - start_time, 2)

        return {
            "incident_id": f"INC-AWS-{int(time.time())}",
            "alarm": alarm_description,
            "total_investigation_time_sec": total_duration_sec,
            "lifecycle_events": lifecycle_events,
            "trace": lifecycle_events,
            "final_post_mortem": final_post_mortem,
        }

