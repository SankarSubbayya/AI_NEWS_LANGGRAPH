"""
Base state models without LangGraph dependency for testing.
"""

from typing import List, Dict, Optional, Any, Literal
from datetime import datetime
from pydantic import BaseModel, Field


class ArticleModel(BaseModel):
    """Structured article data model."""
    title: str
    url: str
    source: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    published_date: Optional[datetime] = None
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class TopicSearchResultModel(BaseModel):
    """Search results for a specific topic."""
    topic_name: str
    topic_description: str
    search_query: str
    articles: List[ArticleModel] = Field(default_factory=list)
    search_timestamp: datetime = Field(default_factory=datetime.now)


class TopicSummaryModel(BaseModel):
    """Comprehensive summary for a topic."""
    topic_name: str
    overview: str
    key_findings: List[str] = Field(default_factory=list)
    notable_trends: List[str] = Field(default_factory=list)
    top_articles: List[ArticleModel] = Field(default_factory=list)
    quality_score: Optional[float] = Field(None, ge=0.0, le=1.0)


class NewsletterContentModel(BaseModel):
    """Newsletter content structure."""
    subject_line: str
    preheader: str
    executive_summary: str
    topics: List[Dict[str, Any]]
    call_to_action: str
    footer_text: str
    generated_at: datetime = Field(default_factory=datetime.now)


class AgentTaskResultModel(BaseModel):
    """Result from an agent task execution."""
    task_name: str
    agent_name: str
    status: Literal["pending", "in_progress", "success", "failed", "skipped"]
    output: Optional[str] = None
    error: Optional[str] = None
    execution_time: float = 0.0
    timestamp: datetime = Field(default_factory=datetime.now)
    retry_count: int = 0


class WorkflowStateBase(BaseModel):
    """
    Base workflow state without LangGraph dependency.
    Used for testing purposes.
    """
    # Configuration
    main_topic: str = "AI in Cancer Care"
    topics_config: Dict[str, Any] = Field(default_factory=dict)
    topics_path: Optional[str] = None

    # Workflow control
    current_stage: Literal[
        "initialized",
        "fetching",
        "summarizing",
        "reviewing",
        "generating",
        "completed",
        "failed"
    ] = "initialized"
    current_topic_index: int = 0
    thread_id: str = Field(default_factory=lambda: f"thread_{datetime.now().timestamp()}")

    # Research data
    topic_results: List[TopicSearchResultModel] = Field(default_factory=list)
    topic_summaries: List[TopicSummaryModel] = Field(default_factory=list)

    # Newsletter
    newsletter_content: Optional[NewsletterContentModel] = None
    executive_summary: Optional[str] = None

    # Quality control
    quality_reviews: Dict[str, Any] = Field(default_factory=dict)
    review_feedback: List[str] = Field(default_factory=list)

    # Outputs
    outputs: Dict[str, str] = Field(default_factory=dict)

    # Tracking
    agent_results: List[AgentTaskResultModel] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

    # Metrics
    total_articles_fetched: int = 0
    total_topics_processed: int = 0
    workflow_start_time: datetime = Field(default_factory=datetime.now)
    workflow_end_time: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

    def add_error(self, error: str) -> None:
        """Add an error message to the state."""
        self.errors.append(f"[{datetime.now().isoformat()}] {error}")

    def add_warning(self, warning: str) -> None:
        """Add a warning message to the state."""
        self.warnings.append(f"[{datetime.now().isoformat()}] {warning}")

    def add_agent_result(self, result: AgentTaskResultModel) -> None:
        """Add an agent task result to the state."""
        self.agent_results.append(result)

    def get_remaining_topics(self) -> List[Dict[str, Any]]:
        """Get list of topics that haven't been processed yet."""
        all_topics = self.topics_config.get("topics", self.topics_config.get("sub_topics", []))
        return all_topics[self.current_topic_index:]

    def is_complete(self) -> bool:
        """Check if the workflow is complete."""
        return self.current_stage in ["completed", "failed"]

    def calculate_metrics(self) -> Dict[str, Any]:
        """Calculate workflow metrics."""
        if self.workflow_end_time:
            duration = (self.workflow_end_time - self.workflow_start_time).total_seconds()
        else:
            duration = (datetime.now() - self.workflow_start_time).total_seconds()

        return {
            "total_articles": self.total_articles_fetched,
            "topics_processed": self.total_topics_processed,
            "success_rate": sum(1 for r in self.agent_results if r.status == "success") / max(len(self.agent_results), 1),
            "duration_seconds": duration,
            "errors_count": len(self.errors),
            "warnings_count": len(self.warnings)
        }


# Alias for compatibility
WorkflowState = WorkflowStateBase