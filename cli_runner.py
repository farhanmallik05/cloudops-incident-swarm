#!/usr/bin/env python3
"""Interactive Terminal Runner & Operations CLI for CloudOps Multi-Agent Swarm.

Supports incident triaging, benchmark evaluations, chaos fault injection,
exporting to Slack/Jira, and launching the Web UI server.
"""
import sys
import time
import argparse
import json

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.swarm import CloudOpsSwarm
from src.chaos.fault_injector import ChaosFaultInjector
from src.tools.exporters import export_to_slack_block_kit, export_to_jira_issue
from src.tools.webhook_dispatcher import WebhookDispatcher
from src.harness.benchmark_evaluator import SwarmBenchmarkEvaluator, BENCHMARK_SCENARIOS

def main():
    parser = argparse.ArgumentParser(
        description="CloudOps Autonomous Multi-Agent SRE Swarm (Strands SDK + Amazon Bedrock)"
    )
    parser.add_argument(
        "--scenario",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Execute a specific benchmark scenario (1-5)",
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run the complete 5-scenario evaluation benchmark harness",
    )
    parser.add_argument(
        "--chaos",
        type=str,
        choices=["leak", "timeout", "oom"],
        help="Inject a synthetic chaos failure into target microservices",
    )
    parser.add_argument(
        "--export-slack",
        action="store_true",
        help="Export incident investigation to Slack Block Kit format",
    )
    parser.add_argument(
        "--export-jira",
        action="store_true",
        help="Export incident investigation to Jira Issue ticket schema",
    )
    parser.add_argument(
        "--web",
        action="store_true",
        help="Launch the interactive FastAPI Web Dashboard server on port 8000",
    )

    args = parser.parse_args()

    # Route: Web UI Server
    if args.web:
        import uvicorn
        print("[*] Launching CloudOps Swarm Web Dashboard on http://localhost:8000 ...")
        uvicorn.run("src.web_api:app", host="0.0.0.0", port=8000, reload=False)
        return

    # Route: Benchmark Harness
    if args.benchmark:
        print("[*] Running Swarm Benchmark Evaluator...\n")
        evaluator = SwarmBenchmarkEvaluator()
        summary = evaluator.run_all()
        for sc in summary["scenarios"]:
            icon = "[PASS]" if sc["passed"] else "[FAIL]"
            print(f" {icon} {sc['id']} - {sc['name']}")
            print(f"        Duration: {sc['duration_s']}s | Cost: ${sc['cost_usd']:.5f} | Incident: {sc['incident_id']}")
        print(f"\n[+] BENCHMARK ACCURACY: {summary['accuracy_score_pct']}% ({summary['passed_scenarios']}/{summary['total_scenarios']} passed)")
        print(f"[+] Total Bedrock Invocations Cost: ${summary['total_finops_cost_usd']:.5f} USD")
        return

    # Determine Alarm
    if args.chaos:
        fault_map = {
            "leak": "connection_pool_leak",
            "timeout": "504_gateway_timeout",
            "oom": "memory_saturation",
        }
        fault_data = ChaosFaultInjector.inject_fault(fault_map[args.chaos], "checkout-service")
        test_alarm = fault_data["simulated_alarm"]
        print(f"[!] CHAOS INJECTED ({fault_data['fault']}): {fault_data['description']}")
    elif args.scenario:
        sc = BENCHMARK_SCENARIOS[args.scenario - 1]
        test_alarm = sc.alarm_text
        print(f"[*] RUNNING BENCHMARK SCENARIO #{args.scenario}: {sc.name}")
    else:
        test_alarm = (
            "CRITICAL: CloudWatch Alarm 'High5XXGatewayTimeouts' triggered for service "
            "'checkout-service' in us-east-1. Error rate 14.8% exceeding threshold 5.0%."
        )

    print("=" * 80)
    print("[*] CLOUDOPS AUTONOMOUS MULTI-AGENT SRE SWARM")
    print("Powered by Strands Agents SDK & Amazon Bedrock (Claude 3.5 Sonnet / Haiku)")
    print("=" * 80)
    print(f"\n[!] INCOMING TELEMETRY ALARM:\n   {test_alarm}\n")
    print("Initiating autonomous multi-agent swarm collaboration...\n")

    swarm = CloudOpsSwarm(region_name="us-east-1")
    result = swarm.handle_incident(test_alarm)

    print("\n" + "=" * 80)
    print("[+] MULTI-AGENT INCIDENT TIMELINE & INVESTIGATION TRACE")
    print("=" * 80)

    for event in result["lifecycle_events"]:
        print(f"\n[-] Stage: {event['stage']} ({event['duration_ms']} ms)")
        print(f"   Specialist: {event['agent']}")
        print(f"   Summary: {event['summary'][:200]}...")

    print("\n" + "=" * 80)
    print("[+] FINAL SRE EXECUTIVE POST-MORTEM")
    print("=" * 80)
    print(result["final_post_mortem"])
    print("\n" + "=" * 80)
    print(f"[i] Total Autonomous Investigation Duration: {result['total_investigation_time_sec']} seconds")
    print(f"[i] Incident Reference ID: {result['incident_id']}")
    print("=" * 80)

    dispatcher = WebhookDispatcher()

    # Route: Export to Slack
    if args.export_slack:
        slack_payload = export_to_slack_block_kit(result["incident_id"], test_alarm, result["final_post_mortem"])
        dispatch_res = dispatcher.dispatch_to_slack(slack_payload)
        print("\n[+] SLACK BLOCK KIT DISPATCH RESULT:")
        print(json.dumps(dispatch_res, indent=2))

    # Route: Export to Jira
    if args.export_jira:
        jira_payload = export_to_jira_issue(result["incident_id"], result["final_post_mortem"])
        dispatch_res = dispatcher.dispatch_to_jira(jira_payload)
        print("\n[+] JIRA TICKET DISPATCH RESULT:")
        print(json.dumps(dispatch_res, indent=2))

if __name__ == "__main__":
    main()
