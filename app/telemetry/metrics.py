"""
Metrics aggregator for Observability.
"""
from typing import Dict, List
import time

class MetricsAggregator:
    def __init__(self):
        self.agent_latencies: Dict[str, List[float]] = {}
        self.pipeline_executions = 0
        self.pipeline_successes = 0
        self.pipeline_failures = 0

    def record_agent_latency(self, agent_name: str, duration: float):
        if agent_name not in self.agent_latencies:
            self.agent_latencies[agent_name] = []
        self.agent_latencies[agent_name].append(duration)

    def record_pipeline_result(self, success: bool):
        self.pipeline_executions += 1
        if success:
            self.pipeline_successes += 1
        else:
            self.pipeline_failures += 1

    def get_metrics(self) -> Dict[str, float]:
        metrics = {
            "total_executions": self.pipeline_executions,
            "success_rate": (self.pipeline_successes / self.pipeline_executions) * 100 if self.pipeline_executions else 0.0,
        }
        for agent, latencies in self.agent_latencies.items():
            if latencies:
                metrics[f"avg_latency_{agent}"] = sum(latencies) / len(latencies)
        return metrics

# Singleton
metrics_aggregator = MetricsAggregator()
