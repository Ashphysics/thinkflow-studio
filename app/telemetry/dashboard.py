"""
Telemetry dashboard API for the UI.
"""
from app.telemetry.metrics import metrics_aggregator

def get_dashboard_metrics():
    """Provides a unified view of system health."""
    return metrics_aggregator.get_metrics()
