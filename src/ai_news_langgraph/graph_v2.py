"""
Refactored LangGraph implementation following metamorphosis pattern.

This module provides the main entry point for the AI News workflow,
implementing patterns from the metamorphosis template:
- Pydantic-based state management
- WorkflowExecutor for orchestration
- Direct tool access for agents
- Self-reviewing capabilities
- Thread-based conversation management
"""

from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime

from .workflow import WorkflowExecutor, ParallelWorkflowExecutor
from .state import WorkflowState
from .tools_direct import DirectToolRegistry


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AINewsWorkflow:
    """
    Main workflow class implementing the metamorphosis pattern.
    Provides high-level interface for AI News generation workflow.
    """

    def __init__(
        self,
        use_parallel: bool = False,
        checkpoint_type: str = "memory",
        enable_streaming: bool = False
    ):
        """
        Initialize the AI News workflow.

        Args:
            use_parallel: Enable parallel topic processing
            checkpoint_type: Type of checkpointing ("memory" or "sqlite")
            enable_streaming: Enable real-time streaming updates
        """
        self.use_parallel = use_parallel
        self.enable_streaming = enable_streaming

        # Initialize executor
        if use_parallel:
            self.executor = ParallelWorkflowExecutor(checkpoint_type)
        else:
            self.executor = WorkflowExecutor(checkpoint_type)

        # Initialize direct tool registry
        self.tool_registry = DirectToolRegistry()

        # Build the graph
        self.graph = self.executor.build_graph()

        logger.info(f"Initialized AINewsWorkflow (parallel={use_parallel}, streaming={enable_streaming})")

    async def run_async(
        self,
        main_topic: str = "AI in Cancer Care",
        topics_path: Optional[str] = None,
        thread_id: Optional[str] = None,
        selected_topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run the workflow asynchronously.

        Args:
            main_topic: Main research topic
            topics_path: Path to topics configuration file
            thread_id: Thread ID for conversation management
            selected_topics: List of topic names to include in newsletter (None = all)

        Returns:
            Workflow execution results
        """
        logger.info(f"Starting async workflow for topic: {main_topic}")

        try:
            # Execute the workflow
            result = await self.executor.execute(
                main_topic=main_topic,
                topics_path=topics_path,
                thread_id=thread_id,
                stream_output=self.enable_streaming,
                selected_topics=selected_topics
            )

            # Log execution summary
            self._log_execution_summary(result)

            return result

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}", exc_info=True)
            return {
                "status": "failed",
                "error": str(e)
            }

    def run(
        self,
        main_topic: str = "AI in Cancer Care",
        topics_path: Optional[str] = None,
        thread_id: Optional[str] = None,
        selected_topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run the workflow synchronously.

        Args:
            main_topic: Main research topic
            topics_path: Path to topics configuration file
            thread_id: Thread ID for conversation management
            selected_topics: List of topic names to include in newsletter (None = all)

        Returns:
            Workflow execution results
        """
        # Run async workflow in sync context
        return asyncio.run(self.run_async(main_topic, topics_path, thread_id, selected_topics))

    def resume(self, thread_id: str) -> Dict[str, Any]:
        """
        Resume a previously started workflow.

        Args:
            thread_id: Thread ID to resume

        Returns:
            Workflow execution results
        """
        logger.info(f"Resuming workflow for thread: {thread_id}")

        # Get current state
        current_state = self.executor.get_state(thread_id)

        if not current_state:
            return {
                "status": "error",
                "error": f"No state found for thread {thread_id}"
            }

        # Resume execution
        return asyncio.run(self.executor.execute(
            main_topic=current_state.main_topic,
            topics_path=current_state.topics_path,
            thread_id=thread_id,
            stream_output=self.enable_streaming
        ))

    def get_status(self, thread_id: str) -> Dict[str, Any]:
        """
        Get the current status of a workflow.

        Args:
            thread_id: Thread ID to check

        Returns:
            Status information
        """
        state = self.executor.get_state(thread_id)

        if not state:
            return {
                "status": "not_found",
                "thread_id": thread_id
            }

        return {
            "status": "active" if not state.is_complete() else "completed",
            "thread_id": thread_id,
            "current_stage": state.current_stage,
            "topics_processed": state.total_topics_processed,
            "articles_fetched": state.total_articles_fetched,
            "errors_count": len(state.errors),
            "warnings_count": len(state.warnings),
            "all_topics": state.get_all_topic_names(),
            "selected_topics": state.selected_topic_names
        }

    def get_available_topics(self, thread_id: str) -> List[str]:
        """
        Get list of all topics that have been processed in a workflow.

        Args:
            thread_id: Thread ID to check

        Returns:
            List of topic names
        """
        state = self.executor.get_state(thread_id)
        if not state:
            return []
        return state.get_all_topic_names()

    def list_workflows(self) -> List[Dict[str, Any]]:
        """
        List all available workflows.

        Returns:
            List of workflow summaries
        """
        thread_ids = self.executor.list_threads()

        workflows = []
        for thread_id in thread_ids:
            status = self.get_status(thread_id)
            workflows.append(status)

        return workflows

    def _log_execution_summary(self, result: Dict[str, Any]) -> None:
        """Log a summary of the execution results."""
        logger.info("=" * 60)
        logger.info("WORKFLOW EXECUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Status: {result.get('status', 'unknown')}")

        if 'metrics' in result:
            metrics = result['metrics']
            logger.info(f"Topics Processed: {metrics.get('topics_processed', 0)}")
            logger.info(f"Articles Fetched: {metrics.get('total_articles', 0)}")
            logger.info(f"Success Rate: {metrics.get('success_rate', 0):.2%}")
            logger.info(f"Duration: {metrics.get('duration_seconds', 0):.2f}s")

        if 'outputs' in result:
            logger.info(f"Outputs: {result['outputs']}")

        if 'errors' in result and result['errors']:
            logger.warning(f"Errors: {len(result['errors'])}")
            for error in result['errors'][:5]:  # Show first 5 errors
                logger.warning(f"  - {error}")

        logger.info("=" * 60)


def build_multi_agent_graph():
    """
    Build and return a function to run the multi-agent workflow.
    Provides backward compatibility with the original interface.

    Returns:
        Callable that runs the workflow
    """
    workflow = AINewsWorkflow(use_parallel=False)

    def run(topic: str = "AI in Cancer Care", topics_json_path: str = None) -> Dict:
        """
        Run the multi-agent workflow.

        Args:
            topic: Main research topic
            topics_json_path: Path to topics configuration file

        Returns:
            Execution results
        """
        return workflow.run(
            main_topic=topic,
            topics_path=topics_json_path
        )

    return run


# CLI Interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI News LangGraph Workflow")
    parser.add_argument("--topic", default="AI in Cancer Care", help="Main research topic")
    parser.add_argument("--config", help="Path to topics configuration file")
    parser.add_argument("--parallel", action="store_true", help="Enable parallel processing")
    parser.add_argument("--stream", action="store_true", help="Enable streaming updates")
    parser.add_argument("--thread-id", help="Thread ID for resuming workflow")
    parser.add_argument("--checkpoint", choices=["memory", "sqlite"], default="memory",
                        help="Checkpoint type")

    args = parser.parse_args()

    # Initialize workflow
    workflow = AINewsWorkflow(
        use_parallel=args.parallel,
        checkpoint_type=args.checkpoint,
        enable_streaming=args.stream
    )

    # Run or resume workflow
    if args.thread_id:
        print(f"Resuming workflow {args.thread_id}...")
        result = workflow.resume(args.thread_id)
    else:
        print(f"Starting new workflow for topic: {args.topic}")
        result = workflow.run(
            main_topic=args.topic,
            topics_path=args.config
        )

    # Display results
    print("\nWorkflow completed!")
    print(f"Status: {result['status']}")
    if 'outputs' in result:
        print(f"Outputs: {result['outputs']}")
    if 'errors' in result and result['errors']:
        print(f"Errors: {result['errors']}")