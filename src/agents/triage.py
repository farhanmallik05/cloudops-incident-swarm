"""Telemetry & Log Triage Specialist Agent."""
from ..harness.agent import Agent
from ..harness.models import BedrockModel
from ..tools.cloudwatch import query_cloudwatch_insights, get_service_metrics

TRIAGE_SYSTEM_PROMPT = """You are the Telemetry & Log Triage Specialist in the CloudOps SRE Swarm.
Your responsibility:
1. Ingest production alarms and query Amazon CloudWatch Logs Insights.
2. Isolate the primary exception, affected endpoint, and timestamp of first emergence.
3. Quantify total error volume and peak error rates.
Be crisp, structured, and fact-focused. Do not make wild guesses beyond the evidence."""

def create_triage_agent(model: BedrockModel) -> Agent:
    return Agent(
        model=model,
        tools=[query_cloudwatch_insights, get_service_metrics],
        system_prompt=TRIAGE_SYSTEM_PROMPT,
        name="TriageSpecialist"
    )

