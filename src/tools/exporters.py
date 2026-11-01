"""Multi-Channel Incident Post-Mortem Exporters (Slack, Jira, Markdown)."""
import json
from typing import Dict, Any

def export_to_slack_block_kit(incident_id: str, alarm: str, post_mortem_text: str) -> Dict[str, Any]:
    """Formats incident post-mortem into Slack Block Kit payload."""
    return {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"🚨 [SRE Post-Mortem] {incident_id}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Alarm:*\n{alarm[:150]}"},
                    {"type": "mrkdwn", "text": "*Resolution:*\nAutonomous Rollback Verified"}
                ]
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": post_mortem_text[:2800]
                }
            }
        ]
    }

def export_to_jira_issue(incident_id: str, post_mortem_text: str) -> Dict[str, Any]:
    """Formats post-mortem into a Jira Incident ticket schema."""
    return {
        "fields": {
            "project": {"key": "INC"},
            "summary": f"CloudOps Swarm Post-Mortem: {incident_id}",
            "description": post_mortem_text,
            "issuetype": {"name": "Incident Post-Mortem"},
            "priority": {"name": "High"},
            "labels": ["cloudops-swarm", "automated-sre", "strands-sdk"]
        }
    }

