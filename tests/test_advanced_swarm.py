"""Comprehensive Test Suite for Advanced Swarm Features."""
import unittest
from src.harness.hitl import HITLApprovalGateway
from src.harness.cost_tracker import TokenCostTracker
from src.chaos.fault_injector import ChaosFaultInjector
from src.tools.exporters import export_to_slack_block_kit, export_to_jira_issue
from src.tools.webhook_dispatcher import WebhookDispatcher
from src.harness.kms_signer import AwsKmsEnvelopeSigner
from src.harness.benchmark_evaluator import SwarmBenchmarkEvaluator
from src.swarm import CloudOpsSwarm

class TestAdvancedSwarmFeatures(unittest.TestCase):

    def test_hitl_approval_gateway(self):
        gw = HITLApprovalGateway()
        req_id = gw.request_approval(
            action="ROLLBACK_DEPLOYMENT",
            parameters={"target_commit": "b2f901a"},
            risk_rating="LOW"
        )
        self.assertTrue(req_id.startswith("REQ-"))
        self.assertFalse(gw.verify_token(req_id, "random-token"))

        token = gw.approve(req_id, "LEAD_SRE")
        self.assertIsNotNone(token)
        self.assertTrue(gw.verify_token(req_id, token))

    def test_token_cost_tracker(self):
        tracker = TokenCostTracker()
        cost = tracker.record_usage(
            model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
            input_tokens=1000,
            output_tokens=1000
        )
        # Sonnet: $0.003 input / 1k + $0.015 output / 1k = $0.018
        self.assertAlmostEqual(cost, 0.018, places=4)

        summary = tracker.get_summary()
        self.assertEqual(summary["total_tokens"], 2000)
        self.assertAlmostEqual(summary["total_cost_usd"], 0.018, places=4)

    def test_chaos_fault_injector(self):
        fault = ChaosFaultInjector.inject_fault("DB_CONNECTION_POOL_EXHAUSTION", "checkout-service")
        self.assertEqual(fault["fault"], "DB_CONNECTION_POOL_EXHAUSTION")
        self.assertIn("saturation", fault["simulated_alarm"])

        with self.assertRaises(ValueError):
            ChaosFaultInjector.inject_fault("NON_EXISTENT_FAULT")

    def test_slack_and_jira_exporters(self):
        slack = export_to_slack_block_kit("INC-99", "504 Spike", "Root cause identified.")
        self.assertIn("blocks", slack)
        self.assertEqual(len(slack["blocks"]), 4)

        jira = export_to_jira_issue("INC-99", "Root cause identified.")
        self.assertIn("fields", jira)
        self.assertEqual(jira["fields"]["summary"], "CloudOps Swarm Post-Mortem: INC-99")

    def test_kms_envelope_signer(self):
        signer = AwsKmsEnvelopeSigner()
        payload = {"incident_id": "INC-TEST-1", "action": "ROLLBACK_TASK_V41"}
        signed = signer.sign_payload(payload)
        self.assertIn("signature_hex", signed)
        self.assertEqual(signed["status"], "VALID")

        is_valid = signer.verify_signature(payload, signed["signature_hex"])
        self.assertTrue(is_valid)

        tampered_payload = {"incident_id": "INC-TEST-1", "action": "DELETE_ALL_DATABASES"}
        self.assertFalse(signer.verify_signature(tampered_payload, signed["signature_hex"]))

    def test_benchmark_evaluator(self):
        evaluator = SwarmBenchmarkEvaluator()
        summary = evaluator.run_all()
        self.assertEqual(summary["total_scenarios"], 5)
        self.assertEqual(summary["accuracy_score_pct"], 100.0)
        self.assertGreater(summary["total_finops_cost_usd"], 0.0)

    def test_webhook_dispatcher(self):
        dispatcher = WebhookDispatcher()
        slack_res = dispatcher.dispatch_to_slack({"blocks": [{"type": "section"}]})
        self.assertEqual(slack_res["status_code"], 200)
        self.assertEqual(slack_res["destination"], "Slack")

        jira_res = dispatcher.dispatch_to_jira({"fields": {"summary": "Incident"}})
        self.assertEqual(jira_res["status_code"], 201)
        self.assertTrue(jira_res["issue_key"].startswith("SRE-"))

if __name__ == "__main__":
    unittest.main()

