# Testing Guide for AI News LangGraph

## Overview

This guide explains how to test the AI News LangGraph implementation following the metamorphosis pattern. The testing strategy includes unit tests, integration tests, and performance benchmarks.

## Test Structure

```
tests/
├── conftest.py           # Shared fixtures and configuration
├── test_state.py         # Unit tests for state models
├── test_prompts.py       # Unit tests for prompt registry
├── test_nodes_v2.py      # Unit tests for workflow nodes
├── test_tools_direct.py  # Unit tests for direct tools
├── test_workflow.py      # Integration tests for workflow
└── test_e2e.py          # End-to-end tests
```

## Running Tests

### Quick Start

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Run all tests
pytest

# Run with coverage
pytest --cov=src/ai_news_langgraph --cov-report=html

# Run specific test file
pytest tests/test_nodes_v2.py

# Run with verbose output
pytest -vv
```

### Using the Test Runner

```bash
# Check test environment
python run_tests.py --check

# Run all test suites with summary
python run_tests.py --all

# Run only unit tests
python run_tests.py --unit

# Run only integration tests
python run_tests.py --integration

# Run with coverage report
python run_tests.py --coverage

# Run tests in parallel (4 workers)
python run_tests.py --parallel 4
```

## Test Categories

### 1. Unit Tests

Test individual components in isolation:

```python
@pytest.mark.unit
class TestWorkflowState:
    def test_add_error(self):
        state = WorkflowState()
        state.add_error("Test error")
        assert len(state.errors) == 1
```

### 2. Integration Tests

Test component interactions:

```python
@pytest.mark.integration
async def test_full_workflow():
    nodes = WorkflowNodesV2()
    state = WorkflowState()

    # Test workflow execution
    state = await nodes.initialize_workflow(state)
    state = await nodes.fetch_news_for_topic(state)
    assert len(state.topic_results) > 0
```

### 3. Performance Tests

Test performance requirements:

```python
@pytest.mark.performance
def test_prompt_compilation_speed(performance_timer):
    performance_timer.start()
    registry = PromptRegistry()
    performance_timer.stop()
    performance_timer.assert_under(1.0)  # Should init in < 1 second
```

## Testing Functions in nodes_v2.py

### 1. Testing Initialization

```python
async def test_initialize_workflow():
    nodes = WorkflowNodesV2()
    state = WorkflowState()

    with patch.object(nodes, '_load_topics_config') as mock_load:
        mock_load.return_value = {"main_topic": "Test", "topics": [...]}
        result = await nodes.initialize_workflow(state)

        assert result.current_stage == "initialized"
        assert result.main_topic == "Test"
```

### 2. Testing News Fetching with Mocks

```python
async def test_fetch_news_for_topic():
    # Create nodes with mocked dependencies
    nodes = WorkflowNodesV2()

    # Mock the news tool
    nodes.news_tool = Mock()
    nodes.news_tool.search = Mock(return_value=[
        {"title": "Article 1", "url": "...", "content": "..."}
    ])

    # Mock relevance analysis
    nodes._analyze_relevance = AsyncMock(return_value=0.85)

    # Test fetching
    state = WorkflowState()
    state.topics_config = {"topics": [{"name": "Test Topic"}]}

    result = await nodes.fetch_news_for_topic(state)
    assert len(result.topic_results) == 1
```

### 3. Testing Summarization

```python
async def test_summarize_topic():
    nodes = WorkflowNodesV2()

    # Mock LLM response
    nodes.llm = AsyncMock()
    nodes.llm.ainvoke = AsyncMock(return_value="Summary text")

    # Mock tool registry
    nodes.tool_registry.execute_tool = Mock(
        return_value=Mock(success=True, output=["Key point"])
    )

    # Create state with articles
    state = WorkflowState()
    state.topic_results = [sample_topic_result]

    result = await nodes.summarize_topic(state)
    assert len(result.topic_summaries) == 1
```

### 4. Testing Quality Review

```python
async def test_review_quality():
    nodes = WorkflowNodesV2()
    state = WorkflowState()
    state.topic_summaries = [sample_summary]

    # Mock quality evaluation
    nodes.llm.ainvoke = AsyncMock(return_value="Quality score: 85")

    result = await nodes.review_quality(state)
    assert result.quality_reviews["average_quality"] > 0
```

## Using Fixtures

### Sample Data Fixtures

```python
def test_with_sample_data(sample_articles, sample_topics):
    # Use pre-configured test data
    assert len(sample_articles) == 3
    assert sample_topics["main_topic"] == "AI in Cancer Care"
```

### Mock Service Fixtures

```python
async def test_with_mocks(mock_llm, mock_news_tool):
    # Use pre-configured mocks
    mock_news_tool.search.return_value = [...]
    result = mock_news_tool.search("test query")
    assert len(result) > 0
