# Implementation Guide: Enhanced Cancer-Specific AI News System

## Overview

This guide documents the enhanced implementation of the AI News LangGraph system with:
1. **Cancer-specific news sources** (PubMed, NEJM, JCO, Nature Cancer, etc.)
2. **Agent constructor YAML files** (one per agent with detailed configurations)
3. **Enhanced CO-STAR prompts** (with audience specs, style guides, and few-shot examples)
4. **Alternative news APIs** (replacing SerperAPI dependency)

## Table of Contents

- [Architecture](#architecture)
- [Cancer-Specific News Sources](#cancer-specific-news-sources)
- [Agent Configuration System](#agent-configuration-system)
- [Enhanced Prompting System](#enhanced-prompting-system)
- [API Configuration](#api-configuration)
- [Usage Examples](#usage-examples)
- [Testing](#testing)

---

## Architecture

### Component Overview

```
AI_NEWS_LANGGRAPH/
├── src/ai_news_langgraph/
│   ├── tools_cancer_news.py       # NEW: Cancer-specific news sources
│   ├── tools.py                   # UPDATED: Integrated cancer sources
│   ├── prompts_enhanced.py        # NEW: Enhanced CO-STAR prompts
│   ├── config/
│   │   ├── agents/                # NEW: Individual agent configs
│   │   │   ├── research_assistant.yaml
│   │   │   ├── editor_assistant.yaml
│   │   │   ├── chief_editor.yaml
│   │   │   └── self_reviewer.yaml
│   │   └── prompts_costar_enhanced.yaml  # NEW: Enhanced prompts
│   ├── nodes_v2.py                # Agent node implementations
│   ├── workflow.py                # Workflow orchestration
│   └── graph_v2.py                # Main graph interface
```

### Data Flow

```
User Query
    ↓
Cancer News Sources (PubMed, NEJM, JCO, etc.)
    ↓
Research Assistant (with enhanced CO-STAR prompts)
    ↓
Editor Assistant (synthesis with few-shot learning)
    ↓
Chief Editor (HTML formatting)
    ↓
Self Reviewer (QA with detailed checklist)
    ↓
Final Newsletter
```

---

## Cancer-Specific News Sources

### Overview

The new `tools_cancer_news.py` module provides targeted access to authoritative cancer research sources, eliminating dependency on generic search APIs like SerperAPI.

### Supported Sources

| Source | Type | Coverage | API |
|--------|------|----------|-----|
| **PubMed/NCBI** | API | All peer-reviewed medical research | NCBI E-utilities |
| **Journal of Clinical Oncology** | RSS | Oncology clinical trials & research | RSS feed |
| **New England Journal of Medicine** | RSS | High-impact medical research | RSS feed |
| **Nature Cancer** | RSS | Cancer-focused Nature articles | RSS feed |
| **National Cancer Institute** | RSS | NCI news and research updates | RSS feed |
| **ASCO** | RSS | Clinical oncology society news | RSS feed |
| **Oncology News Central** | RSS | Oncology news aggregator | RSS feed |
| **Stanford Medicine PubNet** | Web | Stanford cancer research | Web scraping |

### Key Features

#### 1. Multi-Source Aggregation

```python
from ai_news_langgraph.tools_cancer_news import CancerNewsAPI

api = CancerNewsAPI()

# Search all sources simultaneously
articles = api.search_all_sources(
    query="AI machine learning cancer diagnosis",
    max_results_per_source=5,
    days_back=30
)

# Returns deduplicated, date-sorted results
print(f"Found {len(articles)} unique articles")
```

#### 2. PubMed Integration

Direct access to NCBI E-utilities API for peer-reviewed research:

```python
# Search PubMed specifically
pubmed_articles = api._search_pubmed(
    query="artificial intelligence oncology",
    max_results=10,
    days_back=30
)

# Each article includes:
# - title, url, content
# - authors, journal, PMID
# - publication date
# - relevance score
```

#### 3. RSS Feed Processing

Automated parsing of medical journal RSS feeds:

```python
# Automatically pulls from:
# - JCO RSS feed
# - NEJM RSS feed
# - Nature Cancer RSS feed
# - NCI news feed
# - ASCO news feed

# Filters by:
# - Date range (days_back parameter)
# - Query relevance (keyword matching)
# - Content quality (source reputation)
```

#### 4. Alternative APIs

Support for additional news APIs:

```python
# AI News API (if API key available)
ai_news_results = api._search_ai_news_api(
    query="cancer AI",
    max_results=10
)

# NewsAPI.org (if API key available)
newsapi_results = api._search_newsapi(
    query="cancer AI",
    max_results=10,
    days_back=30
)
```

### Integration with Existing Tools

The cancer news sources are automatically integrated into `NewsSearchTool`:

```python
from ai_news_langgraph.tools import NewsSearchTool

# Automatically uses cancer sources if enabled
searcher = NewsSearchTool()

# Searches cancer-specific sources first
results = searcher.search("AI lung cancer detection")

# Falls back to Tavily/Serper if cancer sources fail
# or if USE_CANCER_SOURCES=false in environment
```

### Environment Configuration

```bash
# Enable cancer-specific sources (default: true)
export USE_CANCER_SOURCES=true

# Optional: Additional API keys for broader coverage
export AI_NEWS_API_KEY=your_api_key
export NEWSAPI_KEY=your_newsapi_key

# PubMed configuration
export PUBMED_EMAIL=your_email@example.com

# Legacy APIs (still supported as fallback)
export TAVILY_API_KEY=your_tavily_key
export SERPER_API_KEY=your_serper_key
```

---

## Agent Configuration System

### Overview

Each agent now has a dedicated YAML configuration file defining its role, capabilities, and behavior. This follows the metamorphosis pattern of explicit agent construction.

### Agent Configuration Files

#### 1. Research Assistant ([research_assistant.yaml](src/ai_news_langgraph/config/agents/research_assistant.yaml))

**Role**: Junior AI News Researcher specializing in Oncology

**Key Configuration**:
```yaml
agent_id: research_assistant
role: "Junior AI News Researcher specializing in Oncology"
goal: "Discover the most recent, relevant and trending topics on AI applications in Cancer care"

backstory: |
  Diligent content researcher with expertise in finding high-quality,
  peer-reviewed research and understanding clinical implications.

model: "gpt-4o-mini"
temperature: 0.7
max_tokens: 4000

tools:
  - search_news
  - search_academic_papers
  - extract_key_points

search_config:
  preferred_sources:
    - PubMed/NCBI
    - Journal of Clinical Oncology
    - New England Journal of Medicine
  max_results_per_topic: 10
  days_back: 30
```

**Usage**:
```python
import yaml
from pathlib import Path

# Load agent config
config_path = Path("src/ai_news_langgraph/config/agents/research_assistant.yaml")
with open(config_path) as f:
    config = yaml.safe_load(f)

# Access configuration
print(f"Agent: {config['role']}")
print(f"Tools: {config['tools']}")
print(f"Model: {config['model']}")
```

#### 2. Editor Assistant ([editor_assistant.yaml](src/ai_news_langgraph/config/agents/editor_assistant.yaml))

**Role**: Senior AI Researcher and Content Curator

**Key Configuration**:
```yaml
agent_id: editor_assistant
role: "Senior AI Researcher and Content Curator"
goal: "Curate and editorialize findings, identifying trends and translating research"

backstory: |
  Experienced medical journalist with Ph.D. in Computational Biology,
  10+ years covering AI in healthcare, excels at pattern recognition
  and making complex research accessible.

analysis_config:
  summary_styles:
    - executive_overview: 180-250 words
    - per_topic_summary: 140-200 words
    - key_findings: 3-5 bullet points per topic

  focus_areas:
    - Breakthrough developments
    - Clinical trial results
    - Practical applications
```

#### 3. Chief Editor ([chief_editor.yaml](src/ai_news_langgraph/config/agents/chief_editor.yaml))

**Role**: Chief Editor of AI in Cancer Care Weekly Digest

**Key Configuration**:
```yaml
agent_id: chief_editor
role: "Chief Editor of AI in Cancer Care Weekly Digest"
goal: "Transform summaries into professionally formatted, engaging HTML newsletter"

design_config:
  layout:
    type: responsive_single_column
    max_width: 680px

  typography:
    font_family: "Georgia, 'Times New Roman', serif"
    heading_font: "Arial, Helvetica, sans-serif"

  colors:
    primary: "#2c5282"
    accent: "#e53e3e"

newsletter_structure:
  header: [logo, date, issue_number, reading_time]
  sections: [executive_summary, 5_topic_sections, trends, further_reading]
  footer: [contact, unsubscribe, privacy]
```

#### 4. Self Reviewer ([self_reviewer.yaml](src/ai_news_langgraph/config/agents/self_reviewer.yaml))

**Role**: Senior Quality Assurance Editor and Fact Checker

**Key Configuration**:
```yaml
agent_id: self_reviewer
role: "Senior Quality Assurance Editor and Fact Checker"
goal: "Ensure highest quality standards through rigorous fact-checking"

review_criteria:
  1_factual_accuracy:
    - verify_all_statistics: true
    - check_study_citations: true
    priority: critical

  2_scientific_accuracy:
    - check_technical_terms: true
    - assess_conclusion_validity: true
    priority: critical

  3_editorial_quality:
    - check_grammar_spelling: true
    - ensure_consistent_voice: true
    priority: high

quality_metrics:
  readability:
    target_flesch_reading_ease: 50-60
    target_flesch_kincaid_grade: 10-12
```

### Loading Agent Configurations

```python
from pathlib import Path
import yaml

def load_agent_config(agent_id: str) -> dict:
    """Load agent configuration from YAML file."""
    config_path = Path(f"src/ai_news_langgraph/config/agents/{agent_id}.yaml")

    if not config_path.exists():
        raise FileNotFoundError(f"Agent config not found: {config_path}")

    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# Load all agent configs
agents = ['research_assistant', 'editor_assistant', 'chief_editor', 'self_reviewer']
configs = {agent: load_agent_config(agent) for agent in agents}

# Use in workflow
research_config = configs['research_assistant']
llm = ChatOpenAI(model=research_config['model'], temperature=research_config['temperature'])
```

---

## Enhanced Prompting System

### Overview

The enhanced CO-STAR prompting system includes:
1. **Detailed agent personas** with specific backgrounds and credentials
2. **Comprehensive audience specifications** (expertise level, reading context)
3. **Explicit style and tone guidelines**
4. **Few-shot examples** (2-3 per prompt) demonstrating desired outputs

### CO-STAR Framework

**C**ontext → **O**bjective → **S**tyle → **T**one → **A**udience → **R**esponse

### Enhanced Prompt Components

#### 1. Context (Detailed Persona)

**Before**:
```yaml
context: "You are an AI Research Analyst evaluating articles."
```

**After**:
```yaml
context: |
  You are Dr. Sarah Chen, an AI Research Analyst at Stanford Medicine with dual
  expertise in computational oncology and machine learning. You have:
  - Ph.D. in Computational Biology (Stanford, 2018)
  - 8 years evaluating AI applications in cancer diagnosis and treatment
  - 45+ peer-reviewed publications in Nature Medicine, JCO, and JAMA Oncology
  - Experience as a grant reviewer for NIH/NCI cancer informatics programs
```

#### 2. Audience (Detailed Specification)

**Before**:
```yaml
audience: "Medical researchers and oncologists"
```

**After**:
```yaml
audience: |
  **Primary**: Medical oncologists, cancer researchers, clinical data scientists
  **Secondary**: Healthcare executives, policy makers, grant reviewers

  **Expertise Level**: Advanced (assumes knowledge of both oncology and AI/ML)
  **Reading Context**: Rapid triage of research for weekly digest
  **Information Need**: Quick determination of article relevance and priority
```

#### 3. Style (Comprehensive Guidelines)

**Before**:
```yaml
style: "Analytical and precise"
```

**After**:
```yaml
style: |
  - Analytical and evidence-based
  - Systematic evaluation using defined criteria
  - Quantitative scoring with clear justification
  - Focus on clinical applicability and research impact
```

#### 4. Few-Shot Examples

**New Addition**:
```yaml
few_shot_examples:
  - example: 1
    input:
      topic_name: "Early Detection and Diagnosis"
      title: "Deep Learning Model Achieves 94% Accuracy in Lung Cancer Detection"
      content: "Researchers at Johns Hopkins developed..."
    output: "0.95"
    reasoning: |
      High relevance (0.4): Directly addresses early detection via imaging AI
      High credibility (0.2): Nature Medicine, large study, validated results
      High recency (0.2): Recent publication, near-term FDA timeline
      High innovation (0.19): Significant improvement over current practice
      Total: 0.95
```

### Using Enhanced Prompts

#### Option 1: Python API

```python
from ai_news_langgraph.prompts_enhanced import get_enhanced_prompt

# Full prompt with few-shot examples
prompt = get_enhanced_prompt(
    agent_name="research_agent",
    prompt_name="analyze_relevance",
    topic_name="Early Detection and Diagnosis",
    topic_description="AI in medical imaging for cancer detection",
    title="Deep Learning Detects Lung Cancer with 94% Accuracy",
    content="Study of 1,200 patients...",
    source="Nature Medicine",
    published_date="2024-01-15",
    compact=False  # Full version with all examples
)

# Compact version (for token-limited APIs)
compact_prompt = get_enhanced_prompt(
    agent_name="research_agent",
    prompt_name="analyze_relevance",
    # ... same parameters ...
    compact=True  # Abbreviated version with 1 example
)
```

#### Option 2: Direct YAML Access

```python
import yaml
from pathlib import Path

# Load enhanced prompts
config_path = Path("src/ai_news_langgraph/config/prompts_costar_enhanced.yaml")
with open(config_path, 'r') as f:
    prompts = yaml.safe_load(f)

# Access specific prompt
research_prompt = prompts['research_agent']['analyze_relevance']

# Get components
context = research_prompt['context']
objective = research_prompt['objective']
examples = research_prompt['few_shot_examples']
```

### Available Enhanced Prompts

| Agent | Prompt | Few-Shot Examples | Token Count (Full) |
|-------|--------|-------------------|---------------------|
| research_agent | analyze_relevance | 3 | ~1,200 |
| research_agent | extract_key_facts | 3 | ~1,400 |
| editor_agent | summarize_topic | 2 | ~1,800 |
| chief_editor | generate_newsletter | 1 | ~2,200 |
| self_reviewer | review_content | 2 | ~1,600 |

---

## API Configuration

### Environment Variables

```bash
# ========================================
# Cancer-Specific Sources (Recommended)
# ========================================

# Enable cancer sources (default: true)
export USE_CANCER_SOURCES=true

# PubMed API (free, no key required)
export PUBMED_EMAIL=your_email@example.com

# ========================================
# Optional: Additional APIs for Broader Coverage
# ========================================

# AI News API (https://www.ainews-api.com/)
export AI_NEWS_API_KEY=your_ai_news_key

# NewsAPI.org (https://newsapi.org/)
export NEWSAPI_KEY=your_newsapi_key

# ========================================
# Legacy/Fallback APIs
# ========================================

# Tavily (AI-optimized search)
export TAVILY_API_KEY=your_tavily_key

# Serper (Google Search API)
export SERPER_API_KEY=your_serper_key

# Preferred fallback API (if cancer sources disabled)
export PREFERRED_SEARCH_API=tavily  # or 'serper'

# ========================================
# LLM Configuration
# ========================================

export OPENAI_API_KEY=your_openai_key
```

### API Priority Order

1. **Cancer-specific sources** (if `USE_CANCER_SOURCES=true`)
   - PubMed API
   - Medical journal RSS feeds
   - AI News API (if key available)
   - NewsAPI (if key available)

2. **Fallback to general sources** (if cancer sources fail or disabled)
   - Tavily API (if `PREFERRED_SEARCH_API=tavily`)
   - Serper API (if `PREFERRED_SEARCH_API=serper`)

### Disabling SerperAPI

To completely avoid SerperAPI dependency:

```bash
# Use cancer-specific sources only
export USE_CANCER_SOURCES=true
unset SERPER_API_KEY

# Or use Tavily as fallback
export USE_CANCER_SOURCES=true
export PREFERRED_SEARCH_API=tavily
export TAVILY_API_KEY=your_tavily_key
```

---

## Usage Examples

### Example 1: Search Cancer-Specific Sources

```python
from ai_news_langgraph.tools_cancer_news import CancerNewsAPI

# Initialize API
api = CancerNewsAPI()

# Search all cancer sources
articles = api.search_all_sources(
    query="AI artificial intelligence deep learning cancer diagnosis",
    max_results_per_source=5,
    days_back=30
)

print(f"Found {len(articles)} articles from:")
for article in articles:
    print(f"  - {article['source']}: {article['title']}")
```

### Example 2: Load and Use Agent Configuration

```python
import yaml
from pathlib import Path
from langchain_openai import ChatOpenAI

# Load research assistant config
config_path = Path("src/ai_news_langgraph/config/agents/research_assistant.yaml")
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Initialize LLM with agent config
llm = ChatOpenAI(
    model=config['model'],
    temperature=config['temperature'],
    max_tokens=config.get('max_tokens', 4000)
)

# Use agent's search preferences
preferred_sources = config['search_config']['preferred_sources']
max_results = config['search_config']['max_results_per_topic']
days_back = config['search_config']['days_back']

print(f"Agent: {config['role']}")
print(f"Searching {preferred_sources[:3]} for articles from last {days_back} days")
```

### Example 3: Use Enhanced CO-STAR Prompts

```python
from ai_news_langgraph.prompts_enhanced import get_enhanced_prompt, enhanced_prompt_registry

# List available prompts
print("Available prompts:")
for prompt_name in enhanced_prompt_registry.list_prompts("research_agent"):
    print(f"  - {prompt_name}")

# Get full prompt with few-shot examples
prompt = get_enhanced_prompt(
    agent_name="research_agent",
    prompt_name="extract_key_facts",
    title="AI Model Predicts Immunotherapy Response in Melanoma",
    content="A study from Memorial Sloan Kettering analyzed 847 patients...",
    source="Journal of Clinical Oncology"
)

# Use with LLM
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
response = llm.predict(prompt)
print(response)
```

### Example 4: Run Complete Workflow

```python
from ai_news_langgraph.graph_v2 import AINewsWorkflow

# Initialize workflow
workflow = AINewsWorkflow()

# Run with cancer-specific sources
result = workflow.run(
    main_topic="Artificial Intelligence in Cancer Care",
    subtopics=[
        "Early Detection and Diagnosis",
        "Treatment Planning",
        "Clinical Trials"
    ]
)

# Access results
print(f"Newsletter generated: {result['final_newsletter_path']}")
print(f"Articles found: {len(result['all_articles'])}")
```

---

## Testing

### Test Enhanced Prompts

```python
# Test script: test_enhanced_prompts.py
from ai_news_langgraph.prompts_enhanced import enhanced_prompt_registry

# Test loading
assert len(enhanced_prompt_registry.prompts) > 0, "No prompts loaded"

# Test each agent
agents = ["research_agent", "editor_agent", "chief_editor", "self_reviewer"]
for agent in agents:
    prompts = enhanced_prompt_registry.list_prompts(agent)
    assert len(prompts) > 0, f"No prompts for {agent}"
    print(f"✅ {agent}: {len(prompts)} prompts loaded")

# Test rendering
prompt = enhanced_prompt_registry.render_prompt(
    agent_name="research_agent",
    prompt_name="analyze_relevance",
    topic_name="Test Topic",
    topic_description="Test description",
    title="Test title",
    content="Test content",
    source="Test source",
    published_date="2024-01-15"
)

assert "# CONTEXT" in prompt
assert "# FEW-SHOT EXAMPLES" in prompt or "# EXAMPLES" in prompt
assert len(prompt) > 1000  # Should be substantial
print("✅ Prompt rendering works")
```

### Test Cancer News Sources

```bash
# Install dependencies
pip install feedparser beautifulsoup4

# Run test
python -c "
from ai_news_langgraph.tools_cancer_news import CancerNewsAPI

api = CancerNewsAPI()
results = api.search_all_sources('AI cancer', max_results_per_source=2, days_back=30)
print(f'✅ Found {len(results)} articles')
assert len(results) > 0, 'No articles found'
"
```

### Test Agent Configs

```bash
# Test loading all agent configs
python -c "
import yaml
from pathlib import Path

agents = ['research_assistant', 'editor_assistant', 'chief_editor', 'self_reviewer']
for agent in agents:
    path = Path(f'src/ai_news_langgraph/config/agents/{agent}.yaml')
    with open(path) as f:
        config = yaml.safe_load(f)
    assert 'agent_id' in config
    assert 'role' in config
    print(f'✅ {agent}: {config[\"role\"][:50]}...')
"
```

---

## Migration from Old Implementation

### Changes Summary

1. **News Sources**: SerperAPI → Cancer-specific sources (PubMed, NEJM, etc.)
2. **Agent Configs**: Merged agents.yaml → Individual files per agent
3. **Prompts**: Basic prompts → Enhanced CO-STAR with few-shot examples
4. **Tools**: Generic NewsSearchTool → CancerNewsAPI integration

### Migration Steps

```bash
# 1. Install new dependencies
pip install feedparser beautifulsoup4

# 2. Set environment variables
export USE_CANCER_SOURCES=true
export PUBMED_EMAIL=your_email@example.com

# 3. Update imports in your code
# OLD:
# from ai_news_langgraph.prompts_costar import get_costar_prompt

# NEW:
from ai_news_langgraph.prompts_enhanced import get_enhanced_prompt

# 4. Update prompt calls
# OLD:
# prompt = get_costar_prompt("research_agent", "analyze_relevance", **kwargs)

# NEW:
prompt = get_enhanced_prompt("research_agent", "analyze_relevance", **kwargs)

# 5. Test the changes
python test_enhanced_prompts.py
```

---

## Troubleshooting

### Issue: No articles found from cancer sources

**Solution**:
```bash
# Check PubMed API access
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=cancer&retmode=json"

# Verify email is set
echo $PUBMED_EMAIL

# Test RSS feeds
python -c "import feedparser; print(len(feedparser.parse('https://www.cancer.gov/syndication/feeds/rss/news').entries))"
```

### Issue: Enhanced prompts not loading

**Solution**:
```bash
# Check file exists
ls -l src/ai_news_langgraph/config/prompts_costar_enhanced.yaml

# Test YAML syntax
python -c "import yaml; yaml.safe_load(open('src/ai_news_langgraph/config/prompts_costar_enhanced.yaml'))"

# Verify import
python -c "from ai_news_langgraph.prompts_enhanced import enhanced_prompt_registry; print(len(enhanced_prompt_registry.prompts))"
```

### Issue: Agent config not found

**Solution**:
```bash
# List agent config files
ls -l src/ai_news_langgraph/config/agents/

# Test loading
python -c "import yaml; print(yaml.safe_load(open('src/ai_news_langgraph/config/agents/research_assistant.yaml'))['agent_id'])"
```

---

## Next Steps

1. **Customize Agent Configs**: Edit YAML files in `config/agents/` to adjust agent behavior
2. **Extend News Sources**: Add more RSS feeds or APIs to `tools_cancer_news.py`
3. **Refine Prompts**: Add more few-shot examples to `prompts_costar_enhanced.yaml`
4. **Add Topics**: Update `config/tasks.yaml` with new cancer research topics
5. **Monitor Performance**: Track article relevance scores and newsletter quality metrics

---

## References

- **Metamorphosis Pattern**: https://github.com/supportvectors/metamorphosis
- **CO-STAR Framework**: Context, Objective, Style, Tone, Audience, Response
- **PubMed API**: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- **NewsAPI**: https://newsapi.org/docs
- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/

---

**Last Updated**: January 2024
**Version**: 2.0.0
**Authors**: AI News LangGraph Team
