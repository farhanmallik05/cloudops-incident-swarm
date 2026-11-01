# 07 — Submission & Demo Guide: Strands SDK: Workshop to Ship

This guide provides the presentation script, project description copy, and pre-submission checklist for the **Strands SDK: Workshop to Ship** challenge.

---

## 🎬 3-Minute Video Demo Script

Judges want to see autonomous intelligence: agents making decisions, invoking tools, and collaborating in a swarm to solve a tough engineering problem.

```
⏱️ 0:00 - 0:35 | The Problem & The Mission
"Welcome builders! Cloud reliability is the backbone of the digital economy, yet when high-severity production incidents strike, human SREs spend hours in high-stress triage, manually parsing logs and tracing dependencies. 
Today, we took the lessons from the official AWS workshop—'Building AI Agents with Strands SDK: From Simple Loops to Multi-Agent Swarms'—and shipped CloudOps Swarm: an autonomous, multi-agent incident triaging and self-healing system powered by Strands SDK and Amazon Bedrock."

⏱️ 0:35 - 1:45 | Live Swarm Execution (The Autonomous Investigation)
"Let's simulate a live production outage: a sudden 5XX surge on our checkout service.
Watch the multi-agent choreography in action:
1. The Incident Commander Agent activates and immediately delegates the log anomaly search to our Triage Specialist.
2. The Triage Agent invokes our CloudWatch Insights tool, analyzes 10,000 log events in seconds, and discovers a connection pool exhaustion exception.
3. The Commander passes this context to our Deep Diagnostic Agent, powered by Claude 3.5 Sonnet on Amazon Bedrock. The Diagnostic Agent correlates the spike with recent git commits and identifies that a commit from 20 minutes ago introduced an unindexed query.
4. Finally, our Remediation Agent calculates a safe capacity adjustment and drafts an index migration script, equipped with a one-click rollback plan."

⏱️ 1:45 - 2:30 | Technical Architecture & Strands SDK Native Patterns
"What makes this system production-grade:
- Code-First Strands SDK Harness: Zero rigid graph frameworks. Our agents rely on Bedrock's native planning and tool calling.
- Model Selection: We pair Claude 3.5 Haiku for high-speed log parsing with Claude 3.5 Sonnet for deep architectural reasoning.
- Bedrock Guardrails: All tool outputs are automatically sanitized to prevent credential leakage or prompt injection attacks.
- Persistence: Session memory is managed through DynamoDB, allowing multi-turn investigations to resume seamlessly."

⏱️ 2:30 - 3:00 | Conclusion & Impact
"CloudOps Swarm reduces Mean Time to Detection (MTTD) from 45 minutes to under 30 seconds. 
Our open-source repository, full architecture documentation, and setup instructions are live on GitHub. 
Thank you to the AWS team for building the Strands SDK!"
```

---

## 📝 AWS Builder Center Submission Form Copy

### Project Title
`CloudOps Swarm — Autonomous AWS Incident Triaging & Self-Healing Multi-Agent System`

### Short Description (Max 150 characters)
`Autonomous SRE multi-agent swarm built on Strands SDK and Amazon Bedrock that triages, diagnoses, and remediates AWS cloud incidents in under 60 seconds.`

### Long Description
```markdown
### Summary
CloudOps Swarm is an autonomous multi-agent incident triage and self-healing system built with the open-source **Strands Agents SDK** and **Amazon Bedrock**. It takes developers from the concepts of the "Building AI Agents with Strands SDK" workshop to a full production cloud-native deployment.

### Multi-Agent Swarm Architecture
- **Incident Commander (Supervisor):** Deconstructs alarms into structured investigative subtasks and coordinates specialist agents.
- **Triage Specialist Agent:** Parses CloudWatch Logs Insights and extracts error signatures using Claude 3.5 Haiku.
- **Deep Diagnostic Agent:** Correlates AWS Health metrics and Git deployment diffs using Claude 3.5 Sonnet to establish root cause.
- **Remediation Specialist Agent:** Validates configuration changes and drafts zero-downtime rollback scripts.

### AWS Services & Security
- **Amazon Bedrock:** Claude 3.5 Sonnet & Haiku foundation models.
- **Amazon Bedrock Guardrails:** Automatic masking of sensitive AWS credentials and PII.
- **Amazon DynamoDB:** Persistent agent session state and memory.
- **Amazon CloudWatch & EventBridge:** Real-time event ingestion and operational telemetry.
```

### URLs
- **GitHub Repository URL:** `https://github.com/<your-username>/cloudops-strands-swarm`
- **Video Walkthrough URL:** `https://youtu.be/...`
- **Live Demo / API Gateway URL:** `https://<api-id>.execute-api.us-east-1.amazonaws.com`

---

## 📋 Pre-Submission Checklist

- [ ] Does the agent loop run without crashing or unhandled exceptions?
- [ ] Are tools properly documented with type hints and docstrings?
- [ ] Is Amazon Bedrock (Claude 3.5 Sonnet or Haiku) actively generating the agent reasoning?
- [ ] Are sensitive AWS API keys and credentials excluded from code and `.env` files?
- [ ] Is the GitHub repository public with an open-source license and comprehensive `README.md`?
- [ ] Is the video under 3 minutes, clearly displaying the multi-agent reasoning trace and live output?

