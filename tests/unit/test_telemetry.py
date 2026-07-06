"""
Tests for telemetry components.
"""
from app.telemetry.metrics import MetricsAggregator
from app.telemetry.logger import SecureLogger

def test_metrics_aggregation():
    metrics = MetricsAggregator()
    metrics.record_agent_latency("analyzer", 1.5)
    metrics.record_agent_latency("analyzer", 2.5)
    metrics.record_pipeline_result(True)
    metrics.record_pipeline_result(False)
    
    data = metrics.get_metrics()
    assert data["total_executions"] == 2
    assert data["success_rate"] == 50.0
    assert data["avg_latency_analyzer"] == 2.0

def test_secure_logger_redaction():
    msg = "Connecting with API_KEY='sk-12345abcd'"
    sanitized = SecureLogger.sanitize(msg)
    assert "sk-12345abcd" not in sanitized
    assert "REDACTED" in sanitized
