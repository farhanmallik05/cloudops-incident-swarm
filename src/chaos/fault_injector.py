"""Chaos Engineering Fault Injection Simulator for CloudOps Swarm."""
import time
from typing import Dict, Any

class ChaosFaultInjector:
    """Injects simulated infrastructure defects to test autonomous self-healing resilience."""

    SUPPORTED_FAULTS = [
        "DB_CONNECTION_POOL_EXHAUSTION",
        "DOWNSTREAM_504_TIMEOUT",
        "DEADLOCK_CASCADE",
        "MEMORY_SATURATION",
    ]

    ALIASES = {
        "connection_pool_leak": "DB_CONNECTION_POOL_EXHAUSTION",
        "leak": "DB_CONNECTION_POOL_EXHAUSTION",
        "db_connection_pool_exhaustion": "DB_CONNECTION_POOL_EXHAUSTION",
        "downstream_504_timeout": "DOWNSTREAM_504_TIMEOUT",
        "timeout": "DOWNSTREAM_504_TIMEOUT",
        "504_gateway_timeout": "DOWNSTREAM_504_TIMEOUT",
        "memory_saturation": "MEMORY_SATURATION",
        "oom": "MEMORY_SATURATION",
        "memory": "MEMORY_SATURATION",
        "deadlock_cascade": "DEADLOCK_CASCADE",
        "deadlock": "DEADLOCK_CASCADE",
    }

    @staticmethod
    def inject_fault(fault_type: str, target_service: str = "checkout-service") -> Dict[str, Any]:
        """Simulates the activation of a critical production anomaly."""
        normalized = fault_type.strip()
        if normalized in ChaosFaultInjector.ALIASES:
            canonical_fault = ChaosFaultInjector.ALIASES[normalized]
        elif normalized.upper() in ChaosFaultInjector.SUPPORTED_FAULTS:
            canonical_fault = normalized.upper()
        else:
            raise ValueError(f"Unknown fault: {fault_type}. Choose from {ChaosFaultInjector.SUPPORTED_FAULTS}")

        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        if canonical_fault == "DB_CONNECTION_POOL_EXHAUSTION":
            alarm_desc = f"CRITICAL: Service '{target_service}' connection pool saturation at 100%. Latency spike to 4500ms."
            return {
                "fault": canonical_fault,
                "target_service": target_service,
                "timestamp": timestamp,
                "alarm_name": "HighDBConnectionPoolWaitTime",
                "simulated_alarm": alarm_desc,
                "description": alarm_desc,
                "root_cause_seed": "Commit introduced unclosed database connection in transaction block."
            }
        elif canonical_fault == "DOWNSTREAM_504_TIMEOUT":
            alarm_desc = f"HIGH: Upstream gateway reported 18.2% 504 timeouts contacting '{target_service}'."
            return {
                "fault": canonical_fault,
                "target_service": target_service,
                "timestamp": timestamp,
                "alarm_name": "DownstreamGatewayTimeout504",
                "simulated_alarm": alarm_desc,
                "description": alarm_desc,
                "root_cause_seed": "Downstream payment gateway latency degraded from 80ms to 9200ms."
            }
        else:
            alarm_desc = f"CRITICAL: '{target_service}' container memory utilization exceeded 95%."
            return {
                "fault": canonical_fault,
                "target_service": target_service,
                "timestamp": timestamp,
                "alarm_name": "HighMemorySaturationAlert",
                "simulated_alarm": alarm_desc,
                "description": alarm_desc,
                "root_cause_seed": "Unbounded cache growth in application memory."
            }
