# AI News LangGraph - Multi-Agent Cancer Research System

A sophisticated multi-agent system built with LangGraph for aggregating, analyzing, and presenting AI news in cancer research. This project implements a collaborative agent workflow similar to CrewAI but using LangGraph's powerful state management and orchestration capabilities.

## 🎉 Latest Enhancements (October 2025)

Six major enhancements have been added to make this system production-ready:

1. **📄 HTML Newsletter Generation** - Beautiful, responsive HTML newsletters with modern design
2. **📊 Plotly Visualizations** - Interactive charts including quality gauges, distribution charts, and analytics dashboards
3. **🎯 COSTAR Prompts** - Enhanced AI prompts using the COSTAR framework (Context, Objective, Style, Tone, Audience, Response)
4. **🎨 Flux AI Auto-Generation** - **NEW!** Automatically generate photorealistic cover images using Flux via Replicate API (no manual work!)
5. **🖼️ Dual Image Generation** - Get both DALL-E (artistic) and Flux (photorealistic) cover images automatically
6. **🧠 Cancer Research Knowledge Graph** - Domain-specific medical knowledge graph with cancer entities, treatments, biomarkers, and medical relationships (NOT TF-IDF!)

**See [FLUX_AUTO_GENERATION.md](FLUX_AUTO_GENERATION.md) for Flux setup and [CANCER_KG_SUMMARY.md](CANCER_KG_SUMMARY.md) for knowledge graph details.**

---

## Features

### Multi-Agent Architecture
- **Research Agent**: Discovers and fetches latest AI news in cancer care
- **Editor Agent**: Curates and summarizes findings with clinical insights
- **Chief Editor Agent**: Creates professional newsletters and reports

### Key Capabilities
- 🌐 **Web Interface**: Beautiful Streamlit UI for easy interaction
- 🔍 **Intelligent Search**: Searches academic and news sources for cancer AI research
- 📊 **Relevance Scoring**: Analyzes and scores articles for relevance
- 📝 **Auto-Summarization**: Creates comprehensive summaries with key findings
- 📰 **Newsletter Generation**: Beautiful HTML newsletters and Markdown reports
- 📈 **Interactive Visualizations**: Plotly charts with quality gauges and dashboards (86.8% avg quality)
- 🎯 **COSTAR Prompts**: Enhanced AI outputs with structured prompt engineering
- 🎨 **Flux AI Auto-Generation**: Automatic photorealistic cover images via Replicate API (NEW!)
- 🖼️ **Dual Image System**: Both DALL-E and Flux images generated automatically
- 🧠 **Cancer Research Knowledge Graph**: Domain-specific medical KG with 28 cancer types, 30+ treatments, 20+ biomarkers
- 🔗 **Medical Relationships**: Semantic relationships (treats, diagnoses, biomarker_for) - NOT just co-occurrence
- 📚 **AI-Powered Glossaries**: Generate context-aware definitions for medical entities
- 🔄 **State Management**: Full workflow tracking with checkpointing
- ⚡ **Performance Metrics**: Tracks agent performance and execution times

## Project Structure

```
AI_NEWS_LANGGRAPH/
├── src/ai_news_langgraph/
│   ├── __init__.py
│   ├── main.py                      # Entry point with CLI
│   ├── graph_v2.py                  # LangGraph workflow definitions
│   ├── nodes_v2.py                  # Workflow nodes (with enhancements)
│   ├── workflow.py                  # Workflow executor
│   ├── html_generator.py            # HTML newsletter templates
│   ├── visualizations.py            # Plotly chart generation
│   ├── costar_prompts.py            # COSTAR prompt framework
│   ├── cover_image_generator.py            # Cover image generation (DALL-E)
│   ├── flux_image_generator.py             # Flux image auto-generation (Replicate) ⭐ NEW
│   ├── flux_prompt_generator.py            # Flux/CivitAI prompt generator
│   ├── cancer_research_knowledge_graph.py  # NEW: Cancer research medical KG ⭐ RECOMMENDED
│   ├── knowledge_graph_builder.py          # Generic TF-IDF KG (for comparison)
│   ├── glossary_generator.py               # AI-powered glossary generation
│   ├── prompt_loader.py             # Prompt management
│   ├── tools.py                     # Search and processing tools
│   ├── schemas.py                   # Pydantic schemas
│   ├── models.py                # Data models
│   └── config/
│       ├── topics_cancer.json   # Research topics configuration
│       ├── prompts.yaml         # Standard prompts
│       ├── prompts_costar.yaml  # NEW: COSTAR prompts
│       ├── agents.yaml          # Agent configurations
│       └── tasks.yaml           # Task definitions
├── docs/                        # 📚 Documentation
│   ├── ENHANCEMENTS_COMPLETE.md # Feature documentation
│   ├── QUICK_START.md           # Quick reference guide
│   ├── ARCHITECTURE.md          # System architecture
│   └── ...                      # Additional guides
├── tests/                       # 🧪 Test suite
│   ├── test_nodes_v2.py
│   ├── test_costar_prompts.py
│   └── ...                      # More tests
├── outputs/                     # Generated outputs directory
│   ├── newsletter_*.html        # HTML newsletters
│   ├── newsletter_*.md          # Markdown reports
│   └── run_results_*.json       # Execution data
├── app.py                       # Streamlit web interface
├── pyproject.toml               # Project dependencies
└── README.md

```

