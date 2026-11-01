## 🚀 Project Overview

**CloudOps Swarm** is an autonomous, multi-agent incident triaging and self-healing system built with the **Strands Agents SDK** and **Amazon Bedrock (Anthropic Claude 3.5 Sonnet & Haiku)**. 

When high-severity production outages occur at 3 AM, human Site Reliability Engineers (SREs) typically spend 45+ minutes under immense pressure manually sifting through CloudWatch logs, tracing git commits, and formulating rollbacks. CloudOps Swarm replaces this manual grind with an autonomous swarm of four specialized AI agents that investigate, correlate, simulate safety blast-radii, and generate verified pull requests in **under 30 seconds**—slashing simulated Mean Time to Detect (MTTD) from 45 minutes to 28 seconds with **100% benchmark accuracy** at an operational cost of just **$0.01 per triage**.

---

## 🏗️ 4-Agent Autonomous Swarm Architecture

Instead of a monolithic prompt or brittle linear chain, CloudOps Swarm utilizes a supervisor-specialist multi-agent topology orchestrated via the Strands Agents SDK:

### Agent Responsibilities & Capabilities

| Agent | Core Role | Specialized Capability | Tools & Integrations |
| :--- | :--- | :--- | :--- |
| **Agent 1: Triage Lead** | Supervisor & Orchestrator | Deconstructs incoming CloudWatch alarms, assesses blast-radius severity, and delegates diagnostic tasks. | `CloudWatch Alarm Ingestion`, `Task Dispatcher` |
| **Agent 2: Log Diagnostic** | Telemetry Analyst | Analyzes high-velocity CloudWatch logs, detects error spikes, and extracts stack-trace signatures. | `CloudWatch Insights Query`, `Pattern Matcher` |
| **Agent 3: Diff Analyzer** | Root-Cause Correlator | Scans git commit diffs, inspects code changes, and isolates unhandled exceptions or config leaks. | `Git Commit Diff Scanner`, `Deployment Correlator` |
| **Agent 4: Remediation Lead** | Safety & Synthesis Lead | Synthesizes root-cause findings, verifies safety constraints, and generates zero-downtime fix PRs. | `Blast-Radius Verifier`, `GitHub PR Generator` |

### Multi-Agent Autonomous Workflow Pipeline

1. **Trigger (CloudWatch / EventBridge):** High-severity operational alarm is ingested (e.g. 5XX error rate surge).
2. **Phase 1 — Agent 1 (Triage Lead):** Assesses alarm severity, computes preliminary blast radius, and dispatches parallel diagnostic tasks.
3. **Phase 2 — Parallel Deep Analysis (Agents 2 & 3):**
   - **Agent 2 (Log Diagnostic):** Queries CloudWatch Logs Insights, isolates error spikes, and extracts stack-trace signatures.
   - **Agent 3 (Diff Analyzer):** Cross-references recent Git commit diffs and AWS Health events to isolate code and config culpability.
4. **Phase 3 — Agent 4 (Remediation Lead):** Synthesizes root-cause findings, validates zero-downtime safety constraints, and generates an automated GitHub Pull Request with rollback plan.
5. **Phase 4 — SRE Verification Gate:** Presents executive post-mortem to Site Reliability Engineers with KMS-signed execution token.

---

## 📊 Benchmark Results & Performance

We built an automated benchmark evaluation suite (`run_benchmark.py`) to stress-test CloudOps Swarm against 5 real-world cloud incident archetypes:

- **Scenario 1:** Database Connection Pool Starvation (RDS handle exhaustion) — **PASSED**
- **Scenario 2:** Out-Of-Memory (OOM) Memory Leak in Worker Container (ECS/EKS) — **PASSED**
- **Scenario 3:** Malformed Environment Variable Configuration (Lambda / App Runner) — **PASSED**
- **Scenario 4:** Upstream DNS Resolution Timeout (Route 53 / VPC endpoint) — **PASSED**
- **Scenario 5:** Provisioned Concurrency Saturation & Cold Start Cascades — **PASSED**

### Benchmark Summary
- **Accuracy Score:** **100.0%** (5/5 incidents accurately diagnosed and remediated)
- **Average Triage Time:** **28.4 seconds** (compared to 45 minutes industry baseline)
- **Mean Cost per Triage:** **$0.0109 USD**
- **Safety Record:** **Zero hallucinated rollbacks** via human-in-the-loop verification gates

---

## 🛠️ AWS Services & Architecture Highlights

- **Strands Agents SDK:** Powers agent lifecycle, autonomous state transitions, tool dispatching, and agent-to-agent delegation.
- **Amazon Bedrock:** Foundation model intelligence utilizing Anthropic Claude 3.5 Sonnet for deep diagnostic reasoning and Claude 3.5 Haiku for ultra-fast log parsing.
- **Amazon CloudWatch & EventBridge:** Real-time alarm ingestion, metric telemetry tracking, and structured log stream queries.
- **AWS Lambda & S3:** Event-driven serverless trigger execution and high-performance interactive dashboard hosting.
- **Amazon Bedrock Guardrails:** Sanitizes operational telemetry to prevent credential or secret leakage during multi-agent context exchanges.

---

## 💻 Live Interactive Demo & Repositories

- **Live Interactive Web Dashboard (HTTPS Secure):** [https://farhanmallik05.github.io/cloudops-incident-swarm/](https://farhanmallik05.github.io/cloudops-incident-swarm/)
- **Source Code Repository:** [GitHub - farhanmallik05/cloudops-incident-swarm](https://github.com/farhanmallik05/cloudops-incident-swarm)

### Running the Demo Locally

```bash
# Clone the repository
git clone https://github.com/farhanmallik05/cloudops-incident-swarm.git
cd cloudops-incident-swarm

# Install dependencies
pip install -r requirements.txt

# Run the autonomous incident triage demo
python cli_runner.py --demo

# Run chaos fault injection testing
python cli_runner.py --chaos connection_pool_leak

# Execute automated multi-scenario benchmark suite
python run_benchmark.py
```
