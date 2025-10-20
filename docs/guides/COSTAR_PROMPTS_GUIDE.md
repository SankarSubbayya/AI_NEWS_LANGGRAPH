# CO-STAR Prompts Guide for AI News LangGraph

## What is CO-STAR?

CO-STAR is a structured prompting framework that improves LLM responses by providing clear context and expectations:

- **C**ontext: Background information and role
- **O**bjective: The specific task
- **S**tyle: How to write
- **T**one: Emotional quality
- **A**udience: Who will read it
- **R**esponse: Expected format

## Implementation in This Project

I've created CO-STAR formatted prompts for your AI News system in two formats:

### 1. Python Implementation (`prompts_costar.py`)
- Fully structured with all CO-STAR components
- Ready to use as a drop-in replacement
- Type-safe with dataclasses

### 2. YAML Configuration (`config/prompts_costar.yaml`)
- Easier to edit and maintain
- Clear separation of each component
- Can be loaded dynamically

## How CO-STAR Improves Your Prompts

### Before (Original Prompt):
```python
"Score this article's relevance to the topic (0-1):
Topic: {topic_name} - {topic_desc}
Article: {title}
Return only a number between 0 and 1."
```

### After (CO-STAR Format):
```yaml
context: |
  You are an AI Research Analyst at a leading oncology institution.
  You specialize in identifying cutting-edge AI applications in cancer care.
  Expertise: oncology, genomics, AI/ML in healthcare, precision medicine

objective: |
  Evaluate article relevance to {topic_name}: {topic_description}
  Score based on value for healthcare professionals

style: "Analytical, precise, evidence-based"

tone: "Professional, objective, scholarly"

audience: "Medical researchers, oncologists, data scientists"

response: |
  Score 0.0-1.0 with weights:
  - Relevance (40%)
  - Credibility (20%)
  - Recency (20%)
  - Innovation (20%)
```

## Benefits of CO-STAR Format

1. **Consistency**: Every prompt follows the same structure
2. **Clarity**: LLM understands role, task, and expectations
3. **Quality**: Better responses due to clear context
4. **Maintainability**: Easy to update components independently
5. **Reusability**: Components can be shared across prompts

## How to Use CO-STAR Prompts

### Option 1: Replace Current Prompts
```python
# In nodes_v2.py, change:
from .prompts import prompt_registry

# To:
from .prompts_costar import costar_prompt_registry as prompt_registry
```

### Option 2: Load from YAML
```python
from prompts_costar import CostarPromptRegistry

registry = CostarPromptRegistry()
registry.load_from_yaml("config/prompts_costar.yaml")
prompt = registry.get_prompt("research_agent", "analyze_relevance")
```

### Option 3: Use Directly
```python
from prompts_costar import get_costar_prompt

# Get a CO-STAR formatted prompt
prompt = get_costar_prompt("research_agent", "analyze_relevance")

# Use with LLM
chain = prompt | llm | output_parser
result = await chain.ainvoke({
    "topic_name": "AI Diagnostics",
    "topic_description": "AI in medical imaging",
    "title": article_title,
    "content": article_content
})
```

## CO-STAR Components for Each Agent

### Research Agent
- **Context**: AI Research Analyst with oncology expertise
- **Objective**: Evaluate relevance, extract facts
- **Style**: Analytical, precise
- **Tone**: Professional, scholarly
- **Audience**: Medical professionals
- **Response**: Scores, structured facts

### Editor Agent
- **Context**: Senior Medical Editor with 15+ years experience
- **Objective**: Create comprehensive summaries
- **Style**: Professional medical writing
- **Tone**: Authoritative yet accessible
- **Audience**: Healthcare executives, researchers
- **Response**: Structured summaries with sections

### Chief Editor
- **Context**: Chief Editor with final responsibility
- **Objective**: Refine and polish content
- **Style**: Editorial excellence
- **Tone**: Polished, engaging
- **Audience**: Time-constrained executives
- **Response**: Refined, publication-ready content

### Self-Reviewer
- **Context**: Quality Assurance Specialist
- **Objective**: Evaluate content quality
- **Style**: Systematic, thorough
- **Tone**: Constructive, professional
- **Audience**: Internal editorial team
- **Response**: Scored assessments with feedback

## Examples of CO-STAR in Action

### Example 1: Article Relevance Scoring

**Without CO-STAR**: "Score this article 0-1"

**With CO-STAR**: The LLM understands:
- It's a research analyst at an oncology institution
- Must evaluate for medical professionals
- Should consider credibility, recency, innovation
- Output single decimal with specific weight criteria

### Example 2: Topic Summary

**Without CO-STAR**: "Summarize these articles"

**With CO-STAR**: The LLM knows:
- It's a senior editor with medical expertise
- Writing for executives and researchers
- Must include overview, findings, trends, implications
- Should be 200-250 words with specific sections

## Customizing CO-STAR Prompts

To modify prompts for your specific needs:

1. **Edit YAML file** (`config/prompts_costar.yaml`):
   - Easiest approach
   - Change any component independently
   - Test immediately

2. **Update Python code** (`prompts_costar.py`):
   - For programmatic changes
   - Add new prompts
   - Modify compilation logic

3. **Key areas to customize**:
   - **Context**: Add specific expertise or credentials
   - **Audience**: Adjust for your readers
   - **Response**: Change output format/structure
   - **Style/Tone**: Match your brand voice

## Testing CO-STAR Prompts

```python
# Test script
from prompts_costar import costar_prompt_registry

# List all prompts
print(costar_prompt_registry.list_prompts())

# Get and test a prompt
prompt = costar_prompt_registry.get_prompt("research_agent", "analyze_relevance")
config = costar_prompt_registry.get_prompt_config("research_agent", "analyze_relevance")

print(f"Context: {config.context[:100]}...")
print(f"Objective: {config.objective[:100]}...")
print(f"Response Format: {config.response_format[:100]}...")
```

## Migration Path

1. **Test first**: Run parallel with existing prompts
2. **Compare outputs**: Verify CO-STAR improves quality
3. **Gradual rollout**: Start with one agent
4. **Full migration**: Replace all prompts

## Summary

CO-STAR prompts provide:
- ✅ Structured, consistent format
- ✅ Clear context for better LLM understanding
- ✅ Improved response quality
- ✅ Easier maintenance
- ✅ Professional framework

The implementation is ready to use and can significantly improve the quality of your AI-generated content!