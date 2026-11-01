# 05 — AWS Bedrock & AgentCore Integration: Strands SDK

This guide details the technical configuration for connecting the **Strands Agents SDK** with **Amazon Bedrock**, configuring **AgentCore memory**, and deploying serverless agent runtimes.

---

## ☁️ 1. Configuring Amazon Bedrock for Strands SDK

Strands communicates with Amazon Bedrock via the official AWS Boto3 SDK or standard OpenAI-compatible endpoints with SigV4 signing.

### Step 1: Install Dependencies
```bash
pip install strands-agents boto3 botocore pydantic
```

### Step 2: Initialize the Bedrock Model Provider
```python
import boto3
from strands.models import BedrockModel

# Initialize Boto3 Bedrock Runtime Client
bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Initialize Strands Bedrock Model Harness
model = BedrockModel(
    client=bedrock_runtime,
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.1,  # Low temperature for precise analytical tool-use
    max_tokens=4096
)
```

---

## 💾 2. AgentCore & DynamoDB Session Persistence

For multi-agent swarms, maintaining state across steps and restarts is critical. Strands agents can be configured with persistent storage backends:

```python
from strands.memory import DynamoDBMemory

# Configure DynamoDB persistence
memory = DynamoDBMemory(
    table_name="StrandsAgentSessions",
    session_id="incident-uuid-2026-10-30-001",
    region_name="us-east-1"
)
```

### DynamoDB Table Schema:
- **Table Name:** `StrandsAgentSessions`
- **Partition Key:** `SessionId` (String)
- **Sort Key:** `MessageId` (Number or Timestamp)
- **Attributes:** `role` (user/assistant/tool), `content`, `tool_calls`, `created_at`

---

## 🛡️ 3. Applying Bedrock Guardrails

Protect your agent swarm from prompt injections, credential exposure, and harmful hallucinations by attaching an Amazon Bedrock Guardrail:

1. **In AWS Console -> Amazon Bedrock -> Guardrails -> Create Guardrail**:
   - **Name:** `CloudOpsSafetyGuardrail`
   - **PII Filters:** Mask AWS Access Keys, Secret Keys, database passwords, and personal emails.
   - **Topic Denials:** Block off-topic user queries unrelated to DevOps, cloud telemetry, or system debugging.
2. **Attach Guardrail to Strands Model Call:**
```python
model = BedrockModel(
    client=bedrock_runtime,
    model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
    guardrail_identifier="guardrail-id-xxx",
    guardrail_version="1"
)
```

---

## 🚀 4. Packaging Strands Agents for Serverless AWS Lambda

Strands agents can run directly inside AWS Lambda functions triggered by Amazon EventBridge or API Gateway:

```python
# lambda_function.py
import json
from strands import Agent
from strands.models import BedrockModel

def lambda_handler(event, context):
    model = BedrockModel(model_id="anthropic.claude-3-5-sonnet-20241022-v2:0")
    
    # Initialize agents & tools
    commander = Agent(
        model=model,
        tools=[...],
        system_prompt="You are an autonomous Cloud Incident Commander."
    )
    
    prompt = event.get("alarm_detail", "Analyze system health")
    response = commander.run(prompt)
    
    return {
        "statusCode": 200,
        "body": json.dumps({"incident_resolution": response})
    }
```

> **Lambda Configuration Recommendations:**
> - **Memory:** 1024 MB – 2048 MB (ensures fast execution of JSON parsing and SSL network calls).
> - **Timeout:** 300 seconds (5 minutes) to give the multi-agent loop ample room for multi-turn tool invocations.
> - **Architecture:** `arm64` (Graviton2/3, 20% lower cost, faster cold starts).