## Installation

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd AI_NEWS_LANGGRAPH
```

2. **Install dependencies**:
```bash
pip install -e .
```

Or using UV:
```bash
uv pip install -e .
```

## Configuration

### Environment Variables

The project uses python-dotenv to load environment variables. It will automatically search for `.env` files in the following locations (in order):

1. Current working directory
2. AI_NEWS_LANGGRAPH project root
3. `../ai_news/.env` (shared with original ai_news project)
4. `.env.example` (as fallback)

**Option 1: Use existing ai_news .env file**

If you have the original ai_news project set up, the system will automatically use its `.env` file.

**Option 2: Create a new .env file**

Copy the example file and add your API keys:

```bash
cp .env.example .env
```

Then edit `.env`:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key

# Optional but Recommended
REPLICATE_API_TOKEN=your_replicate_token  # For Flux image auto-generation (NEW!)
SERPER_API_KEY=your_serper_api_key  # Fallback search API
OPENAI_MODEL=gpt-4o-mini            # Default model
AI_NEWS_TOPIC="AI in Cancer Care"   # Main topic
AI_NEWS_TOPICS_JSON=path/to/topics.json  # Topics config
```

**Getting API Keys:**

- **OpenAI**: Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Tavily**: Get your key from [Tavily](https://tavily.com/)
- **Replicate** (recommended): Get your token from [Replicate API Tokens](https://replicate.com/account/api-tokens) - Enables Flux auto-generation!
- **Serper** (optional): Get your key from [Serper](https://serper.dev/)

### Topics Configuration

Edit `src/ai_news_langgraph/config/topics_cancer.json` to customize research topics:

```json
{
  "main_topic": "AI in Cancer Care",
  "sub_topics": [
    {
      "name": "Cancer Research",
      "description": "AI across oncology research workflows",
      "query": "AI cancer research oncology latest"
    },
    {
      "name": "Early Detection",
      "description": "AI for early cancer detection",
      "query": "AI early cancer detection diagnosis"
    }
  ]
}
```

## Usage

### 🌐 Streamlit Web Application (Recommended)

The easiest way to use the system is through the Streamlit web interface:

```bash
streamlit run app.py
```

This opens a web browser with an interactive interface for:
- ✨ Configuring research topics with a visual editor
- 🚀 Running the multi-agent workflow with one click
- 📊 Viewing results with interactive previews
- 💾 Downloading generated newsletters and reports

**Features:**
- Pre-flight checks for API keys and configuration
- Real-time progress tracking
- Agent performance metrics
- HTML newsletter preview
- Markdown report rendering
- Download in multiple formats (HTML, Markdown, JSON)

See [STREAMLIT_GUIDE.md](docs/STREAMLIT_GUIDE.md) for detailed usage instructions.

### Command Line Interface

**Run the multi-agent workflow** (default):
```bash
python -m ai_news_langgraph.main
```

**Run with custom topic**:
```bash
python -m ai_news_langgraph.main --topic "AI in Radiology"
```

**Run with custom configuration**:
```bash
python -m ai_news_langgraph.main --config path/to/config.json
```

**Run simple mode** (backward compatibility):
```bash
python -m ai_news_langgraph.main --mode simple
```

### Programmatic Usage

```python
from ai_news_langgraph.graph import build_multi_agent_graph

# Build and run the workflow
graph_run = build_multi_agent_graph()
result = graph_run(
    topic="AI in Cancer Care",
    topics_json_path="config/topics_cancer.json"
)

# Access results
print(f"Status: {result['status']}")
print(f"Outputs: {result['outputs']}")
print(f"Summary: {result['summary']}")
```

## Workflow Stages

1. **Initialize**: Load configuration and set up workflow state
2. **Fetch News**: Research agent searches for articles on each topic
3. **Summarize Topics**: Editor agent creates summaries and extracts insights
4. **Executive Summary**: Create overall summary across all topics
5. **Generate Newsletter**: Chief editor produces HTML and Markdown outputs

## Output Files

The system generates several output files in the `outputs/` directory:

- `newsletter_[timestamp].html` - Professional HTML newsletter
- `report_[timestamp].md` - Comprehensive Markdown report
- `data_[timestamp].json` - Structured data export
- `run_results_[timestamp].json` - Complete workflow results

## Agent Details

### Research Assistant
- **Role**: Junior AI News Researcher
- **Goal**: Discover recent, relevant AI news in cancer care
- **Tools**: Web search, academic search, key point extraction

### Editor Assistant
- **Role**: Senior AI Researcher
- **Goal**: Curate and analyze top findings
- **Capabilities**: Trend analysis, clinical insight extraction

### Chief Editor
- **Role**: Newsletter Chief Editor
- **Goal**: Create professional, engaging content
- **Outputs**: HTML newsletters, Markdown reports

## Advanced Features

### State Management
The system uses LangGraph's state management for:
- Workflow checkpointing
- Error recovery
- Progress tracking
- Performance monitoring

### Tool Integration
- **Tavily API**: Primary search engine for news and research
- **Serper API**: Fallback search option
- **OpenAI LLMs**: Content analysis and generation
- **Document Processing**: Key point extraction and categorization

## Development

### Adding New Agents

1. Define agent in `src/ai_news_langgraph/agents.py`
2. Add configuration to `config/agents.yaml`
3. Update workflow in `graph.py`

### Adding New Tools

1. Implement tool in `src/ai_news_langgraph/tools.py`
2. Wrap with `@tool` decorator for LangChain integration
3. Add to agent tool list in configuration

### Customizing Topics

Modify `config/topics_cancer.json` to add new research areas:
```json
{
  "name": "Your Topic",
  "description": "Topic description",
  "query": "Optimized search query"
}
```

## Performance

The system tracks performance metrics for each agent:
- Task execution time
- Success/failure status
- Output quality metrics
- Error handling and recovery

## Comparison with Original AI_NEWS

This LangGraph implementation offers several advantages over the original CrewAI version:

| Feature | Original (CrewAI) | This (LangGraph) |
|---------|------------------|------------------|
| State Management | Limited | Full state tracking |
| Error Recovery | Basic | Advanced with checkpointing |
| Performance Tracking | None | Detailed metrics |
| Workflow Visualization | No | Yes (LangGraph Studio) |
| Memory/Context | Task-level | Full workflow memory |
| Parallel Execution | Sequential | Conditional parallel |
| Output Formats | HTML only | HTML, Markdown, JSON |

## Documentation

Comprehensive documentation is available in the `docs/` folder. See **[docs/README.md](docs/README.md)** for the complete documentation index.

### Quick Links
- **[QUICK_START.md](docs/QUICK_START.md)** - Get started in 2 minutes
- **[STREAMLIT_GUIDE.md](docs/STREAMLIT_GUIDE.md)** - Web interface guide
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture and design
- **[COSTAR_PROMPTS_GUIDE.md](docs/COSTAR_PROMPTS_GUIDE.md)** - COSTAR prompt framework
- **[TESTING_GUIDE.md](docs/TESTING_GUIDE.md)** - Testing documentation
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues and solutions

### All Documentation (16 guides)
See the full documentation index at **[docs/README.md](docs/README.md)** for:
- Getting Started guides
- Core architecture documentation
- Prompt engineering guides
- Technical comparisons
- Testing and troubleshooting

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_nodes_v2.py

# Run with coverage
pytest --cov=ai_news_langgraph tests/
```

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure all required API keys are set in environment
2. **Import Errors**: Install all dependencies with `pip install -e .`
3. **Search Failures**: Check API quotas and network connectivity
4. **LLM Errors**: Verify OpenAI API key and model availability

### Debug Mode

Set environment variable for verbose output:
```bash
export DEBUG=true
python -m ai_news_langgraph.main
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- 📖 [Documentation Index](docs/README.md) - Complete guide index
- 🌐 [Streamlit Guide](docs/STREAMLIT_GUIDE.md) - Web interface tutorial
- 🏗️ [Architecture](docs/ARCHITECTURE.md) - System design and components
- 📋 [Tasks Guide](docs/TASKS_GUIDE.md) - Task configuration
- 💬 [Prompts Guide](docs/PROMPTS_GUIDE.md) - Prompt management
- 🔍 [Search API Guide](docs/SEARCH_API_GUIDE.md) - API configuration
- 🔧 [Troubleshooting](docs/TROUBLESHOOTING.md) - Common issues and fixes

## Acknowledgments

- Inspired by the original AI_NEWS project using CrewAI
- Built with LangGraph for advanced workflow orchestration
- Uses LangChain for LLM integration and tool management

## Contact

For questions or support, please open an issue on GitHub.