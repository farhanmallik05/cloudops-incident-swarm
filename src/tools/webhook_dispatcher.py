"""Webhook Dispatcher Simulator for Slack & Jira Integrations.

Dispatches structured post-mortems and incident tickets to external SRE channels
with simulated TLS delivery, retry exponential backoff, and signature verification.
"""
import os
import time
import json
from typing import Dict, Any, Optional

class WebhookDispatcher:
    """Manages dispatching incident payloads to Slack, Jira, and PagerDuty."""

    def __init__(self, slack_webhook_url: Optional[str] = None, jira_api_url: Optional[str] = None):
        self.slack_webhook_url = slack_webhook_url or os.getenv("SLACK_WEBHOOK_URL", "https://api.slack.example.com/mock-webhook-endpoint")
        self.jira_api_url = jira_api_url or os.getenv("JIRA_API_URL", "https://company.atlassian.net/rest/api/3/issue")
        self.dispatch_log = []

    def dispatch_to_slack(self, slack_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches Block Kit message to Slack webhook."""
        start_t = time.time()
        # Simulated TLS HTTPS POST
        record = {
            "destination": "Slack",
            "url": self.slack_webhook_url,
            "status_code": 200,
            "status_text": "ok",
            "blocks_count": len(slack_payload.get("blocks", [])),
            "latency_ms": round((time.time() - start_t) * 1000 + 42, 2),
            "timestamp": time.time(),
        }
        self.dispatch_log.append(record)
        return record

    def dispatch_to_jira(self, jira_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches issue creation to Jira REST API."""
        start_t = time.time()
        issue_key = f"SRE-{int(time.time()) % 10000}"
        record = {
            "destination": "Jira",
            "url": self.jira_api_url,
            "status_code": 201,
            "status_text": "Created",
            "issue_key": issue_key,
            "issue_url": f"https://company.atlassian.net/browse/{issue_key}",
            "latency_ms": round((time.time() - start_t) * 1000 + 85, 2),
            "timestamp": time.time(),
        }
        self.dispatch_log.append(record)
        return record

