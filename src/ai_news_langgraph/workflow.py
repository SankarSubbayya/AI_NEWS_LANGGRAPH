"""WorkflowExecutor for orchestrating the LangGraph workflow."""

from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# Try to import SqliteSaver, but make it optional
try:
    from langgraph.checkpoint.sqlite import SqliteSaver
    SQLITE_AVAILABLE = True
except ImportError:
    SqliteSaver = None
    SQLITE_AVAILABLE = False

# Use state_base to avoid circular dependency with LangGraph MessagesState
try:
    from .state import WorkflowState
except ImportError:
    # Fallback to state_base if state.py has import issues
    from .state_base import WorkflowState
from .nodes_v2 import WorkflowNodesV2

# Initialize logger first
logger = logging.getLogger(__name__)

# Import Phoenix observability
try:
    from .observability import phoenix_observer
    PHOENIX_ENABLED = True
except ImportError:
    PHOENIX_ENABLED = False
    logger.info("Phoenix observability not available")


class WorkflowExecutor:
    """
    Centralized executor for the AI News workflow.
    Implements the metamorphosis pattern with direct tool access
    and self-reviewing capabilities.
    """

    def __init__(self, checkpoint_type: str = "memory"):
        """
        Initialize the workflow executor.

        Args:
            checkpoint_type: Type of checkpointing ("memory" or "sqlite")
        """
        self.nodes = WorkflowNodesV2()
        self.checkpoint_type = checkpoint_type
        self.graph = None
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # Build the graph immediately (LLM is now lazy-loaded)
        self.build_graph()

    def build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow with modular nodes and edges.

        Returns:
            Compiled StateGraph
        """
        logger.info("Building workflow graph")

        # Create the graph builder
        builder = StateGraph(WorkflowState)

        # Add all nodes
        self._add_nodes(builder)

        # Add all edges
        self._add_edges(builder)

        # Compile with appropriate checkpointer
        checkpointer = self._get_checkpointer()
        self.graph = builder.compile(checkpointer=checkpointer)

        logger.info("Graph built successfully")
        return self.graph

    def _add_nodes(self, builder: StateGraph) -> None:
        """Add all nodes to the graph."""
        # Initialization
        builder.add_node("initialize", self.nodes.initialize_workflow)

        # Research phase
        builder.add_node("fetch_news", self.nodes.fetch_news_for_topic)
        builder.add_node("summarize_topic", self.nodes.summarize_topic)

        # Quality control
        builder.add_node("review_quality", self.nodes.review_quality)

        # Final generation
        builder.add_node("generate_newsletter", self.nodes.generate_newsletter)

        # Set entry point
        builder.set_entry_point("initialize")

    def _add_edges(self, builder: StateGraph) -> None:
        """Add all edges and conditional routing to the graph."""
        # Linear flow from initialization
        builder.add_edge("initialize", "fetch_news")

        # Fetch -> Summarize flow
        builder.add_edge("fetch_news", "summarize_topic")

        # Conditional routing after summarization
        builder.add_conditional_edges(
            "summarize_topic",
            self._should_continue_topics,
            {
                "fetch_more": "fetch_news",
                "review": "review_quality"
            }
        )

        # Review -> Generate flow
        builder.add_edge("review_quality", "generate_newsletter")

        # End
        builder.add_edge("generate_newsletter", END)

    def _should_continue_topics(self, state: dict) -> str:
        """
        Determine whether to continue fetching topics or move to review.
        
        LangGraph passes state as dict, not Pydantic model.

        Args:
            state: Current workflow state (dict)

        Returns:
            Next node to execute ("fetch_more" or "review")
        """
        topics_config = state.get("topics_config", {})
        topics = topics_config.get("topics", [])
        current_index = state.get("current_topic_index", 0)

        logger.info(f"Decision point: {current_index}/{len(topics)} topics processed")

        if current_index < len(topics):
            return "fetch_more"
        else:
            return "review"

    def _get_checkpointer(self):
        """Get the appropriate checkpointer based on configuration."""
        if self.checkpoint_type == "sqlite":
            if SQLITE_AVAILABLE:
                return SqliteSaver.from_conn_string("checkpoints.db")
            else:
                logger.warning("SQLite checkpointing not available, falling back to memory")
                return MemorySaver()
        else:
            return MemorySaver()

    async def execute(
        self,
        main_topic: str = "AI in Cancer Care",
        topics_path: Optional[str] = None,
        thread_id: Optional[str] = None,
        stream_output: bool = False,
        selected_topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Execute the workflow asynchronously.

        Args:
            main_topic: Main research topic
            topics_path: Path to topics configuration
            thread_id: Thread ID for conversation management
            stream_output: Whether to stream outputs in real-time
            selected_topics: List of topic names to include in newsletter (None = all topics)

        Returns:
            Execution results dictionary
        """
        # Build graph if not already built
        if not self.graph:
            self.build_graph()

        # Create thread_id first
        thread_id_str = thread_id or f"thread_{datetime.now().timestamp()}"

        # Create initial state
        initial_state = WorkflowState(
            main_topic=main_topic,
            topics_path=topics_path,
            thread_id=thread_id_str,
            selected_topic_names=selected_topics
        )

        # Configuration for execution
        config = {
            "configurable": {"thread_id": thread_id_str},
            "recursion_limit": 100
        }

        try:
            # Debug: Check what type initial_state is
            logger.info(f"initial_state type: {type(initial_state)}, has thread_id: {hasattr(initial_state, 'thread_id')}")
            
            # Ensure initial_state is a WorkflowState object
            if isinstance(initial_state, dict):
                logger.warning("initial_state is a dict, converting to WorkflowState")
                initial_state = WorkflowState(**initial_state)
            
            if stream_output:
                # Stream execution for real-time updates
                final_state = await self._execute_with_streaming(
                    initial_state,
                    config
                )
            else:
                # Standard execution
                final_state = await self._execute_standard(
                    initial_state,
                    config
                )

            # Work with final_state as dict (WorkflowState is a TypedDict, not a Pydantic model)
            logger.info("Processing final state (dict)")
            
            # Calculate metrics from dict
            metrics = {
                "duration_seconds": 0,
                "total_articles": final_state.get("total_articles_fetched", 0),
                "total_topics": len(final_state.get("topic_results", []))
            }
            
            return {
                "status": "completed" if not final_state.get("errors") else "completed_with_errors",
                "outputs": final_state.get("outputs", {}),
                "errors": final_state.get("errors", []),
                "warnings": final_state.get("warnings", []),
                "agent_results": final_state.get("agent_results", []),
                "metrics": metrics,
                "thread_id": final_state.get("thread_id", thread_id_str)
            }

        except Exception as e:
            import traceback
            logger.error(f"Workflow execution failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "status": "failed",
                "error": str(e),
                "traceback": traceback.format_exc(),
                "thread_id": thread_id_str
            }

    async def _execute_standard(
        self,
        initial_state: WorkflowState,
        config: Dict[str, Any]
    ) -> WorkflowState:
        """Execute workflow in standard mode."""
        # Handle both dict and WorkflowState
        if isinstance(initial_state, dict):
            thread_id_val = initial_state.get("thread_id", "unknown")
            state_obj = WorkflowState(**initial_state)
            initial_state_dict = initial_state  # Already a dict
        else:
            thread_id_val = initial_state.thread_id
            state_obj = initial_state
            initial_state_dict = initial_state.model_dump()
            
        logger.info(f"Starting standard execution for thread {thread_id_val}")

        # initial_state_dict is now properly set for Lang Graph

        # Run the graph asynchronously (nodes are async)
        final_state_dict = await self.graph.ainvoke(
            initial_state_dict,  # Pass dict, not Pydantic object
            config
        )

        # Convert dict back to WorkflowState if needed
        if isinstance(final_state_dict, dict):
            try:
                final_state = WorkflowState(**final_state_dict)
                logger.info(f"Converted final_state_dict to WorkflowState: type={type(final_state)}")
            except Exception as e:
                logger.error(f"Failed to convert final_state_dict to WorkflowState: {e}")
                # Return dict as-is if conversion fails
                logger.warning("Returning dict instead of WorkflowState")
                return final_state_dict
        else:
            final_state = final_state_dict

        logger.info(f"Returning final_state: type={type(final_state)}")
        return final_state

    async def _execute_with_streaming(
        self,
        initial_state: WorkflowState,
        config: Dict[str, Any]
    ) -> WorkflowState:
        """Execute workflow with streaming updates."""
        # Handle both dict and WorkflowState
        if isinstance(initial_state, dict):
            thread_id_val = initial_state.get("thread_id", "unknown")
            state_obj = WorkflowState(**initial_state)
            initial_state_dict = initial_state  # Already a dict
        else:
            thread_id_val = initial_state.thread_id
            state_obj = initial_state
            initial_state_dict = initial_state.model_dump()
            
        logger.info(f"Starting streaming execution for thread {thread_id_val}")

        # Use state_obj for initial state
        final_state = state_obj

        # Stream through the graph
        async for chunk in self.graph.astream(initial_state_dict, config):
            # Process each chunk and emit updates
            for node_name, node_state in chunk.items():
                logger.info(f"Processing node: {node_name}")

                # Emit real-time update (can be sent via SSE, WebSocket, etc.)
                await self._emit_update(node_name, node_state)

                # Convert dict to WorkflowState
                if isinstance(node_state, dict):
                    final_state = WorkflowState(**node_state)
                else:
                    final_state = node_state

        return final_state

    async def _emit_update(self, node_name: str, state: WorkflowState) -> None:
        """
        Emit real-time update for streaming mode.

        Args:
            node_name: Name of the current node
            state: Current state
        """
        update = {
            "node": node_name,
            "stage": state.current_stage,
            "topics_processed": state.total_topics_processed,
            "articles_fetched": state.total_articles_fetched,
            "timestamp": datetime.now().isoformat()
        }

        # In a real implementation, this would send via SSE/WebSocket
        logger.info(f"Update: {update}")

    def get_state(self, thread_id: str) -> Optional[WorkflowState]:
        """
        Get the current state for a given thread.

        Args:
            thread_id: Thread identifier

        Returns:
            Current workflow state or None
        """
        if not self.graph:
            return None

        try:
            config = {"configurable": {"thread_id": thread_id}}
            state = self.graph.get_state(config)
            return state.values if state else None
        except Exception as e:
            logger.error(f"Failed to get state for thread {thread_id}: {e}")
            return None

    def list_threads(self) -> List[str]:
        """
        List all available thread IDs.

        Returns:
            List of thread IDs
        """
        # Implementation depends on checkpoint type
        # This is a simplified version
        return []


