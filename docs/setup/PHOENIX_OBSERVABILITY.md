# Phoenix Observability for AI News LangGraph

## Overview

This system now includes **Arize Phoenix observability** for comprehensive tracing, monitoring, and debugging of the AI newsletter generation workflow. Phoenix provides deep insights into LLM calls, agent execution, token usage, and performance metrics.

## Features

### 🔍 Complete Tracing
- **LLM Call Tracking**: Every GPT-4o-mini call traced with prompts, responses, tokens
- **Agent Execution Timeline**: Visual timeline of all agent interactions
- **Tool Usage Monitoring**: Track Tavily searches, file operations, and more
- **Knowledge Graph Generation**: Monitor entity extraction and relationship building
- **Glossary Creation**: Track AI definition generation for medical terms

### 📊 Metrics & Analytics
- **Token Usage**: Track total tokens consumed across all agents
- **Cost Tracking**: Real-time cost calculation for API calls
- **Latency Analysis**: Identify slow operations and bottlenecks
- **Success Rates**: Monitor agent success/failure rates
- **Error Tracking**: Detailed error traces with stack traces

### 🎯 Agent-Specific Tracing

| Agent | Traces | Metrics |
|-------|--------|---------|
| **Initializer** | Workflow setup, topic loading | Setup time, topic count |
| **Research Agent** | Article fetching, relevance scoring | Articles found, quality scores |
| **Editor Agent** | Topic summarization, COSTAR prompts | Summary quality, token usage |
| **Quality Reviewer** | Quality assessment, feedback | Review scores, improvement suggestions |
| **Chief Editor** | Newsletter generation, KG/glossary | Generation time, output size |

## Installation

### 1. Dependencies Already Added

The required dependencies are in `pyproject.toml`:
```toml
"arize-phoenix[llama-index]>=4.0.0",
"openinference-instrumentation-langchain>=0.1.0",
"opentelemetry-api>=1.20.0",
"opentelemetry-sdk>=1.20.0",
"opentelemetry-exporter-otlp>=1.20.0",
```

### 2. Install Dependencies

```bash
# Install with pip
pip install -e .

# Or install Phoenix separately
pip install "arize-phoenix[llama-index]" openinference-instrumentation-langchain
```

## Quick Start

### Launch Phoenix Dashboard

```bash
# Basic launch
python phoenix_dashboard.py

# Custom port
python phoenix_dashboard.py --port 7007

# Without auto-opening browser
python phoenix_dashboard.py --no-browser

# With trace export
python phoenix_dashboard.py --export

# With test workflow
python phoenix_dashboard.py --test
```

### Dashboard Access

Once launched, the dashboard is available at:
```
http://localhost:6006
```

## Integration with Workflow

### Automatic Tracing

All workflow nodes are automatically traced with the `@trace_node` decorator:

```python
@trace_node("research_agent")
async def fetch_news_for_topic(self, state: dict) -> dict:
    # Agent logic here
    pass
```

### What Gets Traced

1. **Workflow Initialization**
   - Topic configuration loading
   - State setup
   - Environment validation

2. **Research Phase**
   - Tavily/Serper API calls
   - Article fetching
   - Relevance scoring
   - Quality assessment

3. **Summarization**
   - COSTAR prompt usage
   - GPT-4o-mini calls
   - Token consumption
   - Response quality

4. **Knowledge Graph**
   - Entity extraction
   - Relationship building
   - Centrality calculations
   - Export operations

5. **Glossary Generation**
   - Term selection
   - AI definition generation
   - Related term linking

6. **Newsletter Creation**
   - HTML generation
   - Visualization creation
   - Cover image generation (DALL-E + Flux)
   - Final assembly

## Using the Dashboard

### Main Views

1. **Traces View**
   - Timeline of all operations
   - Nested span hierarchy
   - Duration visualization
   - Error highlighting

2. **LLM View**
   - All LLM calls
   - Prompt/response pairs
   - Token usage
   - Cost breakdown

3. **Metrics View**
   - Success rates
   - Latency percentiles
   - Token consumption trends
   - Cost analysis

### Filtering & Search

- **Filter by Agent**: `agent.name:research_agent`
- **Filter by Task**: `agent.task:fetch_news`
- **Error Only**: `status:error`
- **High Latency**: `duration_ms>5000`

## Programmatic Usage

### Initialize in Code

```python
from src.ai_news_langgraph.observability import initialize_phoenix

# Start observability
observer = initialize_phoenix(
    project_name="AI-News-LangGraph",
    port=6006
)

# Run your workflow
workflow = WorkflowExecutor()
result = await workflow.execute(initial_state)

# Get metrics
metrics = observer.get_metrics_summary()
print(f"Total API Calls: {metrics['total_requests']}")
print(f"Success Rate: {metrics['success_rate']}%")
print(f"Total Cost: ${metrics['total_cost']}")

# Export traces
observer.export_traces("traces.json")
```

### Custom Tracing

```python
from src.ai_news_langgraph.observability import phoenix_observer

# Trace custom operation
with phoenix_observer.trace_agent(
    agent_name="custom_agent",
    task="special_operation",
    custom_field="value"
):
    # Your code here
    result = perform_operation()

# Trace LLM call
phoenix_observer.trace_llm_call(
    model="gpt-4o-mini",
    prompt="Your prompt",
    response="Model response",
    tokens_used=150,
    cost=0.003
)

# Trace tool usage
phoenix_observer.trace_tool_use(
    tool_name="tavily_search",
    input_data={"query": "AI cancer research"},
    output_data={"articles": [...]}
)
```

