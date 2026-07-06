"""
Tracer hooking into EventDispatcher to measure latency.
"""
from typing import Dict
import time
from app.orchestrator.events import dispatcher, WorkflowEvent
from app.telemetry.metrics import metrics_aggregator
from app.telemetry.logger import logger

class ExecutionTracer:
    def __init__(self):
        self.active_spans: Dict[str, float] = {}
        dispatcher.subscribe(self.handle_event)

    def handle_event(self, event: WorkflowEvent):
        span_id = f"{event.session_id}_{event.agent_name}"
        
        if event.event_type in ("agent_started", "pipeline_started"):
            self.active_spans[span_id] = time.time()
            
        elif event.event_type in ("agent_completed", "agent_failed", "pipeline_completed"):
            start_time = self.active_spans.pop(span_id, None)
            if start_time:
                duration = time.time() - start_time
                if event.agent_name != "pipeline":
                    metrics_aggregator.record_agent_latency(event.agent_name, duration)
                    
            if event.event_type == "pipeline_completed":
                metrics_aggregator.record_pipeline_result(success=True)
            elif event.event_type == "agent_failed":
                # Assuming agent_failed means pipeline failed since we abort
                metrics_aggregator.record_pipeline_result(success=False)

# Initialize tracer
tracer = ExecutionTracer()
