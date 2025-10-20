"""
Unit tests for PromptRegistry and prompt management.
"""

import pytest
from unittest.mock import Mock, patch
import tempfile
import yaml

from src.ai_news_langgraph.prompts import (
    PromptConfig,
    PromptRegistry,
    PromptOptimizer,
    get_prompt
)


class TestPromptConfig:
    """Test PromptConfig dataclass."""

    def test_prompt_config_creation(self):
        """Test creating a prompt configuration."""
        config = PromptConfig(
            name="test_prompt",
            description="Test prompt for unit testing",
            system_template="You are a test assistant.",
            human_template="Process this: {input}",
            variables=["input"],
            output_format="text"
        )

        assert config.name == "test_prompt"
        assert config.description == "Test prompt for unit testing"
        assert "{input}" in config.human_template
        assert "input" in config.variables

    def test_prompt_config_with_examples(self):
        """Test prompt config with examples."""
        examples = [
            {"input": "test1", "output": "result1"},
            {"input": "test2", "output": "result2"}
        ]

        config = PromptConfig(
            name="test_with_examples",
            description="Test",
            system_template="System",
            human_template="Human: {input}",
            variables=["input"],
            examples=examples
        )

        assert len(config.examples) == 2
        assert config.examples[0]["input"] == "test1"


