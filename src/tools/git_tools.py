"""Git and CI/CD Deployment Telemetry Tools."""
from typing import Dict, Any, List

def get_recent_git_deployments(service_name: str, limit: int = 3) -> Dict[str, Any]:
    """Retrieves recent CI/CD deployments and Git commit metadata for a service.

    Args:
        service_name: Name of the microservice.
        limit: Number of recent deployments to fetch.
    """
    return {
        "service": service_name,
        "deployments": [
            {
                "commit_hash": "c8a41df",
                "author": "dev-alex@company.com",
                "deployed_at": "2026-10-30T17:05:00Z",  # 9 minutes before error emergence!
                "message": "feat(checkout): add synchronous user loyalty tier lookup in order finalize loop",
                "files_changed": [
                    "app/routes/checkout.py",
                    "app/services/loyalty.py",
                    "app/database.py"
                ],
                "diff_summary": "Added unindexed DB query in loop without closing cursor connection in exception block."
            },
            {
                "commit_hash": "b2f901a",
                "author": "sre-sarah@company.com",
                "deployed_at": "2026-10-29T11:20:00Z",
                "message": "chore(deps): bump alpine base image and node dependencies"
            }
        ]
    }

def fetch_commit_diff(commit_hash: str) -> Dict[str, Any]:
    """Retrieves the unified git diff for a specific commit hash.

    Args:
        commit_hash: The 7-character or 40-character git commit hash.
    """
    return {
        "commit_hash": commit_hash,
        "diff": """
--- a/app/routes/checkout.py
+++ b/app/routes/checkout.py
@@ -39,6 +39,8 @@ def process_order(payload):
+    conn = db_pool.get_connection()
+    tier = conn.execute("SELECT tier FROM loyalty_rewards WHERE user_id = %s", (payload['user_id'],)).fetchone()
+    # BUG: Connection is never closed or returned to the pool!
"""
    }

