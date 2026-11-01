#!/usr/bin/env python3
"""CLI Runner for Multi-Agent SRE Swarm Benchmark Evaluation Harness."""
import sys
import json
from src.harness.benchmark_evaluator import SwarmBenchmarkEvaluator

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def main():
    print("=" * 80)
    print("[*] CLOUDOPS STRANDS SRE SWARM: MULTI-SCENARIO BENCHMARK EVALUATOR")
    print("=" * 80)
    print("Evaluating 5 Incident Archetypes against Autonomous Multi-Agent Swarm...\n")

    evaluator = SwarmBenchmarkEvaluator()
    summary = evaluator.run_all()

    for sc in summary["scenarios"]:
        status_icon = "[PASS]" if sc["passed"] else "[FAIL]"
        print(f" {status_icon} {sc['id']} - {sc['name']}")
        print(f"        Duration: {sc['duration_s']}s | Token Cost: ${sc['cost_usd']:.5f} | Incident: {sc['incident_id']}")
        print(f"        Triage: {'OK' if sc['triage_ok'] else 'FAIL'} | Diagnostic: {'OK' if sc['diagnostic_ok'] else 'FAIL'} | Remediation: {'OK' if sc['remediation_safe'] else 'FAIL'}\n")

    print("=" * 80)
    print(f"[+] BENCHMARK ACCURACY SCORE: {summary['accuracy_score_pct']}% ({summary['passed_scenarios']}/{summary['total_scenarios']} passed)")
    print(f"[+] Total Duration: {summary['total_duration_seconds']}s (Avg: {summary['average_scenario_seconds']}s/scenario)")
    print(f"[+] Total Bedrock Invocations Cost: ${summary['total_finops_cost_usd']:.5f} USD")
    print("=" * 80)

if __name__ == "__main__":
    main()

