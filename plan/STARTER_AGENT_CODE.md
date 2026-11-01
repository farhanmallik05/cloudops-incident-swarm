# Starter Agent Code: Strands SDK Multi-Agent Swarm

This is a production-ready, fully commented Python implementation of a **Multi-Agent Incident Swarm** using the **Strands Agents SDK** and **Amazon Bedrock**.

---

## 🛠️ Requirements & Setup

```bash
pip install strands-agents boto3 botocore pydantic
```

Ensure your AWS credentials are configured (`aws configure`) and you have model access enabled for Claude in Amazon Bedrock (`us-east-1` or `us-west-2`).

---

## 🐍 Complete Executable Code (`swarm_main.py`)

```python
"""
CloudOps Swarm: Autonomous Incident Response Swarm
Built with Strands Agents SDK and Amazon Bedrock
"""

import json
import time
from typing import Dict, Any, List
from strands import Agent
from strands.models import BedrockModel

# ==============================================================================
# 1. AWS Tool Definitions (Strands Function Tools)
# ==============================================================================

def query_cloudwatch_logs(service_name: str, lookback_minutes: int = 15) -> Dict[str, Any]:
    """Queries Amazon CloudWatch Logs for 5XX errors, exceptions, and stack traces.

    Args:
        service_name: Name of the microservice or Lambda function (e.g. 'checkout-service').
        lookback_minutes: Minutes of telemetry to search (default: 15).
    """
    print(f"\n🔧 [TOOL EXECUTED] query_cloudwatch_logs(service='{service_name}', lookback={lookback_minutes}m)")
    # Simulated realistic AWS CloudWatch Logs Insights response
    return {
        "status": "success",
        "service": service_name,
        "total_errors_found": 842,
        "primary_error": "DBConnectionPoolTimeoutException: Timeout waiting for idle connection in pool.",
        "sample_stack_trace": [
            "File '/var/task/app/database.py', line 88, in acquire_connection",
            "File '/var/task/app/routes/checkout.py', line 42, in process_order",
            "DBConnectionPoolTimeoutException: Maximum pool size (20) exceeded."
        ],
        "affected_endpoint": "/api/v2/checkout/finalize",
        "first_occurrence_timestamp": "2026-10-30T17:14:02Z"
    }

def get_recent_git_deployments(service_name: str, limit: int = 3) -> Dict[str, Any]:
    """Retrieves recent CI/CD deployments and Git commit metadata for a service.

    Args:
        service_name: Name of the microservice.
        limit: Number of recent deployments to fetch.
    """
    print(f"\n🔧 [TOOL EXECUTED] get_recent_git_deployments(service='{service_name}', limit={limit})")
    # Simulated deployment history
    return {
        "service": service_name,
        "deployments": [
            {
                "commit_hash": "c8a41df",
                "author": "dev-alex@company.com",
                "deployed_at": "2026-10-30T17:05:00Z",  # 9 minutes before error surge!
                "message": "feat(checkout): add user loyalty tier calculation during order finalization",
                "files_changed": ["app/routes/checkout.py", "app/services/loyalty.py"],
                "diff_summary": "Added synchronous DB query inside checkout loop without releasing connection context."
            },
            {
                "commit_hash": "b2f901a",
                "author": "sre-sarah@company.com",
                "deployed_at": "2026-10-29T11:20:00Z",
                "message": "chore: bump dependencies and base alpine image"
            }
        ]
    }

def simulate_remediation_safety(action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """Validates whether a proposed remediation step is safe and passes safety policies.

    Args:
        action: Remediation action name (e.g., 'ROLLBACK_DEPLOYMENT', 'EXPAND_DB_POOL').
        parameters: Configuration dictionary for the action.
    """
    print(f"\n🔧 [TOOL EXECUTED] simulate_remediation_safety(action='{action}', params={parameters})")
    if action == "ROLLBACK_DEPLOYMENT":
        return {
            "is_safe": True,
            "target_commit": parameters.get("target_commit", "b2f901a"),
            "estimated_downtime_seconds": 0,
            "rollback_method": "Blue/Green Traffic Shift via AWS CodeDeploy",
            "approval_required": "HUMAN_SRE_APPROVAL"
        }
    elif action == "EXPAND_DB_POOL":
        return {
            "is_safe": True,
            "proposed_pool_size": 40,
            "db_memory_impact": "Acceptable (RDS Aurora memory utilization at 38%)",
            "approval_required": "AUTO_APPROVED"
        }
    return {"is_safe": False, "reason": "Unknown remediation action."}

# ==============================================================================
# 2. Bedrock Model & Multi-Agent Swarm Setup
# ==============================================================================

def create_swarm():
    # Initialize Amazon Bedrock Foundation Models
    # Use Sonnet for high-reasoning tasks, Haiku for fast triage
    sonnet_model = BedrockModel(
        model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
        temperature=0.1
    )
    
    haiku_model = BedrockModel(
        model_id="anthropic.claude-3-5-haiku-20241022-v1:0",
        temperature=0.0
    )

    # Specialist 1: Triage & Telemetry Agent
    triage_agent = Agent(
        model=haiku_model,
        tools=[query_cloudwatch_logs],
        system_prompt="""You are the Telemetry & Triage Specialist.
Your responsibility is to analyze raw error logs and extract the exact error signature, 
stack trace, and time of first impact. Be crisp, concise, and structured."""
    )

    # Specialist 2: Deep Diagnostic Agent
    diagnostic_agent = Agent(
        model=sonnet_model,
        tools=[get_recent_git_deployments],
        system_prompt="""You are the Deep Diagnostic Specialist.
Your job is to identify the causal root cause of the incident. Correlate stack traces 
with recent git commit diffs, code changes, and architectural bottlenecks."""
    )

    # Specialist 3: Remediation Specialist Agent
    remediation_agent = Agent(
        model=sonnet_model,
        tools=[simulate_remediation_safety],
        system_prompt="""You are the Remediation Specialist.
Formulate a minimal, zero-downtime recovery plan. Always test actions through safety simulation.
Propose rollback or configuration fixes with explicit risk ratings."""
    )

    return triage_agent, diagnostic_agent, remediation_agent, sonnet_model

# ==============================================================================
# 3. Swarm Orchestration Workflow
# ==============================================================================

def run_incident_response(alarm_description: str):
    print("=" * 80)
    print("🚨 [INCIDENT TRIGGERED] CLOUDWATCH ALARM INGESTED")
    print(f"Trigger: {alarm_description}")
    print("=" * 80)

    triage_agent, diagnostic_agent, remediation_agent, supervisor_model = create_swarm()

    # Step 1: Triage Agent analyzes logs
    print("\n⏩ [STEP 1: SWARM DELEGATION] Involving Triage Specialist...")
    triage_prompt = f"Analyze CloudWatch logs for checkout-service following alarm: {alarm_description}"
    triage_result = triage_agent.run(triage_prompt)
    print("\n📋 [TRIAGE RESULT]:\n", triage_result)

    # Step 2: Diagnostic Agent establishes root cause
    print("\n⏩ [STEP 2: SWARM DELEGATION] Involving Diagnostic Specialist...")
    diagnostic_prompt = f"""Based on this triage analysis:
{triage_result}

Investigate recent git commits for checkout-service and determine the exact root cause."""
    diagnostic_result = diagnostic_agent.run(diagnostic_prompt)
    print("\n🔬 [DIAGNOSTIC RESULT]:\n", diagnostic_result)

    # Step 3: Remediation Agent designs safety-validated fix
    print("\n⏩ [STEP 3: SWARM DELEGATION] Involving Remediation Specialist...")
    remediation_prompt = f"""Given this root cause:
{diagnostic_result}

Formulate and simulate a remediation plan to recover checkout-service immediately."""
    remediation_result = remediation_agent.run(remediation_prompt)
    print("\n🛡️ [REMEDIATION PLAN]:\n", remediation_result)

    # Step 4: Incident Commander synthesizes executive post-mortem
    print("\n⏩ [STEP 4: COMMANDER SYNTHESIS] Generating Final Post-Mortem...")
    commander_agent = Agent(
        model=supervisor_model,
        system_prompt="""You are the Incident Commander. Synthesize the findings from 
the Triage, Diagnostic, and Remediation specialists into an executive SRE Incident Post-Mortem in Markdown."""
    )
    
    final_post_mortem = commander_agent.run(f"""
Triage Findings:
{triage_result}

Diagnostic Findings:
{diagnostic_result}

Remediation Recommendations:
{remediation_result}
""")

    print("\n" + "=" * 80)
    print("📄 FINAL SRE EXECUTIVE POST-MORTEM")
    print("=" * 80)
    print(final_post_mortem)

if __name__ == "__main__":
    test_alarm = "CRITICAL: HTTP 504 Gateway Timeout spike (>15% error rate) on checkout-service in us-east-1."
    run_incident_response(test_alarm)
```

