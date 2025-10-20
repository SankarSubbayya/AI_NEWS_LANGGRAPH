"""Schema definitions for structured outputs in AI News LangGraph."""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ArticleItem(BaseModel):
    """Schema for a single news article."""
    title: str = Field(description="Article title")
    url: str = Field(description="Article URL")
    source: Optional[str] = Field(default=None, description="Source website or publication")
    content: Optional[str] = Field(default=None, description="Article content or snippet")
    summary: Optional[str] = Field(default=None, description="AI-generated summary")
    published_date: Optional[str] = Field(default=None, description="Publication date")
    relevance_score: Optional[float] = Field(default=0.5, description="Relevance score (0-1)")
    category: Optional[str] = Field(default=None, description="Article category")


class TopicSearchResult(BaseModel):
    """Schema for search results for a specific topic."""
    topic_name: str = Field(description="Name of the topic")
    topic_description: str = Field(description="Description of the topic")
    search_query: str = Field(description="Query used for search")
    articles: List[ArticleItem] = Field(default_factory=list, description="List of articles found")
    search_timestamp: datetime = Field(default_factory=datetime.now, description="When search was performed")


class FetchResult(BaseModel):
    """Schema for the complete fetch operation result."""
    main_topic: str = Field(description="Main research topic")
    topics: List[TopicSearchResult] = Field(description="Results for each sub-topic")
    total_articles: int = Field(description="Total number of articles fetched")
    fetch_timestamp: datetime = Field(default_factory=datetime.now, description="When fetch was performed")

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "main_topic": self.main_topic,
            "topics": [
                {
                    "topic_name": t.topic_name,
                    "topic_description": t.topic_description,
                    "articles": [a.model_dump() for a in t.articles]
                }
                for t in self.topics
            ],
            "total_articles": self.total_articles,
            "timestamp": self.fetch_timestamp.isoformat()
        }


class TopicSummary(BaseModel):
    """Schema for a summarized topic."""
    topic_name: str = Field(description="Name of the topic")
    overview: str = Field(description="Topic overview (180-250 words)")
    key_findings: List[str] = Field(description="Key findings (3-5 bullet points)")
    notable_trends: List[str] = Field(description="Notable trends identified")
    top_articles: List[ArticleItem] = Field(description="Top 3-5 most relevant articles")
    insights: Optional[str] = Field(default=None, description="Additional insights")


class SummariesOutput(BaseModel):
    """Schema for the complete summaries output."""
    executive_summary: str = Field(description="Executive summary of all topics (200-250 words)")
    topic_summaries: List[TopicSummary] = Field(description="Summaries for each topic")
    overall_trends: List[str] = Field(description="Overall trends across all topics")
    recommendations: List[str] = Field(description="Recommendations for further research")
    summary_timestamp: datetime = Field(default_factory=datetime.now, description="When summary was created")

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "executive_summary": self.executive_summary,
            "topics": [
                {
                    "name": t.topic_name,
                    "overview": t.overview,
                    "key_findings": t.key_findings,
                    "notable_trends": t.notable_trends,
                    "top_articles": [a.model_dump() for a in t.top_articles]
                }
                for t in self.topic_summaries
            ],
            "overall_trends": self.overall_trends,
            "recommendations": self.recommendations,
            "timestamp": self.summary_timestamp.isoformat()
        }


class NewsletterContent(BaseModel):
    """Schema for newsletter content."""
    subject_line: str = Field(description="Email subject line")
    preheader: str = Field(description="Email preheader text")
    executive_summary: str = Field(description="Executive summary")
    topics: List[Dict[str, Any]] = Field(description="Topic sections with articles")
    call_to_action: Optional[str] = Field(default=None, description="Call to action")
    footer_text: Optional[str] = Field(default=None, description="Footer text")


class WorkflowState(BaseModel):
    """Schema for workflow state management."""
    current_stage: str = Field(description="Current workflow stage")
    completed_stages: List[str] = Field(default_factory=list, description="Completed stages")
    fetch_result: Optional[FetchResult] = Field(default=None, description="Fetch operation result")
    summaries: Optional[SummariesOutput] = Field(default=None, description="Summaries result")
    newsletter: Optional[NewsletterContent] = Field(default=None, description="Newsletter content")
    errors: List[str] = Field(default_factory=list, description="Any errors encountered")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class TaskConfig(BaseModel):
    """Schema for task configuration."""
    name: str = Field(description="Task name")
    description: str = Field(description="Task description")
    agent: str = Field(description="Agent responsible for task")
    agent_class: Optional[str] = Field(default=None, description="Python agent class name")
    dependencies: List[str] = Field(default_factory=list, description="Task dependencies")
    expected_output: str = Field(description="Expected output format")
    timeout_seconds: Optional[int] = Field(default=300, description="Task timeout")
    retry_count: Optional[int] = Field(default=1, description="Number of retries on failure")


class AgentTaskResult(BaseModel):
    """Schema for agent task execution result."""
    task_name: str = Field(description="Name of the executed task")
    agent_name: str = Field(description="Agent that executed the task")
    status: str = Field(description="Task status: success, failed, or partial")
    output: Any = Field(description="Task output")
    execution_time: float = Field(description="Execution time in seconds")
    error_message: Optional[str] = Field(default=None, description="Error message if failed")
    retry_count: int = Field(default=0, description="Number of retries attempted")