## Metrics Collected

### System Metrics
- **Total Requests**: All API calls made
- **Success Rate**: Percentage of successful operations
- **Total Tokens**: Cumulative token usage
- **Total Cost**: Estimated cost in USD
- **Average Latency**: Mean operation time

### Agent Metrics
For each agent:
- **Call Count**: Number of invocations
- **Success Rate**: Agent-specific success percentage
- **Average Duration**: Mean execution time
- **Token Usage**: Agent-specific token consumption
- **Error Count**: Number of failures

### Workflow Metrics
- **Topics Processed**: Number of research topics
- **Articles Analyzed**: Total articles fetched
- **Summaries Generated**: Number of topic summaries
- **Average Quality Score**: Mean quality across summaries
- **Knowledge Graph Size**: Entities and relationships
- **Glossary Terms**: Number of terms with AI definitions

## Export & Analysis

### Export Traces

```bash
# Export via dashboard
python phoenix_dashboard.py --export

# Programmatic export
observer.export_traces("traces_20251019.json")
```

### Trace Format

```json
{
  "exported_at": "2025-10-19T12:34:56",
  "metrics": {
    "total_requests": 45,
    "success_rate": 95.6,
    "total_tokens": 12500,
    "total_cost": 0.0875
  },
  "spans": [
    {
      "name": "research_agent.fetch_news",
      "duration_ms": 2340,
      "status": "OK",
      "attributes": {
        "agent.name": "research_agent",
        "agent.task": "fetch_news",
        "topic": "Cancer Research",
        "articles_found": 12
      }
    }
  ]
}
```

## Troubleshooting

### Phoenix Not Starting

```bash
# Check if port is in use
lsof -i :6006

# Kill existing process
kill -9 $(lsof -t -i:6006)

# Try different port
python phoenix_dashboard.py --port 7007
```

### No Traces Appearing

1. Verify Phoenix is initialized:
```python
from src.ai_news_langgraph.observability import phoenix_observer
print(phoenix_observer.initialized)  # Should be True
```

2. Check instrumentation:
```python
# Should see LangChain/OpenAI instrumentation messages
```

3. Run test workflow:
```bash
python phoenix_dashboard.py --test
```

### High Memory Usage

Phoenix stores traces in memory. For long sessions:
1. Export traces periodically
2. Restart Phoenix dashboard
3. Use remote OTLP endpoint for production

## Performance Impact

### Overhead
- **Latency**: ~1-2ms per traced operation
- **Memory**: ~100KB per trace
- **CPU**: < 1% additional usage

### Optimization
- Disable in production: Set `PHOENIX_ENABLED=false`
- Sample traces: Reduce trace frequency
- Remote export: Use OTLP for cloud storage

## Advanced Configuration

### Remote Tracing

```python
# For production with remote backend
observer = initialize_phoenix(
    enable_remote=True,
    remote_endpoint="https://your-otlp-endpoint.com:4317"
)
```

### Custom Span Processors

```python
from opentelemetry.sdk.trace.export import ConsoleSpanExporter

# Add console output
provider.add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
```

## Integration with Streamlit

The Phoenix observability works seamlessly with the Streamlit app:

```python
# In streamlit_newsletter_app.py
from src.ai_news_langgraph.observability import initialize_phoenix

# Start observability when app loads
if 'phoenix_initialized' not in st.session_state:
    initialize_phoenix()
    st.session_state.phoenix_initialized = True
```

## Best Practices

### 1. Start Phoenix Before Workflow
```bash
# Terminal 1: Start Phoenix
python phoenix_dashboard.py

# Terminal 2: Run workflow
streamlit run streamlit_newsletter_app.py
```

### 2. Export Important Traces
After significant runs, export traces for analysis:
```python
observer.export_traces(f"traces_{datetime.now()}.json")
```

### 3. Monitor Cost
Keep track of API costs through metrics:
```python
metrics = observer.get_metrics_summary()
if metrics['total_cost'] > 1.0:
    logger.warning(f"High cost alert: ${metrics['total_cost']}")
```

### 4. Use Filters
Focus on specific agents or errors:
- Agent traces: `agent.name:research_agent`
- Errors only: `status:ERROR`
- Slow operations: `duration_ms>10000`

## Summary

Phoenix observability provides:
- ✅ **Complete visibility** into AI newsletter generation
- ✅ **Real-time monitoring** of all LLM operations
- ✅ **Cost tracking** for budget management
- ✅ **Performance insights** for optimization
- ✅ **Error tracking** for debugging
- ✅ **Knowledge graph & glossary metrics**

Launch the dashboard to start monitoring:
```bash
python phoenix_dashboard.py
```

Visit: **http://localhost:6006** 🚀

## Note on Replicate/Flux

The Replicate credit error you encountered is normal for new accounts. Options:
1. **Add credits**: Go to https://replicate.com/account/billing
2. **Use free tier**: Some models have limited free usage
3. **Skip Flux**: System falls back to DALL-E gracefully
4. **Manual generation**: Use saved prompts on CivitAI

The Phoenix observability will track both successful DALL-E generation and Flux failures, giving you complete visibility into image generation performance.