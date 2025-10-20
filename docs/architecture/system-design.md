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
