"""Remediation & Recovery Specialist Agent."""
from ..harness.agent import Agent
from ..harness.models import BedrockModel
from ..tools.remediation import simulate_remediation_safety, execute_remediation

REMEDIATION_SYSTEM_PROMPT = """You are the Remediation & Recovery Specialist in the CloudOps SRE Swarm.
Your responsibility:
1. Receive root cause analysis and formulate a zero-downtime recovery strategy.
2. Simulate the remediation action using the AWS safety engine before proposing it.
3. Categorize the risk rating (LOW / MEDIUM / HIGH) and define explicit rollback procedures.
4. If human approval is required, formulate the exact change request payload."""

def create_remediation_agent(model: BedrockModel) -> Agent:
    return Agent(
        model=model,
        tools=[simulate_remediation_safety, execute_remediation],
        system_prompt=REMEDIATION_SYSTEM_PROMPT,
        name="RemediationSpecialist"
    )

