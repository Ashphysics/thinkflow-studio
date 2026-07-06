"""
The Orchestration Pipeline.
Executes the deterministic workflow sequence and manages state.
"""

import time
import uuid
from loguru import logger

from app.orchestrator.context import WorkflowContext
from app.orchestrator.events import dispatcher, WorkflowEvent
from app.orchestrator.workflow import get_ideation_workflow
from app.agents.agent_registry import agent_registry
from app.config.providers import ProviderFactory
from app.core.exceptions import AgentExecutionError
from app.memory.memory_service import memory_service
from app.security.scanner import SecurityScanner

class AgentPipeline:
    """
    Executes a predefined sequence of agents, passing the accumulated state.
    """
    def __init__(self, session_id: str = None):
        self.session_id = session_id or str(uuid.uuid4())
        self.config = ProviderFactory.create_google_config("gemini-2.5-flash")

    async def run(self, prompt: str) -> WorkflowContext:
        """
        Runs the full deterministic ideation pipeline.
        """
        request_id = str(uuid.uuid4())
        
        is_safe, sec_error = SecurityScanner.scan_input(prompt)
        if not is_safe:
            context = WorkflowContext(
                session_id=self.session_id, request_id=request_id, user_prompt=prompt,
                start_time=time.time(), end_time=time.time(), status="failed", error_message=sec_error
            )
            memory_service.save_session(context)
            return context

        context = WorkflowContext(
            session_id=self.session_id,
            request_id=request_id,
            user_prompt=prompt,
            start_time=time.time(),
            status="running"
        )
        
        workflow_steps = get_ideation_workflow()
        
        dispatcher.dispatch(WorkflowEvent(
            event_type="pipeline_started",
            session_id=self.session_id,
            agent_name="pipeline",
            details={"steps": workflow_steps, "prompt": prompt}
        ))
        
        for agent_name in workflow_steps:
            dispatcher.dispatch(WorkflowEvent(
                event_type="agent_started",
                session_id=self.session_id,
                agent_name=agent_name,
                details={}
            ))
            
            try:
                # 1. Resolve Agent
                agent_class = agent_registry.get_agent(agent_name)
                agent_instance = agent_class(config=self.config)
                
                # 2. Execute Agent with accumulated context
                # The BaseAgent run() handles retries and logging internally.
                result = await agent_instance.run(prompt=prompt, context=context.to_dict())
                
                # 3. Update State based on which agent just ran
                if agent_name == "analyzer":
                    context.idea_analysis = result
                elif agent_name == "critic":
                    context.critic_analysis = result
                elif agent_name == "framework_selector":
                    context.framework_selection = result
                elif agent_name == "planner":
                    context.execution_plan = result
                    
                context.execution_logs.append({
                    "agent": agent_name,
                    "status": "success",
                    "timestamp": time.time()
                })
                
                dispatcher.dispatch(WorkflowEvent(
                    event_type="agent_completed",
                    session_id=self.session_id,
                    agent_name=agent_name,
                    details={"status": "success"}
                ))
                
                # Save state after each successful step
                memory_service.save_session(context)
                
            except Exception as e:
                # Catastrophic failure halts the pipeline
                logger.error(f"[Pipeline] Halting due to failure in {agent_name}: {e}")
                context.status = "failed"
                context.error_message = str(e)
                context.end_time = time.time()
                
                context.execution_logs.append({
                    "agent": agent_name,
                    "status": "failed",
                    "error": str(e),
                    "timestamp": time.time()
                })
                
                dispatcher.dispatch(WorkflowEvent(
                    event_type="agent_failed",
                    session_id=self.session_id,
                    agent_name=agent_name,
                    details={"error": str(e)}
                ))
                
                memory_service.save_session(context)
                return context

        # Workflow fully succeeded
        context.status = "completed"
        context.end_time = time.time()
        
        dispatcher.dispatch(WorkflowEvent(
            event_type="pipeline_completed",
            session_id=self.session_id,
            agent_name="pipeline",
            details={"duration": context.end_time - context.start_time}
        ))
        
        memory_service.save_session(context)
        return context