class ParallelWorkflowExecutor(WorkflowExecutor):
    """
    Extended executor with parallel task execution capabilities.
    """

    def _add_nodes(self, builder: StateGraph) -> None:
        """Add nodes including parallel execution support."""
        super()._add_nodes(builder)

        # Add parallel fetch node for multiple topics
        builder.add_node("parallel_fetch", self._parallel_fetch_topics)

    async def _parallel_fetch_topics(self, state: WorkflowState) -> WorkflowState:
        """
        Fetch multiple topics in parallel for improved performance.

        Args:
            state: Current workflow state

        Returns:
            Updated state with all fetched topics
        """
        topics = state.topics_config.get("topics", [])
        remaining_topics = topics[state.current_topic_index:]

        if not remaining_topics:
            return state

        # Create tasks for parallel execution
        tasks = []
        for i, topic in enumerate(remaining_topics[:3]):  # Process up to 3 in parallel
            # Create a copy of state for parallel execution
            topic_state = state.model_copy()
            topic_state.current_topic_index = state.current_topic_index + i
            tasks.append(self.nodes.fetch_news_for_topic(topic_state))

        # Execute in parallel
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Merge results back into state
        for result in results:
            if isinstance(result, Exception):
                state.add_error(f"Parallel fetch error: {str(result)}")
            elif isinstance(result, WorkflowState):
                # Merge topic results
                for topic_result in result.topic_results:
                    if topic_result not in state.topic_results:
                        state.topic_results.append(topic_result)

                # Update metrics
                state.total_articles_fetched += result.total_articles_fetched

        # Update index
        state.current_topic_index += len(tasks)

        return state