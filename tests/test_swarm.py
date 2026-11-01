"""Unit and Integration Tests for CloudOps Multi-Agent Swarm."""
import unittest
from src.tools.cloudwatch import query_cloudwatch_insights, get_service_metrics
from src.tools.git_tools import get_recent_git_deployments, fetch_commit_diff
from src.tools.health_tools import get_aws_health_status
from src.tools.remediation import simulate_remediation_safety, execute_remediation
from src.harness.memory import InMemoryMemory
from src.harness.models import BedrockModel
from src.harness.agent import Agent
from src.swarm import CloudOpsSwarm

class TestCloudOpsSwarm(unittest.TestCase):

    def test_cloudwatch_insights_tool(self):
        result = query_cloudwatch_insights("checkout-service", lookback_minutes=15)
        self.assertEqual(result["status"], "success")
        self.assertIn("DBConnectionPoolTimeoutException", result["error_distribution"])
        self.assertGreater(result["total_error_events"], 0)

    def test_git_deployments_tool(self):
        result = get_recent_git_deployments("checkout-service", limit=2)
        self.assertEqual(result["service"], "checkout-service")
        self.assertGreaterEqual(len(result["deployments"]), 2)
        self.assertEqual(result["deployments"][0]["commit_hash"], "c8a41df")

    def test_remediation_safety_simulation(self):
        result = simulate_remediation_safety("ROLLBACK_DEPLOYMENT", {"target_commit": "b2f901a"})
        self.assertTrue(result["is_safe"])
        self.assertEqual(result["approval_required"], "HUMAN_SRE_APPROVAL")

    def test_remediation_execution_blocked_without_token(self):
        result = execute_remediation("ROLLBACK_DEPLOYMENT", {}, approval_token="INVALID")
        self.assertEqual(result["status"], "BLOCKED")

    def test_remediation_execution_success(self):
        result = execute_remediation("ROLLBACK_DEPLOYMENT", {"service": "checkout"}, approval_token="APPROVED")
        self.assertEqual(result["status"], "EXECUTED")

    def test_agent_loop_execution(self):
        model = BedrockModel()
        memory = InMemoryMemory()
        agent = Agent(
            model=model,
            tools=[query_cloudwatch_insights],
            system_prompt="Analyze logs",
            memory=memory
        )
        response = agent.run("Please check CloudWatch logs for checkout-service")
        self.assertTrue(len(response) > 0)
        self.assertGreaterEqual(len(memory.get_messages()), 3)

    def test_end_to_end_swarm_pipeline(self):
        swarm = CloudOpsSwarm(region_name="us-east-1")
        test_alarm = "CRITICAL: High error rates on checkout-service in us-east-1."
        result = swarm.handle_incident(test_alarm)

        self.assertIn("incident_id", result)
        self.assertIn("lifecycle_events", result)
        self.assertEqual(len(result["lifecycle_events"]), 4)
        self.assertTrue(len(result["final_post_mortem"]) > 0)

if __name__ == "__main__":
    unittest.main()

