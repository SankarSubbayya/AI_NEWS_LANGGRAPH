# Quick Start

## Get Running in 5 Minutes

### Prerequisites
- Python 3.9+
- OpenAI API Key (`sk-proj-...`)
- Git

### Step 1: Clone & Setup
```bash
cd AI_NEWS_LANGGRAPH
export OPENAI_API_KEY="sk-proj-your-key-here"
```

### Step 2: Run the App
```bash
uv run streamlit run final_newsletter_app.py --server.port 8501
```

### Step 3: Open in Browser
```
http://localhost:8501
```

### Step 4: Explore Your Newsletter!
1. **Sidebar**: Click any of 5 topics
2. **Tabs**: View Executive Summary, Glossary, Full Newsletter
3. **Download**: Save as HTML

## That's It! 🎉

Your app automatically loads the latest pre-generated newsletter. No generation needed!

### Optional: Enable LangSmith Observability
```bash
export LANGSMITH_API_KEY="lsv2_pt_your-key-here"
```

Then restart the app - you'll see "✅ LangSmith Active" in the sidebar.

See [Full Setup](installation.md) for detailed instructions.
