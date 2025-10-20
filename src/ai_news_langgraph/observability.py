"""Phoenix Observability for AI News LangGraph.

This module provides comprehensive observability for the AI newsletter generation
system using Arize Phoenix for tracing, monitoring, and debugging LLM applications.
"""

import os
import logging
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from contextlib import contextmanager
import threading
import atexit

# Phoenix imports
import phoenix as px
from phoenix.trace import SpanContext
from phoenix.trace.langchain import LangChainInstrumentor
from phoenix.trace.openai import OpenAIInstrumentor

# OpenTelemetry imports
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

# OpenInference semantic conventions
from openinference.semconv.trace import SpanAttributes

logger = logging.getLogger(__name__)


class PhoenixObserver:
    """Phoenix observability manager for AI News workflow."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """Singleton pattern for Phoenix observer."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize Phoenix observer."""
        if not hasattr(self, 'initialized'):
            self.initialized = False
            self.session = None
            self.tracer = None
            self.instrumentor = None
            self.openai_instrumentor = None
            self.spans = {}
            self.metrics = {
                'total_requests': 0,
                'successful_completions': 0,
                'failed_requests': 0,
                'total_tokens': 0,
                'total_cost': 0.0,
                'agent_metrics': {}
            }

    def initialize(
        self,
        project_name: str = "AI-News-LangGraph",
        phoenix_port: int = 6006,
        enable_remote: bool = False,
        remote_endpoint: Optional[str] = None
    ) -> None:
        """Initialize Phoenix observability.

        Args:
            project_name: Name for the Phoenix project
            phoenix_port: Local Phoenix UI port
            enable_remote: Enable remote tracing
            remote_endpoint: Remote OTLP endpoint
        """
        if self.initialized:
            logger.info("Phoenix already initialized")
            return

        try:
            # Launch Phoenix locally
            logger.info(f"🚀 Launching Phoenix on port {phoenix_port}...")
            self.session = px.launch_app(port=phoenix_port)
            logger.info(f"✅ Phoenix UI available at: http://localhost:{phoenix_port}")

            # Setup OpenTelemetry
            resource = Resource.create({
                "service.name": project_name,
                "service.version": "1.0.0",
                "deployment.environment": os.getenv("ENVIRONMENT", "development")
            })

            # Create tracer provider
            provider = TracerProvider(resource=resource)

            # Add exporters
            if enable_remote and remote_endpoint:
                # Remote OTLP exporter for production
                otlp_exporter = OTLPSpanExporter(
                    endpoint=remote_endpoint,
                    insecure=True
                )
                provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
                logger.info(f"📡 Remote tracing enabled: {remote_endpoint}")

            # Set global tracer provider
            trace.set_tracer_provider(provider)
            self.tracer = trace.get_tracer(__name__)

            # Instrument LangChain
            self.instrumentor = LangChainInstrumentor()
            self.instrumentor.instrument()
            logger.info("✅ LangChain instrumentation enabled")

            # Instrument OpenAI
            self.openai_instrumentor = OpenAIInstrumentor()
            self.openai_instrumentor.instrument()
            logger.info("✅ OpenAI instrumentation enabled")

            # Register cleanup
            atexit.register(self.cleanup)

            self.initialized = True
            logger.info("🎯 Phoenix observability fully initialized")

        except Exception as e:
            logger.error(f"Failed to initialize Phoenix: {e}")
            raise

    @contextmanager
    def trace_agent(self, agent_name: str, task: str, **attributes):
        """Context manager for tracing agent execution.

        Args:
            agent_name: Name of the agent
            task: Task being performed
            **attributes: Additional span attributes
        """
        if not self.tracer:
            yield None
            return

        # Create span
        with self.tracer.start_as_current_span(
            name=f"{agent_name}.{task}",
            kind=trace.SpanKind.INTERNAL
        ) as span:
            # Set standard attributes
            span.set_attribute("agent.name", agent_name)
            span.set_attribute("agent.task", task)
            span.set_attribute("timestamp", datetime.now().isoformat())

            # Set custom attributes
            for key, value in attributes.items():
                if value is not None:
                    span.set_attribute(f"custom.{key}", str(value))

            # Track in metrics
            self.metrics['total_requests'] += 1
            if agent_name not in self.metrics['agent_metrics']:
                self.metrics['agent_metrics'][agent_name] = {
                    'calls': 0,
                    'successes': 0,
                    'failures': 0,
                    'total_duration_ms': 0
                }

            agent_metrics = self.metrics['agent_metrics'][agent_name]
            agent_metrics['calls'] += 1

            start_time = datetime.now()

            try:
                yield span
                # Success
                span.set_status(Status(StatusCode.OK))
                self.metrics['successful_completions'] += 1
                agent_metrics['successes'] += 1

            except Exception as e:
                # Failure
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                self.metrics['failed_requests'] += 1
                agent_metrics['failures'] += 1
                raise

            finally:
                # Record duration
                duration = (datetime.now() - start_time).total_seconds() * 1000
                span.set_attribute("duration_ms", duration)
                agent_metrics['total_duration_ms'] += duration

    def trace_llm_call(
        self,
        model: str,
        prompt: str,
        response: str,
        tokens_used: Optional[int] = None,
        cost: Optional[float] = None,
        **kwargs
    ):
        """Trace LLM API calls.

        Args:
            model: Model name
            prompt: Input prompt
            response: Model response
            tokens_used: Total tokens used
            cost: Cost of the call
            **kwargs: Additional metadata
        """
        if not self.tracer:
            return

        with self.tracer.start_as_current_span(
            name=f"llm.{model}",
            kind=trace.SpanKind.CLIENT
        ) as span:
            # Set OpenInference semantic conventions
            span.set_attribute(SpanAttributes.LLM_MODEL_NAME, model)
            span.set_attribute(SpanAttributes.LLM_PROMPTS, json.dumps([prompt]))
            span.set_attribute(SpanAttributes.LLM_RESPONSES, json.dumps([response]))

            if tokens_used:
                span.set_attribute(SpanAttributes.LLM_TOKEN_COUNT_TOTAL, tokens_used)
                self.metrics['total_tokens'] += tokens_used

            if cost:
                span.set_attribute("llm.cost", cost)
                self.metrics['total_cost'] += cost

            # Add custom attributes
            for key, value in kwargs.items():
                if value is not None:
                    span.set_attribute(f"custom.{key}", str(value))

    def trace_tool_use(self, tool_name: str, input_data: Any, output_data: Any):
        """Trace tool usage.

        Args:
            tool_name: Name of the tool
            input_data: Tool input
            output_data: Tool output
        """
        if not self.tracer:
            return

        with self.tracer.start_as_current_span(
            name=f"tool.{tool_name}",
            kind=trace.SpanKind.INTERNAL
        ) as span:
            span.set_attribute("tool.name", tool_name)
            span.set_attribute("tool.input", json.dumps(input_data, default=str)[:1000])
            span.set_attribute("tool.output", json.dumps(output_data, default=str)[:1000])

    def log_workflow_metrics(self, workflow_state: Dict[str, Any]):
        """Log workflow-level metrics.

        Args:
            workflow_state: Current workflow state
        """
        if not self.tracer:
            return

        with self.tracer.start_as_current_span(
            name="workflow.metrics",
            kind=trace.SpanKind.INTERNAL
        ) as span:
            # Extract metrics from state
            topics = workflow_state.get("topics", [])
            articles = workflow_state.get("fetched_articles", {})
            summaries = workflow_state.get("topic_summaries", [])

            # Set metrics
            span.set_attribute("workflow.topics_count", len(topics))
            span.set_attribute("workflow.total_articles",
                              sum(len(arts) for arts in articles.values()))
            span.set_attribute("workflow.summaries_count", len(summaries))

            # Quality scores
            if summaries:
                quality_scores = [s.get("quality_score", 0) for s in summaries]
                avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
                span.set_attribute("workflow.avg_quality_score", avg_quality)

            # Timing
            if workflow_state.get("workflow_start_time"):
                start = datetime.fromisoformat(workflow_state["workflow_start_time"])
                duration = (datetime.now() - start).total_seconds()
                span.set_attribute("workflow.duration_seconds", duration)

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get summary of collected metrics.

        Returns:
            Dictionary of metrics
        """
        summary = {
            "total_requests": self.metrics['total_requests'],
            "successful_completions": self.metrics['successful_completions'],
            "failed_requests": self.metrics['failed_requests'],
            "success_rate": (
                self.metrics['successful_completions'] / self.metrics['total_requests'] * 100
                if self.metrics['total_requests'] > 0 else 0
            ),
            "total_tokens": self.metrics['total_tokens'],
            "total_cost": round(self.metrics['total_cost'], 4),
            "agent_performance": {}
        }

        # Agent-specific metrics
        for agent, metrics in self.metrics['agent_metrics'].items():
            if metrics['calls'] > 0:
                summary['agent_performance'][agent] = {
                    'calls': metrics['calls'],
                    'success_rate': metrics['successes'] / metrics['calls'] * 100,
                    'avg_duration_ms': metrics['total_duration_ms'] / metrics['calls']
                }

        return summary

    def export_traces(self, output_file: str = "traces.json"):
        """Export collected traces to file.

        Args:
            output_file: Path to output file
        """
        try:
            traces = {
                "exported_at": datetime.now().isoformat(),
                "metrics": self.get_metrics_summary(),
                "spans": self.spans
            }

            with open(output_file, 'w') as f:
                json.dump(traces, f, indent=2, default=str)

            logger.info(f"✅ Traces exported to {output_file}")

        except Exception as e:
            logger.error(f"Failed to export traces: {e}")

    def cleanup(self):
        """Cleanup Phoenix resources."""
        if self.instrumentor:
            self.instrumentor.uninstrument()
        if self.openai_instrumentor:
            self.openai_instrumentor.uninstrument()
        if self.session:
            self.session.stop()
        logger.info("🧹 Phoenix observability cleaned up")


# Singleton instance
phoenix_observer = PhoenixObserver()


# Decorator for automatic tracing
def trace_node(agent_name: str):
    """Decorator for tracing LangGraph nodes.

    Args:
        agent_name: Name of the agent/node
    """
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            state = args[0] if args else kwargs.get('state', {})
            task = func.__name__

            with phoenix_observer.trace_agent(
                agent_name=agent_name,
                task=task,
                state_keys=list(state.keys()) if isinstance(state, dict) else []
            ):
                result = await func(*args, **kwargs)
                return result

        def sync_wrapper(*args, **kwargs):
            state = args[0] if args else kwargs.get('state', {})
            task = func.__name__

            with phoenix_observer.trace_agent(
                agent_name=agent_name,
                task=task,
                state_keys=list(state.keys()) if isinstance(state, dict) else []
            ):
                result = func(*args, **kwargs)
                return result

        # Return appropriate wrapper based on function type
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def initialize_phoenix(
    project_name: str = "AI-News-LangGraph",
    port: int = 6006,
    auto_instrument: bool = True
) -> PhoenixObserver:
    """Initialize Phoenix observability with default settings.

    Args:
        project_name: Project name for tracing
        port: Phoenix UI port
        auto_instrument: Auto-instrument LangChain and OpenAI

    Returns:
        PhoenixObserver instance
    """
    observer = phoenix_observer
    observer.initialize(
        project_name=project_name,
        phoenix_port=port
    )
    return observer


# Quick start function
def start_observability():
    """Quick start function to enable observability."""
    logger.info("🔍 Starting Phoenix observability...")
    return initialize_phoenix()