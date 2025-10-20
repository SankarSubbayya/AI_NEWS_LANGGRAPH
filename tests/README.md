# 🧪 Test Suite

Comprehensive test suite for the AI News LangGraph system.

## Test Files

### Core Tests
- **`test_nodes_v2.py`** - Tests for workflow nodes (fetch, summarize, review, generate)
- **`test_state.py`** - State management and TypedDict tests
- **`test_prompts.py`** - Prompt loading and template tests

### Feature Tests
- **`test_costar_prompts.py`** - COSTAR prompt framework tests
- **`test_new_features.py`** - HTML generation and visualization tests
- **`test_metamorphosis.py`** - Refactoring validation tests

### Configuration
- **`conftest.py`** - Pytest fixtures and shared test configuration
- **`run_tests.py`** - Test runner script

---

## Running Tests

### Run All Tests
```bash
# From project root
pytest tests/

# With verbose output
pytest tests/ -v

# With coverage report
pytest tests/ --cov=ai_news_langgraph --cov-report=html
```

### Run Specific Test File
```bash
pytest tests/test_nodes_v2.py
pytest tests/test_costar_prompts.py
```

### Run Specific Test Function
```bash
pytest tests/test_nodes_v2.py::test_fetch_news_for_topic
pytest tests/test_prompts.py::test_load_costar_prompts
```

### Run Tests by Marker
```bash
# Run only fast tests
pytest tests/ -m "not slow"

# Run only integration tests
pytest tests/ -m integration
```

---

## Test Coverage

Current test coverage by module:

- ✅ `nodes_v2.py` - Core workflow nodes
- ✅ `state.py` - State management
- ✅ `prompts.py` - Prompt system
- ✅ `costar_prompts.py` - COSTAR framework
- ✅ `html_generator.py` - HTML generation
- ✅ `visualizations.py` - Chart generation
- 🟡 `graph_v2.py` - Workflow orchestration (partial)
- 🟡 `tools.py` - External tools (partial)

---

## Writing New Tests

### Test Structure

```python
import pytest
from ai_news_langgraph.nodes_v2 import WorkflowNodes

def test_your_feature():
    """Test description."""
    # Arrange
    nodes = WorkflowNodes()
    state = {"key": "value"}
    
    # Act
    result = nodes.your_method(state)
    
    # Assert
    assert result["status"] == "success"
```

### Using Fixtures

```python
def test_with_fixture(sample_state, mock_llm):
    """Test using pytest fixtures."""
    nodes = WorkflowNodes(llm=mock_llm)
    result = nodes.process(sample_state)
    assert result is not None
```

### Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async functionality."""
    result = await async_function()
    assert result is not None
```

---

## Test Fixtures

Available fixtures in `conftest.py`:

### State Fixtures
- `empty_state()` - Empty workflow state
- `sample_state()` - State with sample data
- `state_with_articles()` - State with articles
- `state_with_summaries()` - State with topic summaries

### Mock Fixtures
- `mock_llm()` - Mock language model
- `mock_search_tool()` - Mock search API
- `mock_prompts()` - Mock prompt loader

### Config Fixtures
- `test_config()` - Test configuration
- `temp_output_dir()` - Temporary output directory

---

## Test Categories

### Unit Tests
Test individual functions in isolation:
```python
def test_parse_article():
    """Test article parsing logic."""
    article = parse_article(raw_data)
    assert article.title is not None
```

### Integration Tests
Test component interactions:
```python
@pytest.mark.integration
def test_full_workflow():
    """Test complete workflow execution."""
    result = run_workflow(config)
    assert result["status"] == "completed"
```

### Smoke Tests
Quick validation tests:
```python
@pytest.mark.smoke
def test_imports():
    """Test all imports work."""
    from ai_news_langgraph import nodes_v2
    assert nodes_v2 is not None
```

---

## Mocking External APIs

### Mock OpenAI
```python
from unittest.mock import Mock, patch

@patch('openai.ChatCompletion.create')
def test_with_mock_openai(mock_create):
    mock_create.return_value = {"choices": [{"text": "response"}]}
    result = call_openai()
    assert result is not None
```

### Mock Search APIs
```python
@patch('ai_news_langgraph.tools.NewsSearchTool.search')
def test_with_mock_search(mock_search):
    mock_search.return_value = [{"title": "Article"}]
    result = fetch_news()
    assert len(result) > 0
```

---

## Continuous Integration

### GitHub Actions
Tests run automatically on:
- Push to main branch
- Pull requests
- Scheduled nightly builds

### Pre-commit Hooks
```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

---

## Debugging Tests

### Run with Debugging
```bash
# Drop into debugger on failure
pytest tests/ --pdb

# Show print statements
pytest tests/ -s

# Show local variables on failure
pytest tests/ -l
```

### Verbose Output
```bash
# Maximum verbosity
pytest tests/ -vv

# Show test durations
pytest tests/ --durations=10
```

---

## Test Performance

### Current Stats
- Total tests: ~25
- Average duration: ~15 seconds
- Success rate: >95%

### Slow Tests
Mark slow tests to skip during development:
```python
@pytest.mark.slow
def test_full_workflow():
    """This test takes a while."""
    pass

# Skip slow tests
pytest tests/ -m "not slow"
```

---

## Code Coverage

### Generate Coverage Report
```bash
# HTML report
pytest tests/ --cov=ai_news_langgraph --cov-report=html

# Terminal report
pytest tests/ --cov=ai_news_langgraph --cov-report=term

# XML report (for CI)
pytest tests/ --cov=ai_news_langgraph --cov-report=xml
```

### View Coverage
```bash
# Open HTML report
open htmlcov/index.html
```

---

## Best Practices

### ✅ Do
- Write tests for new features
- Keep tests independent
- Use descriptive test names
- Mock external dependencies
- Test edge cases
- Add docstrings

### ❌ Don't
- Make tests depend on each other
- Use real API keys in tests
- Write tests that require manual setup
- Test implementation details
- Ignore failing tests

---

## Troubleshooting

### Import Errors
```bash
# Ensure package is installed
pip install -e .

# Check Python path
python -c "import ai_news_langgraph; print(ai_news_langgraph.__file__)"
```

### Fixture Not Found
```bash
# Check conftest.py is present
ls tests/conftest.py

# Run with fixture discovery
pytest tests/ --fixtures
```

### Async Test Issues
```bash
# Install pytest-asyncio
pip install pytest-asyncio

# Check marker is present
@pytest.mark.asyncio
```

---

## Contributing

When adding new tests:

1. Place in appropriate test file
2. Use existing fixtures when possible
3. Add new fixtures to `conftest.py`
4. Mark slow tests with `@pytest.mark.slow`
5. Document expected behavior
6. Ensure tests pass locally

---

## Quick Commands

```bash
# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=ai_news_langgraph

# Verbose
pytest tests/ -v

# Stop on first failure
pytest tests/ -x

# Run last failed
pytest tests/ --lf

# Show slowest tests
pytest tests/ --durations=5
```

---

**Happy Testing! 🧪**



