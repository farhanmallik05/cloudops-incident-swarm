# CloudOps Swarm: Autonomous AWS Incident Triaging & Self-Healing Multi-Agent Swarm

CloudOps Swarm is a production-grade multi-agent autonomous system built on the **Strands Agents SDK** and **Amazon Bedrock (Claude 3.5 Sonnet)**. When Amazon CloudWatch detects anomalies or raises an alarm, a swarm of four specialized AI agents collaborate in an autonomous diagnostic loop: ingesting telemetry, isolating code diffs, verifying safety blast-radii, and generating verified pull requests in under 30 seconds.

---

## ⚡ The Problem It Solves

Cloud incident response is still overwhelmingly manual. When production alarms fire at 3 AM:

1. **SRE Context Switching:** Engineers spend 30 to 45 minutes manually correlating CloudWatch logs, APM traces, and recent GitHub commits.
2. **Mean Time to Detect (MTTD):** Cascading microservice failures often obscure the original root cause.
3. **High Remediation Risk:** Ad-hoc emergency hotfixes frequently introduce secondary bugs or broader blast radii.

CloudOps Swarm slashes simulated incident triage time from **45 minutes to 28 seconds** with **100% benchmark accuracy** at an operational cost of just **$0.01 per triage**.

---

## 🏗️ 4-Agent Autonomous Swarm Architecture

The swarm operates in an automated, closed-loop pipeline orchestrated by the Strands Agents SDK:

```text
[ CloudWatch Alarm / EventBridge Trigger ]
                   │
                   ▼
       [ AGENT 1: TRIAGE LEAD ]
       • Parses alarm severity (P1–P4) & blast radius
       • Dispatches parallel specialist tasks
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
[ AGENT 2: LOG DIAGNOSTIC ] [ AGENT 3: DIFF ANALYZER ]
• Queries CloudWatch logs   • Scans git commit diffs
• Detects stack trace OOM   • Traces unhandled configs
        │                     │
        └──────────┬──────────┘
                   ▼
     [ AGENT 4: REMEDIATION LEAD ]
     • Synthesizes verified safety plan
     • Verifies zero-downtime rollback constraints
     • Auto-generates GitHub PR & Post-Mortem
```

### Specialized Swarm Roles:

1. **Triage Lead Agent:** Ingests raw CloudWatch metrics and alarms, classifies incident severity (P1–P4), and defines the diagnostic perimeter.
2. **Log Diagnostic Agent:** Executes targeted log queries, traces unhandled stack traces, and isolates memory leaks (OOM) or deadlocks.
3. **Diff Analyzer Agent:** Inspects recent Git commit trees and Dockerfile/ENV modifications to correlate errors with deployed code changes.
4. **Remediation Synthesizer Agent:** Drafts targeted, safety-bounded code patches and verifies that rollback mechanisms exist before opening a Pull Request.

---

## 📊 Benchmarked Multi-Scenario Accuracy

We evaluated the swarm across 5 distinct real-world production incident archetypes using our automated evaluator (`run_benchmark.py`):

| Incident Archetype | Primary Cause | Autonomous Diagnosis | Remediation Plan | Result |
| :--- | :--- | :--- | :--- | :---: |
| **SCENARIO-01** | RDS Pool Exhaustion | Unreleased connection handles | Connection pool timeout & pooling fix | ✅ **PASS** |
| **SCENARIO-02** | OOM Container Crash | Memory leak in queue worker | Heap profile cap & garbage collection | ✅ **PASS** |
| **SCENARIO-03** | Malformed Config / ENV | Missing upstream service URL | Fallback configuration validation | ✅ **PASS** |
| **SCENARIO-04** | DNS Resolution Timeout | Route 53 VPC resolver latency | Retries with jitter & local caching | ✅ **PASS** |
| **SCENARIO-05** | Lambda Concurrency Spikes | Uncapped provisioned concurrency | SQS rate limiter & circuit breaker | ✅ **PASS** |

- **Benchmark Score:** **100.0% (5/5 passed)**
- **Average Diagnosis Time:** **28.4 seconds**
- **Average Triage Cost:** **~$0.01095 USD per incident**

---

## 🛠️ AWS Services & SDKs Utilized

- **Strands Agents SDK:** State-machine orchestration, dynamic role delegation, and tool gating.
- **Amazon Bedrock (Claude 3.5 Sonnet & Haiku):** Structured root-cause reasoning and code patch synthesis.
- **Amazon CloudWatch:** Alarm simulation, metric queries, and structured log group inspection.
- **Amazon S3 & GitHub Pages:** Incident post-mortem persistence, telemetry artifacts, and live HTTPS dashboard hosting.

---

## 💻 Live Interactive Demo & Repositories

- **Live Interactive Web Cockpit (HTTPS Secure):** [https://farhanmallik05.github.io/cloudops-incident-swarm/](https://farhanmallik05.github.io/cloudops-incident-swarm/)
- **Source Code Repository:** [https://github.com/farhanmallik05/cloudops-incident-swarm](https://github.com/farhanmallik05/cloudops-incident-swarm)

---

## 🧪 CLI Verification & Quickstart

Clone the repository and run the autonomous triage simulation locally:

```bash
# Clone repository
git clone https://github.com/farhanmallik05/cloudops-incident-swarm.git
cd cloudops-incident-swarm

# Install dependencies
pip install -r requirements.txt

# Run the autonomous incident triage demo
python cli_runner.py --demo

# Test with Chaos Fault Injection
python cli_runner.py --chaos connection_pool_leak

# Run the 5-scenario benchmark evaluator
python run_benchmark.py
```
