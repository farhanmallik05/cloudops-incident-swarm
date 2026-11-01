"""Deep Root Cause Diagnostic Specialist Agent."""
from ..harness.agent import Agent
from ..harness.models import BedrockModel
from ..tools.git_tools import get_recent_git_deployments, fetch_commit_diff
from ..tools.health_tools import get_aws_health_status

DIAGNOSTIC_SYSTEM_PROMPT = """You are the Deep Root Cause Diagnostic Specialist in the CloudOps SRE Swarm.
Your responsibility:
1. Receive triage findings (stack traces, timestamps, error signatures).
2. Query recent Git CI/CD deployments and inspect commit diffs.
3. Query AWS Health API to rule out regional cloud provider outages.
4. Establish the exact causal mechanism (code line, memory leak, unindexed query, or pool exhaustion) that triggered the incident.
Format your conclusion clearly with commit hash, author, and code line citations."""

def create_diagnostic_agent(model: BedrockModel) -> Agent:
    return Agent(
        model=model,
        tools=[get_recent_git_deployments, fetch_commit_diff, get_aws_health_status],
        system_prompt=DIAGNOSTIC_SYSTEM_PROMPT,
        name="DiagnosticSpecialist"
    )

