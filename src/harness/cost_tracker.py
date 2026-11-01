"""Token Consumption & FinOps Cost Engine for Amazon Bedrock Models."""
from typing import Dict, Any

# Bedrock Pricing per 1,000 Tokens (USD)
PRICING_TABLE = {
    "anthropic.claude-3-5-sonnet-20241022-v2:0": {
        "input_per_1k": 0.003,
        "output_per_1k": 0.015,
    },
    "anthropic.claude-3-5-haiku-20241022-v1:0": {
        "input_per_1k": 0.00025,
        "output_per_1k": 0.00125,
    },
    "amazon.titan-text-express-v1": {
        "input_per_1k": 0.0002,
        "output_per_1k": 0.0006,
    },
}

class TokenCostTracker:
    """Calculates real-world Amazon Bedrock token spend across multi-agent swarms."""

    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost_usd = 0.0
        self.invocation_records = []

    def record_usage(self, model_id: str, input_tokens: int, output_tokens: int) -> float:
        pricing = PRICING_TABLE.get(model_id, PRICING_TABLE["anthropic.claude-3-5-haiku-20241022-v1:0"])
        cost = (input_tokens / 1000.0) * pricing["input_per_1k"] + (output_tokens / 1000.0) * pricing["output_per_1k"]

        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.total_cost_usd += cost

        record = {
            "model_id": model_id,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": round(cost, 6),
        }
        self.invocation_records.append(record)
        return cost

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_tokens": self.total_input_tokens + self.total_output_tokens,
            "total_cost_usd": round(self.total_cost_usd, 5),
            "total_invocations": len(self.invocation_records),
        }

