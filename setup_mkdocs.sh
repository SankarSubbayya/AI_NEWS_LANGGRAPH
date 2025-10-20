#!/bin/bash

# Create directories
mkdir -p docs/getting-started
mkdir -p docs/user-guide
mkdir -p docs/features
mkdir -p docs/architecture
mkdir -p docs/api
mkdir -p docs/troubleshooting

# Create getting-started files
cat > docs/getting-started/quick-start.md << 'DOC'
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
DOC

# Create user-guide files
cat > docs/user-guide/running-the-app.md << 'DOC'
# Running the App

## Prerequisites

- Python 3.9+
- OpenAI API Key
- Optional: LangSmith API Key for observability

## Installation

```bash
cd AI_NEWS_LANGGRAPH
pip install -r requirements.txt
# or
uv sync
```

## Starting the App

```bash
uv run streamlit run final_newsletter_app.py --server.port 8501
```

Or with Python directly:

```bash
python -m streamlit run final_newsletter_app.py --server.port 8501
```

## Accessing the App

Open your browser to:
```
http://localhost:8501
```

## Stopping the App

Press `Ctrl+C` in the terminal where Streamlit is running.

Or kill the process:
```bash
pkill -f streamlit
```

## Using a Custom Port

```bash
uv run streamlit run final_newsletter_app.py --server.port 9000
```

Then access at: `http://localhost:9000`

## Troubleshooting

**"Port 8501 already in use"**
```bash
pkill -f streamlit
sleep 2
uv run streamlit run final_newsletter_app.py
```

**"OPENAI_API_KEY not found"**
```bash
export OPENAI_API_KEY="sk-proj-..."
```

See [Troubleshooting](../troubleshooting/common-issues.md) for more help.
DOC

# Create features files
cat > docs/features/overview.md << 'DOC'
# Features Overview

## 📋 Topics

**5 Clickable Cancer Research Topics:**
1. Early Detection with AI
2. Precision Treatment Planning
3. Clinical Trials & Research
4. Prevention & Screening
5. Patient Outcomes & Recovery

Each topic shows:
- Topic name and quality score
- Overview and key findings
- Notable trends
- Top articles with links

## 📖 Glossary

**15 Medical Terms** with:
- AI-generated definitions
- Term type (Diagnostic, Treatment, etc.)
- Related terms
- Context from knowledge graph

## 📝 Executive Summary

- High-level newsletter overview
- Key insights across all topics
- One-sentence highlights
- Quick read format

## 📰 Full Newsletter

- Complete HTML newsletter
- All 5 topics together
- Professional formatting
- Download as HTML

## 📚 Newsletter History

- Access previous newsletters
- Quick selection dropdown
- View any past generation
- Full content available

## 📊 Observability

- **LangSmith Integration**
- Real-time operation tracing
- Token usage tracking
- Cost estimation
- Dashboard link in sidebar

See individual feature pages for detailed information.
DOC

# Create architecture files
cat > docs/architecture/system-design.md << 'DOC'
# System Design

## High-Level Architecture

```
User Interface (Streamlit)
        ↓
App (final_newsletter_app.py)
        ↓
LangGraph Workflow
        ↓
├─ Research Node (Fetch Articles)
├─ Summarizer Node (Process Content)
├─ Editor Node (Polish Content)
├─ Quality Node (Score Content)
├─ Image Generator (DALL-E/Flux)
├─ Knowledge Graph (Entity Extraction)
└─ Glossary Generator (AI Definitions)
        ↓
HTML Newsletter
        ↓
Display in Streamlit
```

## Key Components

### 1. **Streamlit App** (`final_newsletter_app.py`)
- User interface
- Tab navigation
- Topic selection
- Sidebar controls

### 2. **LangGraph Workflow** (`src/workflow.py`)
- Multi-agent orchestration
- Sequential node execution
- State management

### 3. **Nodes** (`src/nodes_v2.py`)
- Research Agent
- Summarizer Agent
- Editor Agent
- Quality Reviewer
- Image Generator
- Knowledge Graph Builder
- Glossary Generator

### 4. **Generators**
- HTML Newsletter (`html_generator.py`)
- Cover Images (`cover_image_generator.py`)
- DALL-E Images (`enhanced_cover_generator.py`)
- Flux Images (`flux_image_generator.py`)
- Glossary (`glossary_generator.py`)
- Knowledge Graph (`knowledge_graph_builder.py`)

### 5. **Observability** (`langsmith_observability.py`)
- LangSmith tracing
- Operation monitoring
- Cost tracking

## Data Flow

1. **User Click** → Streamlit app receives request
2. **Load Newsletter** → Find latest HTML in outputs/
3. **Extract Content** → Parse topics, summary, glossary
4. **Display** → Render in appropriate tabs
5. **Optional** → Generate new newsletter if needed

## Storage

```
outputs/
├── newsletter_*.html      # Generated newsletters
├── images/
│   └── dalle_cover_*.png  # Cover images
└── knowledge_graphs/
    └── *.json            # Entity relationships
```

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Workflow | LangGraph |
| LLM Framework | LangChain |
| UI | Streamlit |
| LLMs | OpenAI (GPT-4o-mini, DALL-E) |
| Image Gen | Replicate (Flux) |
| Observability | LangSmith |
| Data Format | JSON, HTML |

See [Workflow](workflow.md) for detailed flow.
DOC

echo "✅ MkDocs structure created successfully!"
echo ""
echo "Next steps:"
echo "1. Install mkdocs: pip install mkdocs mkdocs-material"
echo "2. Run docs: mkdocs serve"
echo "3. Open: http://localhost:8000"
