# 📚 AI News LangGraph Documentation

Welcome to the comprehensive documentation for the AI News LangGraph multi-agent system!

## 🎯 Quick Navigation

### Getting Started
- **[QUICK_START.md](QUICK_START.md)** - Get up and running in 2 minutes
- **[RUN_GUIDE.md](RUN_GUIDE.md)** - Detailed execution instructions
- **[STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)** - Web interface guide

### Core Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design patterns
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)** - Implementation details and best practices
- **[WORKFLOW_GRAPH.md](WORKFLOW_GRAPH.md)** - LangGraph workflow visualization

### Prompts & Configuration
- **[COSTAR_PROMPTS_GUIDE.md](COSTAR_PROMPTS_GUIDE.md)** - COSTAR prompt framework (Context, Objective, Style, Tone, Audience, Response)
- **[HOW_TO_CREATE_ENHANCED_PROMPTS.md](HOW_TO_CREATE_ENHANCED_PROMPTS.md)** - Prompt engineering guide
- **[PROMPTS_GUIDE.md](PROMPTS_GUIDE.md)** - Standard prompts reference
- **[TASKS_GUIDE.md](TASKS_GUIDE.md)** - Task configuration guide

### Testing & Troubleshooting
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Comprehensive testing guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

### Technical Comparisons
- **[CREWAI_VS_LANGGRAPH.md](CREWAI_VS_LANGGRAPH.md)** - Comparison with CrewAI framework
- **[SEARCH_API_GUIDE.md](SEARCH_API_GUIDE.md)** - News API integration details
- **[GRAPH_VISUALIZATION.md](GRAPH_VISUALIZATION.md)** - Workflow graph visualization tools

---

## 🚀 Quick Start Path

### For New Users
1. 📖 Read **[QUICK_START.md](QUICK_START.md)**
2. 🎨 Try the web UI: **[STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md)**
3. ▶️ Run your first workflow: **[RUN_GUIDE.md](RUN_GUIDE.md)**

### For Developers
1. 🏗️ Understand the architecture: **[ARCHITECTURE.md](ARCHITECTURE.md)**
2. 💻 Review implementation: **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)**
3. 🧪 Set up testing: **[TESTING_GUIDE.md](TESTING_GUIDE.md)**

### For Prompt Engineers
1. 🎯 Learn COSTAR framework: **[COSTAR_PROMPTS_GUIDE.md](COSTAR_PROMPTS_GUIDE.md)**
2. ✍️ Create custom prompts: **[HOW_TO_CREATE_ENHANCED_PROMPTS.md](HOW_TO_CREATE_ENHANCED_PROMPTS.md)**
3. 📝 Configure tasks: **[TASKS_GUIDE.md](TASKS_GUIDE.md)**

---

## 📊 System Features

### Multi-Agent Workflow
- 🔍 **News Fetcher Agent**: Searches and retrieves articles from multiple sources
- 📝 **Summarizer Agent**: Creates concise, informative summaries
- ✅ **Quality Reviewer Agent**: Validates content quality and relevance
- 📰 **Editor Agent**: Generates professional newsletters in HTML and Markdown

### Key Capabilities
- **HTML Newsletter Generation**: Responsive, modern design with embedded charts
- **Interactive Visualizations**: Plotly charts for article distribution and quality metrics
- **COSTAR Prompts**: Structured prompts for consistent, high-quality outputs
- **Streaming Support**: Real-time progress updates
- **Web Interface**: User-friendly Streamlit application
- **Quality Scoring**: Automated relevance and quality assessment
- **Multi-Format Output**: HTML, Markdown, and JSON

### Performance
- **Quality Score**: ~86.8% average
- **Topics**: 5+ research areas (configurable)
- **Articles**: 50+ analyzed per run
- **Charts**: 4 interactive visualizations
- **Execution**: ~2-3 minutes

---

## 📁 Documentation Structure

```
docs/
├── README.md                          # This file
├── QUICK_START.md                     # 2-minute setup guide
├── RUN_GUIDE.md                       # Execution instructions
├── ARCHITECTURE.md                    # System design
├── IMPLEMENTATION_GUIDE.md            # Implementation details
├── WORKFLOW_GRAPH.md                  # Workflow visualization
├── STREAMLIT_GUIDE.md                 # Web UI guide
├── COSTAR_PROMPTS_GUIDE.md            # COSTAR framework
├── HOW_TO_CREATE_ENHANCED_PROMPTS.md  # Prompt engineering
├── PROMPTS_GUIDE.md                   # Standard prompts
├── TASKS_GUIDE.md                     # Task configuration
├── TESTING_GUIDE.md                   # Testing guide
├── TROUBLESHOOTING.md                 # Common issues
├── CREWAI_VS_LANGGRAPH.md             # Framework comparison
├── SEARCH_API_GUIDE.md                # API integration
├── GRAPH_VISUALIZATION.md             # Graph tools
└── diagrams/                          # Visual diagrams
    ├── workflow.mmd                   # Mermaid diagram
    └── state_flow.mmd                 # State flow
```

---

## 🎓 Learning Path by Role

### 🎨 Content Creator
1. Quick Start → Streamlit Guide → Run Guide
2. Try the web interface
3. Review generated newsletters
4. Customize topics in `config/tasks.yaml`

### 👨‍💻 Software Engineer
1. Architecture → Implementation Guide → Testing Guide
2. Review `src/ai_news_langgraph/` code
3. Run tests: `pytest tests/`
4. Experiment with custom nodes

### 🧠 AI/ML Engineer
1. COSTAR Prompts → How to Create Prompts → Prompts Guide
2. Review `config/prompts_costar.yaml`
3. Experiment with prompt variations
4. Analyze quality scores and metrics

### 🏢 Tech Lead
1. Architecture → CrewAI vs LangGraph → Implementation Guide
2. Review workflow design
3. Assess scalability and performance
4. Plan customizations

---

## 📈 Recent Updates (October 2025)

### Latest Enhancements
- ✅ HTML newsletter generation with responsive templates
- ✅ Plotly interactive visualizations
- ✅ COSTAR prompt framework integration
- ✅ Quality scoring and metrics
- ✅ Streamlit web interface
- ✅ Comprehensive testing suite

### Coming Soon
- [ ] More visualization types
- [ ] Advanced filtering options
- [ ] Email delivery integration
- [ ] Multi-language support

---

## 🔗 External Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Plotly Python](https://plotly.com/python/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Pydantic V2](https://docs.pydantic.dev/latest/)
- [OpenAI API](https://platform.openai.com/docs)

---

## 💬 Getting Help

1. 📖 **Check relevant guide** - Start with the topic-specific document
2. 🐛 **Review Troubleshooting** - Common issues and solutions
3. 🔍 **Search code** - All modules are well-commented
4. 🐞 **Debug mode** - Set `export LOG_LEVEL=DEBUG`
5. 📝 **Review logs** - Check `outputs/` for execution logs

---

## 🤝 Contributing

When adding new features:
1. Update relevant documentation
2. Add tests to `tests/`
3. Update `ARCHITECTURE.md` if needed
4. Add examples to `QUICK_START.md`

---

**Happy Reading! 📚**

*Last updated: October 2025*
