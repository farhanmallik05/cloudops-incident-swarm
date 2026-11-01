"""Amazon CloudWatch Telemetry and Log Diagnostics Tool."""
from typing import Dict, Any

def query_cloudwatch_insights(service_name: str, lookback_minutes: int = 15) -> Dict[str, Any]:
    """Queries Amazon CloudWatch Logs for 5XX errors, exceptions, and stack traces.

    Args:
        service_name: Name of the microservice or Lambda function (e.g. 'checkout-service').
        lookback_minutes: Lookback timeframe in minutes for the log query (default: 15).
    """
    return {
        "status": "success",
        "service": service_name,
        "timeframe_minutes": lookback_minutes,
        "total_error_events": 842,
        "error_distribution": {
            "DBConnectionPoolTimeoutException": 794,
            "HTTP504GatewayTimeout": 48
        },
        "first_occurrence": "2026-10-30T17:14:02Z",
        "peak_error_rate_eps": 142.5,
        "stack_trace": [
            "File '/var/task/app/database.py', line 88, in acquire_connection",
            "File '/var/task/app/routes/checkout.py', line 42, in process_order",
            "DBConnectionPoolTimeoutException: Maximum pool size (20) exceeded waiting for available connection."
        ],
        "top_failing_endpoint": "POST /api/v2/checkout/finalize",
    }

def get_service_metrics(service_name: str, metric_name: str = "Errors") -> Dict[str, Any]:
    """Retrieves operational time-series metrics from CloudWatch.

    Args:
        service_name: Name of the target AWS resource or service.
        metric_name: Target metric name ('Errors', 'Duration', 'Throttles', 'CPUUtilization').
    """
    return {
        "service": service_name,
        "metric": metric_name,
        "current_value": 14.8 if metric_name == "Errors" else 92.4,
        "unit": "Percent" if metric_name == "Errors" else "Milliseconds",
        "alarm_threshold": 5.0,
        "is_alarm_state": True,
        "historical_baseline": 0.2
    }

