"""LangSmith Observability Integration for AI Newsletter Workflow.

LangSmith provides cloud-based tracing and observability without needing
to run a local server like Phoenix.
"""

import os
import logging
from typing import Optional, Dict, Any
from functools import wraps

logger = logging.getLogger(__name__)


class LangSmithObserver:
    """LangSmith observability for AI Newsletter workflow."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        """Initialize LangSmith observer."""
        if not self.initialized:
            self.initialized = False
            self.enabled = False
            self.api_key = None
            self.project_name = None
            self.traces = {}

    def initialize(self, project_name: str = "AI-News-LangGraph") -> bool:
        """Initialize LangSmith observability.

        Args:
            project_name: Name of the LangSmith project

        Returns:
            True if initialized successfully, False otherwise
        """
        try:
            # Check if LangSmith API key is set
            self.api_key = os.getenv('LANGSMITH_API_KEY')

            if not self.api_key:
                logger.info("💡 LangSmith API key not set. Set LANGSMITH_API_KEY environment variable to enable tracing.")
                logger.info("   Get your API key from: https://smith.langchain.com/")
                self.enabled = False
                return False

            # Set LangSmith environment variables
            os.environ['LANGCHAIN_TRACING_V2'] = 'true'
            os.environ['LANGCHAIN_PROJECT'] = project_name

            self.project_name = project_name
            self.enabled = True
            self.initialized = True

            logger.info(f"✅ LangSmith initialized for project: {project_name}")
            logger.info(f"   📊 Dashboard: https://smith.langchain.com/")
            logger.info(f"   Project: https://smith.langchain.com/o/USER_ID/projects/p/{project_name}")

            return True

        except Exception as e:
            logger.warning(f"⚠️ Failed to initialize LangSmith: {e}")
            self.enabled = False
            return False

    def is_enabled(self) -> bool:
        """Check if LangSmith tracing is enabled."""
        return self.enabled

    def get_dashboard_url(self) -> str:
        """Get LangSmith dashboard URL."""
        if self.project_name:
            return f"https://smith.langchain.com/projects/p/{self.project_name}"
        return "https://smith.langchain.com/"

    def trace_function(self, name: str = None):
        """Decorator to trace function execution.

        Args:
            name: Optional name for the trace (defaults to function name)

        Returns:
            Decorated function with tracing
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                func_name = name or func.__name__

                if self.enabled:
                    logger.debug(f"🔍 Tracing: {func_name}")

                try:
                    result = func(*args, **kwargs)
                    if self.enabled:
                        logger.debug(f"✅ Trace complete: {func_name}")
                    return result
                except Exception as e:
                    if self.enabled:
                        logger.error(f"❌ Trace error in {func_name}: {e}")
                    raise

            return wrapper
        return decorator

    def log_metric(self, name: str, value: Any, metadata: Dict[str, Any] = None):
        """Log a metric for the current trace.

        Args:
            name: Metric name
            value: Metric value
            metadata: Optional metadata dictionary
        """
        if self.enabled:
            try:
                log_data = {
                    'metric_name': name,
                    'value': value,
                    'timestamp': str(datetime.now())
                }

                if metadata:
                    log_data.update(metadata)

                logger.info(f"📊 Metric: {name} = {value}")

                if name not in self.traces:
                    self.traces[name] = []
                self.traces[name].append(log_data)

            except Exception as e:
                logger.debug(f"Failed to log metric {name}: {e}")

    def get_trace_summary(self) -> Dict[str, Any]:
        """Get summary of all traces."""
        return {
            'enabled': self.enabled,
            'project_name': self.project_name,
            'dashboard_url': self.get_dashboard_url(),
            'total_metrics': len(self.traces),
            'metrics': self.traces
        }


# Global instance
langsmith_observer = LangSmithObserver()


def initialize_langsmith(project_name: str = "AI-News-LangGraph") -> LangSmithObserver:
    """Initialize LangSmith observability.

    Args:
        project_name: Name of the LangSmith project

    Returns:
        LangSmithObserver instance
    """
    observer = LangSmithObserver()
    observer.initialize(project_name)
    return observer


def trace_node(func):
    """Decorator to trace a node execution.

    Args:
        func: Function to trace

    Returns:
        Decorated function
    """
    node_name = func.__name__

    def wrapper(*args, **kwargs):
        observer = LangSmithObserver()

        if observer.is_enabled():
            logger.info(f"🔬 Node: {node_name}")

        try:
            result = func(*args, **kwargs)

            if observer.is_enabled():
                logger.info(f"✅ Node complete: {node_name}")

            return result

        except Exception as e:
            if observer.is_enabled():
                logger.error(f"❌ Node error in {node_name}: {e}")
            raise

    return wrapper


# Import datetime for timestamp
from datetime import datetime

__all__ = [
    'LangSmithObserver',
    'langsmith_observer',
    'initialize_langsmith',
    'trace_node'
]