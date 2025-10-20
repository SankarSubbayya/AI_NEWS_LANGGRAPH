# Prompts Configuration Guide

This guide explains how to use and manage prompts in the AI News LangGraph system using the YAML-based configuration.

## Overview

All prompts are centralized in `src/ai_news_langgraph/config/prompts.yaml` for easy maintenance, version control, and collaboration.

## File Structure

```
src/ai_news_langgraph/
├── config/
│   ├── prompts.yaml        # ⭐ All prompts defined here
│   ├── agents.yaml         # Agent configurations
│   ├── tasks.yaml          # Task definitions
│   └── topics_cancer.json  # Research topics
├── prompt_loader.py        # Utility for loading prompts
└── agents.py               # Agents using the prompts
```

## Prompts Configuration Format

### Basic Structure

```yaml
agent_name:
  prompt_name:
    description: "Brief description of what this prompt does"
    system: "System message template"
    human: |
      Human message template with {variables}
    variables:
      - variable1
      - variable2
```

### Example

```yaml
research_agent:
  analyze_relevance:
    description: "Score article relevance to a specific topic"
    system: "You are {role}. {backstory}"
    human: |
      Score this article's relevance to the topic (0-1):
      Topic: {topic_name} - {topic_desc}
      Article: {title}
      Summary: {content}
      
      Return only a number between 0 and 1.
    variables:
      - role
      - backstory
      - topic_name
      - topic_desc
      - title
      - content
```

## Using Prompts in Your Code

### Method 1: Direct Loading (Recommended)

```python
from ai_news_langgraph.prompt_loader import load_prompt

# Load a prompt template
prompt = load_prompt('research_agent', 'analyze_relevance')

# Use with LangChain
chain = prompt | llm

# Invoke with variables
response = chain.invoke({
    "role": "Junior AI News Researcher",
    "backstory": "Expert in finding quality research",
    "topic_name": "Cancer Detection",
    "topic_desc": "AI for early cancer detection",
    "title": "New AI Model Detects Cancer Early",
    "content": "Researchers develop..."
})
```

### Method 2: Using PromptLoader Class

```python
from ai_news_langgraph.prompt_loader import PromptLoader

# Initialize loader
loader = PromptLoader()

# Get prompt template
prompt = loader.get_prompt_template('editor_agent', 'summarize_articles')

# Get metadata
description = loader.get_prompt_description('editor_agent', 'summarize_articles')
variables = loader.get_prompt_variables('editor_agent', 'summarize_articles')

print(f"Description: {description}")
print(f"Required variables: {variables}")
```

### Method 3: List Available Prompts

```python
from ai_news_langgraph.prompt_loader import get_prompt_loader

loader = get_prompt_loader()

# List all agents
agents = loader.list_agents()
print(f"Available agents: {agents}")

# List prompts for a specific agent
prompts = loader.list_prompts('research_agent')
print(f"Research agent prompts: {prompts}")
```

## Adding New Prompts

### Step 1: Add to prompts.yaml

```yaml
your_agent:
  your_new_prompt:
    description: "What your prompt does"
    system: "You are {role}. {backstory}"
    human: |
      Your prompt template here.
      Use {variables} for dynamic content.
    variables:
      - role
      - backstory
      - your_var1
      - your_var2
```

### Step 2: Use in Your Agent

```python
from ai_news_langgraph.prompt_loader import load_prompt

class YourAgent:
    def your_method(self):
        # Load the prompt
        prompt = load_prompt('your_agent', 'your_new_prompt')
        
        # Use it
        chain = prompt | self.llm
        response = chain.invoke({
            "role": self.config.role,
            "backstory": self.config.backstory,
            "your_var1": "value1",
            "your_var2": "value2"
        })
```

## Current Available Prompts

### Research Agent
- `analyze_relevance` - Score article relevance to topics

### Editor Agent
- `summarize_articles` - Create comprehensive article summaries
- `executive_summary` - Create executive summary across topics

### Chief Editor Agent
- `refine_content` - Refine and proofread content
- `generate_subject_line` - Generate email subject lines

### Judge Editor Agent
- `fact_check` - Verify factual accuracy
- `quality_review` - Perform final quality review

## Best Practices

### 1. Use Clear Variable Names

❌ Bad:
```yaml
human: "Analyze {x} for {y}"
```

✅ Good:
```yaml
human: "Analyze {article_title} for {topic_name}"
```

### 2. Include Descriptions

Always add a description explaining what the prompt does:

```yaml
your_prompt:
  description: "Clear explanation of the prompt's purpose"
  # ...
```

### 3. Document Required Variables

List all variables in the `variables` section:

```yaml
variables:
  - role
  - backstory
  - specific_var1
  - specific_var2
```

### 4. Use Multi-line for Long Prompts

Use YAML's `|` syntax for multi-line prompts:

```yaml
human: |
  This is a long prompt
  that spans multiple lines
  and is easier to read.
```

### 5. Keep System Messages Consistent

Use a standard format for system messages:

```yaml
system: "You are {role}. {backstory}"
```

## Troubleshooting

### Error: Prompt Not Found

```python
KeyError: "Prompt 'your_prompt' not found for agent 'your_agent'"
```

**Solution:** Check that the agent and prompt names match exactly in `prompts.yaml`.

### Error: Missing Variables

```python
KeyError: 'some_variable'
```

**Solution:** Ensure all variables in the prompt template are provided when invoking.

### Reload Prompts After Changes

```python
from ai_news_langgraph.prompt_loader import get_prompt_loader

loader = get_prompt_loader()
loader.reload()  # Reload from file
```

## Version Control

Benefits of YAML-based prompts:
- ✅ Easy to track changes in git
- ✅ Clear diffs when prompts are modified
- ✅ Team can review prompt changes in PRs
- ✅ Can version prompts alongside code
- ✅ No code changes needed for prompt updates

## Testing Prompts

Test your prompts without running the full application:

```python
from ai_news_langgraph.prompt_loader import load_prompt

# Load and inspect
prompt = load_prompt('research_agent', 'analyze_relevance')
print(prompt)

# Test with sample data
chain = prompt | llm
result = chain.invoke({
    "role": "Test Role",
    "backstory": "Test Backstory",
    # ... other variables
})
print(result)
```

## Advanced: Custom Prompt Files

You can use custom prompt files:

```python
from ai_news_langgraph.prompt_loader import PromptLoader

# Load from custom location
loader = PromptLoader('/path/to/custom/prompts.yaml')
prompt = loader.get_prompt_template('agent', 'prompt')
```

## Contributing

When adding new prompts:

1. Add to `prompts.yaml` with clear description
2. Document variables required
3. Test the prompt works
4. Update this guide if needed
5. Submit PR with prompt changes

---

For questions or issues, please refer to the main README or open an issue.