class TestPromptRegistry:
    """Test PromptRegistry functionality."""

    @pytest.fixture
    def registry(self):
        """Create a fresh registry for testing."""
        return PromptRegistry()

    def test_registry_initialization(self, registry):
        """Test that registry initializes with default prompts."""
        # Check that default prompts are loaded
        prompts = registry.list_prompts()

        assert "research_agent" in prompts
        assert "editor_agent" in prompts
        assert "chief_editor" in prompts
        assert "self_reviewer" in prompts

        # Check specific prompts
        research_prompts = prompts["research_agent"]
        assert "analyze_relevance" in research_prompts
        assert "extract_key_facts" in research_prompts

    def test_register_custom_prompt(self, registry):
        """Test registering a custom prompt."""
        config = PromptConfig(
            name="custom_prompt",
            description="Custom test prompt",
            system_template="You are a custom assistant.",
            human_template="Process: {data}",
            variables=["data"]
        )

        registry.register_prompt("test_agent", "custom_prompt", config)

        # Verify prompt was registered
        prompts = registry.list_prompts("test_agent")
        assert "custom_prompt" in prompts["test_agent"]

        # Get the prompt
        prompt = registry.get_prompt("test_agent", "custom_prompt")
        assert prompt is not None

    def test_get_prompt(self, registry):
        """Test retrieving a prompt."""
        prompt = registry.get_prompt("research_agent", "analyze_relevance")

        assert prompt is not None
        # Check it's a ChatPromptTemplate
        assert hasattr(prompt, 'format_messages')

    def test_get_nonexistent_prompt(self, registry):
        """Test getting a non-existent prompt raises error."""
        with pytest.raises(ValueError) as exc_info:
            registry.get_prompt("nonexistent_agent", "nonexistent_prompt")

        assert "not found" in str(exc_info.value)

    def test_get_prompt_config(self, registry):
        """Test retrieving prompt configuration."""
        config = registry.get_prompt_config("research_agent", "analyze_relevance")

        assert config.name == "analyze_relevance"
        assert config.description == "Analyze article relevance to topic"
        assert "topic_name" in config.variables

    def test_list_prompts_by_agent(self, registry):
        """Test listing prompts filtered by agent."""
        prompts = registry.list_prompts("editor_agent")

        assert "editor_agent" in prompts
        assert "summarize_topic" in prompts["editor_agent"]
        assert "research_agent" not in prompts

    def test_load_from_yaml(self, registry):
        """Test loading prompts from YAML file."""
        # Create a temporary YAML file
        yaml_content = """
test_agent:
  test_prompt:
    description: "Test prompt from YAML"
    system: "You are a test system."
    human: "Process: {input}"
    variables:
      - input
    output_format: "json"
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(yaml_content)
            yaml_path = f.name

        try:
            # Load from YAML
            registry.load_from_yaml(yaml_path)

            # Verify prompt was loaded
            config = registry.get_prompt_config("test_agent", "test_prompt")
            assert config.description == "Test prompt from YAML"
            assert config.output_format == "json"

        finally:
            import os
            os.unlink(yaml_path)

    def test_compiled_prompt_format(self, registry):
        """Test that compiled prompts have correct format."""
        prompt = registry.get_prompt("research_agent", "analyze_relevance")

        # Test formatting with variables
        messages = prompt.format_messages(
            topic_name="AI Diagnostics",
            topic_description="AI in medical diagnostics",
            title="Test Article",
            content="Article content here"
        )

        assert len(messages) >= 2  # System and Human messages
        assert "AI Diagnostics" in messages[-1].content  # Human message


class TestPromptOptimizer:
    """Test PromptOptimizer functionality."""

    @pytest.fixture
    def optimizer(self):
        """Create optimizer with registry."""
        registry = PromptRegistry()
        return PromptOptimizer(registry)

    def test_optimizer_initialization(self, optimizer):
        """Test optimizer initializes correctly."""
        assert optimizer.registry is not None

    def test_add_few_shot_examples(self, optimizer):
        """Test adding few-shot examples to a prompt."""
        examples = [
            {
                "input": "Sample article about AI",
                "output": "0.85"
            },
            {
                "input": "Unrelated article",
                "output": "0.2"
            }
        ]

        optimizer.add_few_shot_examples(
            "research_agent",
            "analyze_relevance",
            examples
        )

        # Verify examples were added
        config = optimizer.registry.get_prompt_config(
            "research_agent",
            "analyze_relevance"
        )
        assert config.examples == examples

    def test_optimize_prompt_placeholder(self, optimizer):
        """Test optimize_prompt method (placeholder implementation)."""
        test_cases = [
            {"input": "test", "expected": "result"}
        ]

        # This is a placeholder test since optimize_prompt is not fully implemented
        config = optimizer.optimize_prompt(
            "research_agent",
            "analyze_relevance",
            test_cases
        )

        assert config is not None
        assert config.name == "analyze_relevance"


class TestGlobalRegistry:
    """Test global registry and convenience functions."""

    def test_global_get_prompt(self):
        """Test using the global get_prompt function."""
        prompt = get_prompt("research_agent", "analyze_relevance")

        assert prompt is not None
        # Verify it's a proper prompt template
        messages = prompt.format_messages(
            topic_name="Test",
            topic_description="Test desc",
            title="Title",
            content="Content"
        )
        assert len(messages) >= 1


class TestPromptContent:
    """Test the actual content of key prompts."""

    @pytest.fixture
    def registry(self):
        """Create a registry for testing."""
        return PromptRegistry()

    def test_research_agent_prompts(self, registry):
        """Test research agent prompt content."""
        config = registry.get_prompt_config("research_agent", "analyze_relevance")

        # Check system template
        assert "AI Research Analyst" in config.system_template
        assert "cancer care" in config.system_template.lower()

        # Check human template
        assert "relevance" in config.human_template.lower()
        assert "{topic_name}" in config.human_template
        assert "0.0 and 1.0" in config.human_template

    def test_editor_agent_prompts(self, registry):
        """Test editor agent prompt content."""
        config = registry.get_prompt_config("editor_agent", "summarize_topic")

        # Check role definition
        assert "Medical Editor" in config.system_template
        assert "oncology" in config.system_template.lower()

        # Check output requirements
        assert "Overview" in config.human_template
        assert "Key Findings" in config.human_template
        assert "200-250 word" in config.human_template

    def test_self_reviewer_prompts(self, registry):
        """Test self-reviewer prompt content."""
        config = registry.get_prompt_config("self_reviewer", "evaluate_quality")

        # Check quality criteria
        assert "Quality Assurance" in config.system_template
        assert "Scientific Accuracy" in config.human_template
        assert "0-100" in config.human_template or "0-25" in config.human_template


# Performance tests
@pytest.mark.performance
class TestPromptPerformance:
    """Performance tests for prompt operations."""

    def test_prompt_compilation_speed(self):
        """Test that prompt compilation is fast."""
        import time

        registry = PromptRegistry()
        start = time.time()

        # Get 100 prompts
        for _ in range(100):
            prompt = registry.get_prompt("research_agent", "analyze_relevance")

        elapsed = time.time() - start
        assert elapsed < 0.1  # Should be very fast due to caching

    def test_registry_initialization_speed(self):
        """Test that registry initialization is reasonable."""
        import time

        start = time.time()
        registry = PromptRegistry()
        elapsed = time.time() - start

        assert elapsed < 1.0  # Should initialize in under 1 second