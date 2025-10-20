"""
Direct tool access implementation following metamorphosis pattern.

This module provides direct tool access for agents, bypassing
traditional routing and enabling more efficient tool usage.
"""

from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
import logging
from pydantic import BaseModel, Field

from .tools import NewsSearchTool, DocumentProcessor, FileManager
from .schemas import ArticleItem


logger = logging.getLogger(__name__)


class ToolResult(BaseModel):
    """Result from a tool execution."""
    tool_name: str
    success: bool
    output: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DirectToolRegistry:
    """
    Registry for direct tool access.
    Implements the metamorphosis pattern of bypassing MCP routing.
    """

    def __init__(self):
        """Initialize the tool registry."""
        self._tools: Dict[str, Callable] = {}
        self._tool_metadata: Dict[str, Dict[str, Any]] = {}

        # Register default tools
        self._register_default_tools()

    def _register_default_tools(self) -> None:
        """Register the default set of tools."""
        # News search tool
        news_tool = NewsSearchTool()
        self.register_tool(
            "search_news",
            news_tool.search,
            {
                "description": "Search for news articles",
                "parameters": ["query", "max_results"],
                "category": "research"
            }
        )

        # Document processing tools
        doc_processor = DocumentProcessor()
        self.register_tool(
            "extract_key_points",
            doc_processor.extract_key_points,
            {
                "description": "Extract key points from text",
                "parameters": ["text", "max_points"],
                "category": "processing"
            }
        )

        self.register_tool(
            "summarize_text",
            lambda text: doc_processor.summarize(text),
            {
                "description": "Summarize text content",
                "parameters": ["text"],
                "category": "processing"
            }
        )

        # File management tools
        file_manager = FileManager()
        self.register_tool(
            "save_html",
            file_manager.save_html,
            {
                "description": "Save content as HTML file",
                "parameters": ["content", "path"],
                "category": "file_management"
            }
        )

        self.register_tool(
            "save_json",
            file_manager.save_json,
            {
                "description": "Save data as JSON file",
                "parameters": ["data", "path"],
                "category": "file_management"
            }
        )

        # LangGraph-specific tools (metamorphosis pattern)
        self.register_tool(
            "extract_achievements",
            self._extract_achievements,
            {
                "description": "Extract structured achievements from content",
                "parameters": ["content", "context"],
                "category": "langgraph"
            }
        )

        self.register_tool(
            "evaluate_review_text",
            self._evaluate_review_text,
            {
                "description": "Evaluate quality of review text",
                "parameters": ["text", "criteria"],
                "category": "langgraph"
            }
        )

    def register_tool(
        self,
        name: str,
        func: Callable,
        metadata: Dict[str, Any] = None
    ) -> None:
        """
        Register a new tool for direct access.

        Args:
            name: Tool name
            func: Tool function
            metadata: Tool metadata
        """
        self._tools[name] = func
        self._tool_metadata[name] = metadata or {}
        logger.info(f"Registered tool: {name}")

    def execute_tool(
        self,
        name: str,
        **kwargs
    ) -> ToolResult:
        """
        Execute a tool directly.

        Args:
            name: Tool name
            **kwargs: Tool parameters

        Returns:
            ToolResult with execution details
        """
        import time
        start_time = time.time()

        if name not in self._tools:
            return ToolResult(
                tool_name=name,
                success=False,
                error=f"Tool {name} not found"
            )

        try:
            # Execute the tool
            result = self._tools[name](**kwargs)

            return ToolResult(
                tool_name=name,
                success=True,
                output=result,
                execution_time=time.time() - start_time
            )

        except Exception as e:
            logger.error(f"Tool {name} execution failed: {e}")
            return ToolResult(
                tool_name=name,
                success=False,
                error=str(e),
                execution_time=time.time() - start_time
            )

    def get_tool_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a tool."""
        return self._tool_metadata.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[str]:
        """List available tools, optionally filtered by category."""
        if not category:
            return list(self._tools.keys())

        return [
            name for name, meta in self._tool_metadata.items()
            if meta.get("category") == category
        ]

    def _extract_achievements(
        self,
        content: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract structured achievements from content.
        Implements the metamorphosis pattern for achievement extraction.

        Args:
            content: Text content to analyze
            context: Additional context for extraction

        Returns:
            Structured achievements data
        """
        # Simplified implementation - in production, use LLM
        achievements = []
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if any(keyword in line.lower() for keyword in ['achieved', 'completed', 'succeeded']):
                achievements.append({
                    "text": line,
                    "type": "achievement",
                    "confidence": 0.8
                })

        return {
            "achievements": achievements,
            "total_count": len(achievements),
            "extraction_method": "keyword_based",
            "timestamp": datetime.now().isoformat()
        }

    def _evaluate_review_text(
        self,
        text: str,
        criteria: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate the quality of review text.
        Implements the metamorphosis pattern for quality assessment.

        Args:
            text: Text to evaluate
            criteria: Evaluation criteria

        Returns:
            Quality assessment results
        """
        # Default criteria if not provided
        if not criteria:
            criteria = {
                "min_length": 100,
                "required_sections": ["summary", "findings"],
                "tone": "professional"
            }

        # Simple quality scoring
        score = 0.0
        feedback = []

        # Check length
        if len(text) >= criteria.get("min_length", 100):
            score += 0.3
        else:
            feedback.append(f"Text is too short (min: {criteria.get('min_length', 100)} chars)")

        # Check for required sections
        required_sections = criteria.get("required_sections", [])
        for section in required_sections:
            if section.lower() in text.lower():
                score += 0.2
            else:
                feedback.append(f"Missing required section: {section}")

        # Check tone (simplified)
        if criteria.get("tone") == "professional":
            informal_words = ["gonna", "wanna", "kinda", "sorta"]
            if not any(word in text.lower() for word in informal_words):
                score += 0.2
            else:
                feedback.append("Text contains informal language")

        # Structure check
        if text.count('\n\n') >= 2:  # Has paragraphs
            score += 0.1

        if any(text.startswith(marker) for marker in ['#', '##', '-', '*', '1.']):
            score += 0.2  # Has structure markers

        return {
            "quality_score": min(score, 1.0),
            "feedback": feedback,
            "meets_criteria": score >= 0.7,
            "evaluation_timestamp": datetime.now().isoformat(),
            "criteria_used": criteria
        }


class DirectToolExecutor:
    """
    Executor for running tools with advanced features like
    retry logic, caching, and parallel execution.
    """

    def __init__(self, registry: DirectToolRegistry):
        """
        Initialize the executor.

        Args:
            registry: Tool registry to use
        """
        self.registry = registry
        self._cache: Dict[str, Any] = {}

    async def execute_with_retry(
        self,
        tool_name: str,
        max_retries: int = 3,
        **kwargs
    ) -> ToolResult:
        """
        Execute a tool with retry logic.

        Args:
            tool_name: Name of the tool
            max_retries: Maximum number of retries
            **kwargs: Tool parameters

        Returns:
            ToolResult
        """
        import asyncio

        for attempt in range(max_retries + 1):
            result = self.registry.execute_tool(tool_name, **kwargs)

            if result.success:
                return result

            if attempt < max_retries:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Tool {tool_name} failed, retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)

        return result

    async def execute_parallel(
        self,
        tool_calls: List[Dict[str, Any]]
    ) -> List[ToolResult]:
        """
        Execute multiple tools in parallel.

        Args:
            tool_calls: List of tool call specifications

        Returns:
            List of ToolResults
        """
        import asyncio

        tasks = []
        for call in tool_calls:
            tool_name = call.pop("tool_name")
            tasks.append(
                self.execute_with_retry(tool_name, **call)
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to ToolResults
        final_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                final_results.append(ToolResult(
                    tool_name=tool_calls[i].get("tool_name", "unknown"),
                    success=False,
                    error=str(result)
                ))
            else:
                final_results.append(result)

        return final_results

    def execute_with_cache(
        self,
        tool_name: str,
        cache_key: Optional[str] = None,
        cache_ttl: int = 300,
        **kwargs
    ) -> ToolResult:
        """
        Execute a tool with caching.

        Args:
            tool_name: Name of the tool
            cache_key: Cache key (auto-generated if not provided)
            cache_ttl: Cache time-to-live in seconds
            **kwargs: Tool parameters

        Returns:
            ToolResult
        """
        import hashlib
        import time

        # Generate cache key if not provided
        if not cache_key:
            key_data = f"{tool_name}:{str(sorted(kwargs.items()))}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()

        # Check cache
        if cache_key in self._cache:
            cached_data, cached_time = self._cache[cache_key]
            if time.time() - cached_time < cache_ttl:
                logger.info(f"Using cached result for {tool_name}")
                return cached_data

        # Execute tool
        result = self.registry.execute_tool(tool_name, **kwargs)

        # Cache result if successful
        if result.success:
            self._cache[cache_key] = (result, time.time())

        return result