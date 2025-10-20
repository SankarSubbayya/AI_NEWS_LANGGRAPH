# Tasks Configuration Guide

This guide explains how tasks.yaml works in the AI News LangGraph system and how it bridges CrewAI-style declarative task definitions with LangGraph's imperative workflow execution.

## 📋 Overview

**Tasks** in this system represent discrete units of work performed by agents. Unlike CrewAI which automatically orchestrates tasks from YAML, LangGraph requires explicit implementation, but we maintain tasks.yaml for:

1. **Documentation** - Clear description of what each task does
2. **Configuration** - Timeout, retry, and dependency metadata
3. **Mapping** - Links YAML tasks to Python node functions
4. **Validation** - Ensures dependencies are correct

## 🗂️ File Structure

```
src/ai_news_langgraph/
├── config/
│   └── tasks.yaml           # Task definitions & configuration
├── task_loader.py           # Utility to load tasks
├── graph.py                 # Node functions that implement tasks
└── agents.py                # Agents that perform the work
```

## 📝 Task Configuration Format

### Basic Structure

```yaml
task_name:
  node_function: "python_function_name"  # LangGraph node in graph.py
  description: |
    What this task does in detail
  expected_output: |
    What this task produces
  agent: agent_name            # Agent from agents.yaml
  agent_class: "ClassName"     # Python class in agents.py
  dependencies:
    - prerequisite_task_1
    - prerequisite_task_2
  timeout_seconds: 300         # Max execution time
  retry_count: 2               # Number of retry attempts
  output_file: outputs/file.ext
```

### Current Tasks

| Task Name | Node Function | Agent | Purpose |
|-----------|---------------|-------|---------|
| `fetch_ai_news` | `fetch_news_for_topic` | ResearchAgent | Search for AI news articles |
| `summarize_ai_news` | `summarize_topic_news` | EditorAgent | Create summaries and insights |
| `draft_html_newsletter` | `generate_newsletter` | ChiefEditorAgent | Generate HTML newsletter |
| `finalize_html_newsletter` | `generate_newsletter` | ChiefEditorAgent | Finalize newsletter (merged) |
| `generate_markdown_report` | `generate_newsletter` | ChiefEditorAgent | Generate MD report |

## 🔧 Using TaskLoader

### Method 1: Load Task Configuration

```python
from ai_news_langgraph.task_loader import load_task_config

# Get task configuration
config = load_task_config('fetch_ai_news')

print(f"Task: {config.name}")
print(f"Description: {config.description}")
print(f"Agent: {config.agent}")
print(f"Timeout: {config.timeout_seconds}s")
print(f"Retry: {config.retry_count} attempts")
print(f"Dependencies: {config.dependencies}")
```

### Method 2: Use TaskLoader Class

```python
from ai_news_langgraph.task_loader import get_task_loader

loader = get_task_loader()

# List all tasks
tasks = loader.list_tasks()
print(f"Available tasks: {tasks}")

# Get execution order (respects dependencies)
order = loader.get_execution_order()
print(f"Execution order: {order}")
# Output: ['fetch_ai_news', 'summarize_ai_news', 'draft_html_newsletter', ...]

# Validate dependencies
issues = loader.validate_dependencies()
if not issues:
    print("✅ All dependencies are valid")

# Get node function name
node_func = loader.get_node_function('fetch_ai_news')
print(f"Node function: {node_func}")  # 'fetch_news_for_topic'
```

### Method 3: Task Metadata Decorator

```python
from ai_news_langgraph.task_loader import task_metadata

@task_metadata('fetch_ai_news')
def fetch_news_for_topic(state):
    """Fetch AI news articles."""
    # Implementation
    return state

# When called, prints:
# 📋 Task: fetch_ai_news
#    Agent: research_assistant
#    Description: Search the web for recent AI agent news...
#    ✅ Completed in 45.23s
```

## 🎯 How Tasks Map to LangGraph

### CrewAI Approach (Automatic)

```yaml
# tasks.yaml
fetch_ai_news:
  agent: research_assistant
  dependencies: []

summarize_ai_news:
  agent: editor_assistant
  dependencies: [fetch_ai_news]  # ← CrewAI handles this automatically
```

CrewAI reads this and **automatically executes** tasks in dependency order.

### LangGraph Approach (Explicit)

```python
# graph.py
def build_multi_agent_graph():
    graph = StateGraph(ResearchState)
    
    # Add nodes (tasks)
    graph.add_node("fetch", fetch_news_for_topic)
    graph.add_node("summarize", summarize_topic_news)
    
    # Define flow (dependencies)
    graph.add_edge("fetch", "summarize")  # ← You control flow explicitly
    
    return graph.compile()
```