```

### Temporary File Fixtures

```python
def test_with_temp_files(temp_config_file, temp_output_dir):
    # Use temporary files for testing
    nodes = WorkflowNodesV2()
    config = nodes._load_topics_config(temp_config_file)
    assert config is not None
```

## Testing Async Functions

### Using pytest-asyncio

```python
@pytest.mark.asyncio
async def test_async_function():
    nodes = WorkflowNodesV2()
    result = await nodes.some_async_method()
    assert result is not None
```

### Testing Concurrent Operations

```python
@pytest.mark.asyncio
async def test_parallel_execution():
    tasks = [
        nodes.fetch_news_for_topic(state1),
        nodes.fetch_news_for_topic(state2)
    ]
    results = await asyncio.gather(*tasks)
    assert len(results) == 2
```

## Mocking Strategies

### 1. Mocking LLM Calls

```python
# Mock specific responses
mock_llm = MagicMock()
mock_llm.ainvoke = AsyncMock(side_effect=[
    "0.95",  # First call returns high relevance
    "0.30",  # Second call returns low relevance
])
```

### 2. Mocking External APIs

```python
# Mock news API responses
with patch('src.ai_news_langgraph.tools.NewsSearchTool.search') as mock:
    mock.return_value = fake_news_data
    result = news_tool.search("query")
```

### 3. Mocking File Operations

```python
# Mock file saving
with patch('src.ai_news_langgraph.tools.FileManager.save_html') as mock:
    mock.return_value = True
    nodes.generate_newsletter(state)
    mock.assert_called_once()
```

## Error Testing

### Testing Error Handling

```python
async def test_error_handling():
    nodes = WorkflowNodesV2()

    # Force an error
    nodes.news_tool.search = Mock(side_effect=Exception("API Error"))

    state = WorkflowState()
    result = await nodes.fetch_news_for_topic(state)

    assert len(result.errors) > 0
    assert "API Error" in result.errors[0]
```

### Testing Validation

```python
def test_validation():
    with pytest.raises(ValidationError):
        ArticleModel(
            title="Test",
            url="invalid-url",  # Invalid URL
            relevance_score=1.5  # Invalid score > 1.0
        )
```

## Performance Testing

### Measuring Execution Time

```python
def test_performance(performance_timer):
    performance_timer.start()

    # Operation to test
    registry = PromptRegistry()
    prompt = registry.get_prompt("research_agent", "analyze_relevance")

    performance_timer.stop()
    performance_timer.assert_under(0.1)  # Should complete in < 100ms
```

### Load Testing

```python
@pytest.mark.performance
async def test_concurrent_load():
    # Test with multiple concurrent requests
    tasks = [nodes.fetch_news_for_topic(state) for _ in range(10)]

    start = time.time()
    await asyncio.gather(*tasks)
    elapsed = time.time() - start

    assert elapsed < 5.0  # Should handle 10 requests in < 5 seconds
```

## Coverage Goals

Aim for these coverage targets:

- **Unit Tests**: 80% coverage of individual functions
- **Integration Tests**: 70% coverage of workflows
- **Critical Paths**: 100% coverage of error handling
- **Edge Cases**: Comprehensive testing of boundaries

## Best Practices

1. **Use Mocks for External Dependencies**
   - Mock LLM calls to avoid API costs
   - Mock file operations to avoid filesystem changes
   - Mock network calls for deterministic tests

2. **Test Both Success and Failure Paths**
   ```python
   async def test_success_and_failure():
       # Test success
       result = await nodes.operation(valid_state)
       assert result.success

       # Test failure
       result = await nodes.operation(invalid_state)
       assert not result.success
   ```

3. **Use Fixtures for Reusable Test Data**
   ```python
   @pytest.fixture
   def standard_test_state():
       return generate_test_state(num_topics=3)
   ```

4. **Test Async Functions Properly**
   ```python
   @pytest.mark.asyncio
   async def test_async():
       result = await async_function()
       assert result is not None
   ```

5. **Isolate Tests**
   - Each test should be independent
   - Use fresh state for each test
   - Clean up resources after tests

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    - name: Run tests
      run: |
        pytest --cov=src/ai_news_langgraph --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

## Debugging Tests

### Using pytest debugging

```bash
# Drop into debugger on failure
pytest --pdb

# Show local variables on failure
pytest -l

# Show print statements
pytest -s

# Maximum verbosity
pytest -vv
```

### Using logging in tests

```python
import logging

def test_with_logging(caplog):
    with caplog.at_level(logging.INFO):
        nodes.some_operation()

    assert "Expected message" in caplog.text
```

## Summary

The testing strategy ensures:
- **Reliability**: Components work as expected
- **Performance**: Operations complete within time limits
- **Error Handling**: Graceful failure recovery
- **Integration**: Components work together correctly
- **Coverage**: All critical paths are tested

Run tests frequently during development to catch issues early!