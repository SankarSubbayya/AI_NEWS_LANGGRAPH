"""
Unit tests for WorkflowState and related models.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

from src.ai_news_langgraph.state_base import (
    WorkflowState,
    ArticleModel,
    TopicSearchResultModel,
    TopicSummaryModel,
    AgentTaskResultModel,
    NewsletterContentModel
)


class TestArticleModel:
    """Test ArticleModel validation and functionality."""

    def test_article_creation(self):
        """Test creating a valid article."""
        article = ArticleModel(
            title="AI Breakthrough in Cancer Detection",
            url="https://example.com/article",
            source="Medical Journal",
            content="Full article content...",
            summary="AI system achieves 95% accuracy",
            relevance_score=0.85
        )

        assert article.title == "AI Breakthrough in Cancer Detection"
        assert article.relevance_score == 0.85
        assert article.source == "Medical Journal"

    def test_article_relevance_validation(self):
        """Test relevance score validation."""
        # Valid score
        article = ArticleModel(
            title="Test Article",
            url="https://example.com",
            relevance_score=0.5
        )
        assert article.relevance_score == 0.5

        # Invalid score (should fail)
        with pytest.raises(ValidationError):
            ArticleModel(
                title="Test Article",
                url="https://example.com",
                relevance_score=1.5  # > 1.0
            )

    def test_article_optional_fields(self):
        """Test article with minimal required fields."""
        article = ArticleModel(
            title="Minimal Article",
            url="https://example.com"
        )

        assert article.source is None
        assert article.content is None
        assert article.summary is None
        assert article.relevance_score is None


class TestTopicSearchResultModel:
    """Test TopicSearchResultModel functionality."""

    def test_topic_search_result_creation(self):
        """Test creating a topic search result."""
        articles = [
            ArticleModel(title="Article 1", url="https://example.com/1"),
            ArticleModel(title="Article 2", url="https://example.com/2")
        ]

        result = TopicSearchResultModel(
            topic_name="AI Diagnostics",
            topic_description="AI in medical diagnostics",
            search_query="AI cancer diagnosis",
            articles=articles
        )

        assert result.topic_name == "AI Diagnostics"
        assert len(result.articles) == 2
        assert result.search_timestamp is not None

    def test_empty_articles_list(self):
        """Test topic result with no articles."""
        result = TopicSearchResultModel(
            topic_name="Test Topic",
            topic_description="Test description",
            search_query="test query"
        )

        assert result.articles == []
        assert isinstance(result.search_timestamp, datetime)


class TestAgentTaskResultModel:
    """Test AgentTaskResultModel functionality."""

    def test_successful_task_result(self):
        """Test creating a successful task result."""
        result = AgentTaskResultModel(
            task_name="fetch_news",
            agent_name="research_agent",
            status="success",
            output="Fetched 10 articles",
            execution_time=2.5
        )

        assert result.status == "success"
        assert result.output == "Fetched 10 articles"
        assert result.error is None
        assert result.execution_time == 2.5

    def test_failed_task_result(self):
        """Test creating a failed task result."""
        result = AgentTaskResultModel(
            task_name="fetch_news",
            agent_name="research_agent",
            status="failed",
            error="API rate limit exceeded",
            execution_time=0.1
        )

        assert result.status == "failed"
        assert result.error == "API rate limit exceeded"
        assert result.output is None

    def test_invalid_status(self):
        """Test that invalid status raises validation error."""
        with pytest.raises(ValidationError):
            AgentTaskResultModel(
                task_name="test",
                agent_name="test_agent",
                status="invalid_status"  # Not in allowed values
            )


class TestWorkflowState:
    """Test WorkflowState functionality."""

    def test_workflow_state_initialization(self):
        """Test creating a workflow state."""
        state = WorkflowState()

        assert state.main_topic == "AI in Cancer Care"
        assert state.current_stage == "initialized"
        assert state.current_topic_index == 0
        assert state.topic_results == []
        assert state.errors == []
        assert isinstance(state.thread_id, str)

    def test_add_error(self):
        """Test adding errors to state."""
        state = WorkflowState()
        state.add_error("Test error message")

        assert len(state.errors) == 1
        assert "Test error message" in state.errors[0]
        assert datetime.now().isoformat()[:10] in state.errors[0]  # Check date

    def test_add_warning(self):
        """Test adding warnings to state."""
        state = WorkflowState()
        state.add_warning("Test warning")

        assert len(state.warnings) == 1
        assert "Test warning" in state.warnings[0]

    def test_add_agent_result(self):
        """Test adding agent results."""
        state = WorkflowState()
        result = AgentTaskResultModel(
            task_name="test_task",
            agent_name="test_agent",
            status="success"
        )

        state.add_agent_result(result)
        assert len(state.agent_results) == 1
        assert state.agent_results[0].task_name == "test_task"

    def test_get_remaining_topics(self):
        """Test getting remaining topics."""
        state = WorkflowState()
        state.topics_config = {
            "topics": [
                {"name": "Topic 1"},
                {"name": "Topic 2"},
                {"name": "Topic 3"}
            ]
        }
        state.current_topic_index = 1

        remaining = state.get_remaining_topics()
        assert len(remaining) == 2
        assert remaining[0]["name"] == "Topic 2"

    def test_is_complete(self):
        """Test completion checking."""
        state = WorkflowState()

        # Not complete initially
        assert not state.is_complete()

        # Complete when stage is "completed"
        state.current_stage = "completed"
        assert state.is_complete()

        # Also complete when "failed"
        state.current_stage = "failed"
        assert state.is_complete()

    def test_calculate_metrics(self):
        """Test metrics calculation."""
        state = WorkflowState()
        state.total_articles_fetched = 25
        state.total_topics_processed = 3

        # Add some results
        state.add_agent_result(AgentTaskResultModel(
            task_name="task1",
            agent_name="agent1",
            status="success"
        ))
        state.add_agent_result(AgentTaskResultModel(
            task_name="task2",
            agent_name="agent2",
            status="failed"
        ))

        metrics = state.calculate_metrics()

        assert metrics["total_articles"] == 25
        assert metrics["topics_processed"] == 3
        assert metrics["success_rate"] == 0.5  # 1 success, 1 failed
        assert metrics["errors_count"] == 0
        assert "duration_seconds" in metrics


class TestTopicSummaryModel:
    """Test TopicSummaryModel functionality."""

    def test_topic_summary_with_quality(self):
        """Test topic summary with quality score."""
        summary = TopicSummaryModel(
            topic_name="AI Research",
            overview="Comprehensive overview of AI research",
            key_findings=["Finding 1", "Finding 2"],
            notable_trends=["Trend 1"],
            quality_score=0.85
        )

        assert summary.quality_score == 0.85
        assert len(summary.key_findings) == 2

    def test_topic_summary_validation(self):
        """Test quality score validation."""
        with pytest.raises(ValidationError):
            TopicSummaryModel(
                topic_name="Test",
                overview="Test overview",
                quality_score=1.5  # Invalid: > 1.0
            )


class TestNewsletterContentModel:
    """Test NewsletterContentModel functionality."""

    def test_newsletter_creation(self):
        """Test creating newsletter content."""
        newsletter = NewsletterContentModel(
            subject_line="AI Cancer Research Update",
            preheader="Latest developments",
            executive_summary="This week's summary...",
            topics=[{"name": "Topic 1", "summary": "Summary 1"}],
            call_to_action="Subscribe now",
            footer_text="© 2024"
        )

        assert newsletter.subject_line == "AI Cancer Research Update"
        assert len(newsletter.topics) == 1
        assert newsletter.generated_at is not None


# Fixtures for testing
@pytest.fixture
def sample_workflow_state():
    """Create a sample workflow state for testing."""
    state = WorkflowState()
    state.topics_config = {
        "main_topic": "AI in Cancer Care",
        "topics": [
            {"name": "Diagnostics", "description": "AI diagnostics"},
            {"name": "Treatment", "description": "AI treatment planning"}
        ]
    }
    return state


@pytest.fixture
def sample_articles():
    """Create sample articles for testing."""
    return [
        ArticleModel(
            title="Article 1",
            url="https://example.com/1",
            relevance_score=0.9
        ),
        ArticleModel(
            title="Article 2",
            url="https://example.com/2",
            relevance_score=0.7
        )
    ]