### Hybrid Approach (This Project)

We maintain `tasks.yaml` for **documentation and configuration**, but implement tasks as **LangGraph node functions**:

```yaml
# tasks.yaml - Documentation & Config
fetch_ai_news:
  node_function: "fetch_news_for_topic"  # ← Links to Python function
  timeout_seconds: 300
  retry_count: 2
```

```python
# graph.py - Implementation
def fetch_news_for_topic(state: ResearchState) -> ResearchState:
    """
    Task: fetch_ai_news (see config/tasks.yaml)
    
    Research agent fetches AI news articles for current topic.
    """
    config = load_task_config('fetch_ai_news')  # Optional: load config
    
    # Implementation
    research_agent = ResearchAgent()
    # ... search logic
    
    return state
```

## 📊 Task Execution Flow

```
tasks.yaml
    │
    ├─ defines: fetch_ai_news
    │           ├─ timeout: 300s
    │           ├─ retry: 2
    │           └─ node_function: "fetch_news_for_topic"
    │
    ▼
graph.py
    │
    ├─ implements: fetch_news_for_topic(state)
    │              ├─ Uses ResearchAgent
    │              ├─ Searches for articles
    │              └─ Returns updated state
    │
    ▼
LangGraph Execution
    │
    └─ Runs node functions in graph order
       (not by tasks.yaml dependencies)
```

## 🔄 Task Dependencies

### Defined in tasks.yaml

```yaml
fetch_ai_news:
  dependencies: []  # No prerequisites

summarize_ai_news:
  dependencies:
    - fetch_ai_news  # Must run after fetch

draft_html_newsletter:
  dependencies:
    - summarize_ai_news  # Must run after summarize
```

### Implemented in graph.py

```python
# graph.py
graph.add_edge("initialize", "fetch_news")
graph.add_edge("fetch_news", "summarize")
graph.add_edge("summarize", "generate")

# This creates the flow:
# initialize → fetch_news → summarize → generate
```

**Important**: The graph edges define the **actual execution flow**. The dependencies in tasks.yaml are for **documentation and validation**.

## 🛡️ Task Execution with Timeout & Retry

### Using TaskExecutor

```python
from ai_news_langgraph.task_loader import TaskExecutor

executor = TaskExecutor()

def my_task_function(state):
    # Your task logic
    return state

# Execute with automatic timeout and retry from tasks.yaml
try:
    result = executor.execute_with_config(
        'fetch_ai_news',  # Task name for config lookup
        my_task_function,  # Function to execute
        state  # Arguments
    )
except TimeoutError:
    print("Task timed out after configured timeout")
except Exception as e:
    print(f"Task failed after {config.retry_count} retries: {e}")
```

### Manual Timeout/Retry

```python
import time

def fetch_news_with_retry(state):
    config = load_task_config('fetch_ai_news')
    
    for attempt in range(config.retry_count):
        try:
            # Your logic here
            result = perform_search()
            return result
        except Exception as e:
            if attempt < config.retry_count - 1:
                print(f"Retry {attempt + 1}/{config.retry_count}")
                time.sleep(2)
            else:
                raise
```

## 📚 Task Validation

### Validate Dependencies

```python
from ai_news_langgraph.task_loader import get_task_loader

loader = get_task_loader()

# Check for missing dependencies
issues = loader.validate_dependencies()

if issues:
    print("❌ Dependency issues:")
    for task, missing_deps in issues.items():
        print(f"  {task} depends on non-existent tasks: {missing_deps}")
else:
    print("✅ All dependencies are valid")
```

### Get Execution Order

```python
# Get tasks in topological order (respecting dependencies)
execution_order = loader.get_execution_order()

print("Recommended execution order:")
for i, task in enumerate(execution_order, 1):
    print(f"{i}. {task}")

# Output:
# 1. fetch_ai_news
# 2. summarize_ai_news
# 3. draft_html_newsletter
# 4. finalize_html_newsletter
# 5. generate_markdown_report
```

## 🎓 Best Practices

### 1. Keep tasks.yaml Synchronized

When you add a new node function in `graph.py`, add corresponding entry in `tasks.yaml`:

```yaml
your_new_task:
  node_function: "your_node_function"
  description: "What it does"
  agent: agent_name
  dependencies: []
  timeout_seconds: 180
  retry_count: 2
```

### 2. Use Descriptive Task Names

❌ Bad:
```yaml
task1:
  description: "Do stuff"
```

✅ Good:
```yaml
fetch_ai_news:
  description: |
    Search the web for recent AI agent news in cancer care
    across 5 topics using Tavily API and medical domains.
```

### 3. Document Dependencies

Even though LangGraph uses graph edges, document dependencies in tasks.yaml for clarity:

```yaml
summarize_ai_news:
  dependencies:
    - fetch_ai_news  # Needs articles before summarizing
```

### 4. Reference Tasks in Docstrings

```python
def fetch_news_for_topic(state: ResearchState) -> ResearchState:
    """
    Task: fetch_ai_news (see config/tasks.yaml)
    
    Research agent fetches AI news articles for current topic.
    """
    # Implementation
```

### 5. Use Task Metadata for Logging

```python
from ai_news_langgraph.task_loader import load_task_config

def fetch_news_for_topic(state):
    config = load_task_config('fetch_ai_news')
    
    print(f"🚀 Starting task: {config.name}")
    print(f"   Agent: {config.agent}")
    print(f"   Timeout: {config.timeout_seconds}s")
    
    # Implementation
```

## 🔍 Troubleshooting

### Error: Task not found

```python
KeyError: "Task 'my_task' not found in configuration"
```

**Solution**: Check that the task name exists in `tasks.yaml`:

```bash
$ grep "my_task:" src/ai_news_langgraph/config/tasks.yaml
```

### Error: Missing dependencies

```python
# Validation shows missing dependencies
issues = loader.validate_dependencies()
# {'my_task': ['non_existent_task']}
```

**Solution**: Either:
1. Add the missing task to tasks.yaml
2. Remove the invalid dependency

### Reload tasks after changes

```python
loader = get_task_loader()
loader.reload()  # Reloads from tasks.yaml
```

## 🆚 Comparison: CrewAI vs LangGraph Tasks

| Aspect | CrewAI | This Project (LangGraph) |
|--------|--------|---------------------------|
| **Task Definition** | YAML only | YAML + Python functions |
| **Execution** | Auto from YAML | Manual graph construction |
| **Dependencies** | Auto-orchestrated | Defined via graph edges |
| **Control Flow** | Sequential/automatic | Full control (conditional, loops) |
| **Error Handling** | Limited | Full Python exception handling |
| **State Management** | Hidden | Explicit TypedDict |
| **Debugging** | Harder | Easier (standard Python) |
| **Flexibility** | Limited | Very flexible |

## 📖 Example: Complete Task Workflow

```python
from ai_news_langgraph.task_loader import get_task_loader, load_task_config

# 1. Load and validate tasks
loader = get_task_loader()
print(f"Tasks: {loader.list_tasks()}")

# 2. Validate dependencies
issues = loader.validate_dependencies()
assert not issues, f"Dependency issues: {issues}"

# 3. Get execution order
order = loader.get_execution_order()
print(f"Execution order: {order}")

# 4. Load specific task config
fetch_config = load_task_config('fetch_ai_news')
print(f"Timeout: {fetch_config.timeout_seconds}s")

# 5. Implement task (in graph.py)
def fetch_news_for_topic(state):
    config = load_task_config('fetch_ai_news')
    
    print(f"📋 Task: {config.name}")
    print(f"   Description: {config.description[:100]}...")
    
    # Your implementation here
    research_agent = ResearchAgent()
    # ...
    
    return state

# 6. Build graph with task
from langgraph.graph import StateGraph

graph = StateGraph(ResearchState)
graph.add_node("fetch", fetch_news_for_topic)
# ... more nodes
```

## 🚀 Advanced: Auto-Generate Documentation

```python
from ai_news_langgraph.task_loader import get_task_loader

def generate_task_documentation():
    """Generate markdown documentation from tasks.yaml"""
    loader = get_task_loader()
    
    output = "# Task Documentation\n\n"
    
    for task_name in loader.list_tasks():
        config = loader.get_task_config(task_name)
        node = loader.get_node_function(task_name)
        
        output += f"## {task_name}\n\n"
        output += f"- **Node Function**: `{node}()`\n"
        output += f"- **Agent**: {config.agent}\n"
        output += f"- **Timeout**: {config.timeout_seconds}s\n"
        output += f"- **Retry**: {config.retry_count} attempts\n"
        output += f"- **Dependencies**: {config.dependencies}\n\n"
        output += f"### Description\n\n{config.description}\n\n"
        output += f"### Expected Output\n\n{config.expected_output}\n\n"
        output += "---\n\n"
    
    return output

# Generate and save
doc = generate_task_documentation()
with open("TASK_DOCUMENTATION.md", "w") as f:
    f.write(doc)
```

---

For more information, see:
- [CREWAI_VS_LANGGRAPH.md](./CREWAI_VS_LANGGRAPH.md) - Framework comparison
- [ARCHITECTURE.md](./ARCHITECTURE.md) - System architecture
- [PROMPTS_GUIDE.md](./PROMPTS_GUIDE.md) - Prompt management


