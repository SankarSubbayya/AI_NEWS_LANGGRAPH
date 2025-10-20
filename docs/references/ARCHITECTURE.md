# AI News LangGraph - Architecture & Workflow Diagram

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AI NEWS LANGGRAPH SYSTEM                         │
│                    Multi-Agent Research & Newsletter                     │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│                              ENTRY POINT                                  │
├──────────────────────────────────────────────────────────────────────────┤
│  main.py                                                                  │
│  ├─ load_env_file()      # Load .env configuration                       │
│  ├─ run_multi_agent()    # Main workflow                                 │
│  └─ CLI Arguments:                                                        │
│     --mode, --topic, --config                                            │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                          CONFIGURATION LAYER                              │
├──────────────────────────────────────────────────────────────────────────┤
│  config/                                                                  │
│  ├─ prompts.yaml         # ⭐ All LLM prompts (centralized)              │
│  ├─ agents.yaml          # Agent roles, goals, backstories               │
│  ├─ tasks.yaml           # Task definitions & dependencies               │
│  └─ topics_cancer.json   # Research topics configuration                 │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         LANGGRAPH WORKFLOW ENGINE                         │
├──────────────────────────────────────────────────────────────────────────┤
│  graph.py - StateGraph with 5 Stages                                     │
│                                                                           │
│  ┌────────────┐    ┌─────────────┐    ┌────────────┐    ┌──────────┐   │
│  │Initialize  │───▶│ Fetch News  │───▶│ Summarize  │───▶│Generate  │   │
│  │ Workflow   │    │ (Per Topic) │    │  Topics    │    │Newsletter│   │
│  └────────────┘    └─────────────┘    └────────────┘    └──────────┘   │
│                           │                                   │           │
│                           │                                   │           │
│                           └──────────┐              ┌────────┘           │
│                                      ▼              ▼                     │
│                              ┌──────────────────────┐                    │
│                              │   Save Outputs       │                    │
│                              │  (HTML, MD, JSON)    │                    │
│                              └──────────────────────┘                    │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                            AGENT LAYER                                    │
├──────────────────────────────────────────────────────────────────────────┤
│  agents.py                                                                │
│                                                                           │
│  ┌────────────────────┐  ┌────────────────────┐  ┌──────────────────┐  │
│  │  ResearchAgent     │  │   EditorAgent      │  │ ChiefEditorAgent │  │
│  ├────────────────────┤  ├────────────────────┤  ├──────────────────┤  │
│  │ • Search queries   │  │ • Summarize        │  │ • Generate HTML  │  │
│  │ • Analyze          │  │   articles         │  │ • Generate MD    │  │
│  │   relevance        │  │ • Extract insights │  │ • Format content │  │
│  │ • Score articles   │  │ • Executive        │  │                  │  │
│  │                    │  │   summary          │  │                  │  │
│  └────────────────────┘  └────────────────────┘  └──────────────────┘  │
│           │                        │                       │              │
│           └────────────────────────┴───────────────────────┘              │
│                                    │                                      │
│                    Uses prompts from prompts.yaml via                    │
│                         prompt_loader.py                                 │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                             TOOLS LAYER                                   │
├──────────────────────────────────────────────────────────────────────────┤
│  tools.py                                                                 │
│                                                                           │
│  ┌────────────────┐  ┌───────────────────┐  ┌─────────────────────┐    │
│  │ NewsSearchTool │  │ DocumentProcessor │  │   FileManager       │    │
│  ├────────────────┤  ├───────────────────┤  ├─────────────────────┤    │
│  │ • Tavily API   │  │ • Extract key     │  │ • Save HTML         │    │
│  │ • Serper API   │  │   points          │  │ • Save Markdown     │    │
│  │ • Search news  │  │ • Process docs    │  │ • Save JSON         │    │
│  │ • Filter by    │  │ • Categorize      │  │ • Create outputs/   │    │
│  │   domains      │  │   content         │  │   directory         │    │
│  └────────────────┘  └───────────────────┘  └─────────────────────┘    │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         EXTERNAL SERVICES                                 │
├──────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌─────────────────────────┐   │
│  │  OpenAI API  │    │  Tavily API  │    │   Research Sources      │   │
│  │              │    │              │    │                         │   │
│  │ • GPT-4o     │    │ • Search     │    │ • PubMed               │   │
│  │ • GPT-4o-mini│    │ • Advanced   │    │ • Nature.com           │   │
│  │              │    │   mode       │    │ • ScienceDirect        │   │
│  └──────────────┘    └──────────────┘    │ • NEJM                 │   │
│                                           │ • Cancer.gov           │   │
│                                           │ • NIH, ArXiv           │   │
│                                           └─────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                              OUTPUTS                                      │
├──────────────────────────────────────────────────────────────────────────┤
│  outputs/                                                                 │
│  ├─ newsletter_[timestamp].html    # Professional HTML newsletter        │
│  ├─ report_[timestamp].md          # Markdown research report            │
│  ├─ data_[timestamp].json          # Structured data export              │
│  └─ run_results_[timestamp].json   # Complete workflow results           │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Detailed Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           WORKFLOW EXECUTION                             │
└─────────────────────────────────────────────────────────────────────────┘

START: User runs `python -m ai_news_langgraph.main`
  │
  ├─ Load Environment Variables (.env)
  │  ├─ OPENAI_API_KEY
  │  ├─ TAVILY_API_KEY
  │  ├─ OPENAI_MODEL (default: gpt-4o-mini)
  │  └─ AI_NEWS_TOPIC
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: INITIALIZE WORKFLOW                                    │
├─────────────────────────────────────────────────────────────────┤
│ Function: initialize_workflow()                                 │
│                                                                 │
│ Actions:                                                        │
│ ✓ Load topics_cancer.json configuration                        │
│ ✓ Parse main_topic and sub_topics                             │
│ ✓ Initialize workflow state                                    │
│ ✓ Set current_stage = "fetch_news"                            │
│                                                                 │
│ State Updated:                                                  │
│ • topics_config: {main_topic, sub_topics[]}                    │
│ • topic_results: []                                            │
│ • current_topic_index: 0                                       │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: FETCH NEWS (Loops per topic)                          │
├─────────────────────────────────────────────────────────────────┤
│ Function: fetch_news_for_topic()                                │
│ Agent: ResearchAgent                                            │
│                                                                 │
│ For each topic in topics_config.sub_topics:                    │
│                                                                 │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 1. Create Search Query                          │         │
│   │    • ResearchAgent.create_search_queries()      │         │
│   │    • Optimize query for AI + Cancer + Topic     │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 2. Search for Articles                          │         │
│   │    • NewsSearchTool.search()                    │         │
│   │    • Call Tavily API                            │         │
│   │    • Filter by medical/research domains         │         │
│   │    • Limit to last 7 days                       │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 3. Analyze Relevance                            │         │
│   │    • For each article:                          │         │
│   │      - Load prompt: 'analyze_relevance'         │         │
│   │      - LLM scores article (0-1)                 │         │
│   │      - Keep articles with score > 0.5           │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 4. Store Results                                │         │
│   │    • TopicSearchResult {                        │         │
│   │        topic_name, articles[], article_count    │         │
│   │      }                                           │         │
│   │    • Add to state.topic_results                 │         │
│   └─────────────────────────────────────────────────┘         │
│                                                                 │
│ Loop continues until all topics processed                      │
│                                                                 │
│ State Updated:                                                  │
│ • topic_results: [TopicSearchResult, ...]                      │
│ • current_topic_index: incremented                             │
│ • current_stage: "summarize_topics"                            │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: SUMMARIZE TOPICS                                       │
├─────────────────────────────────────────────────────────────────┤
│ Function: summarize_topic_news()                                │
│ Agent: EditorAgent                                              │
│                                                                 │
│ For each topic in topic_results:                               │
│                                                                 │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 1. Summarize Articles                           │         │
│   │    • Load prompt: 'summarize_articles'          │         │
│   │    • EditorAgent.summarize_articles()           │         │
│   │    • LLM creates:                               │         │
│   │      - Overview (180-250 words)                 │         │
│   │      - Key insights (3-5 bullet points)         │         │
│   │      - Notable trends                           │         │
│   │      - Top 3 recommended readings               │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 2. Extract Key Points                           │         │
│   │    • DocumentProcessor.extract_key_points()     │         │
│   │    • Categorize findings                        │         │
│   │    • Identify breakthrough developments         │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 3. Store TopicSummary                           │         │
│   │    • topic_name, summary, highlights[]          │         │
│   │    • article_count, key_findings[]              │         │
│   └─────────────────────────────────────────────────┘         │
│                                                                 │
│ After all topics summarized:                                   │
│                                                                 │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 4. Create Executive Summary                     │         │
│   │    • Load prompt: 'executive_summary'           │         │
│   │    • EditorAgent.create_executive_summary()     │         │
│   │    • 200-250 words covering all topics          │         │
│   │    • Highlight most significant developments    │         │
│   └─────────────────────────────────────────────────┘         │
│                                                                 │
│ State Updated:                                                  │
│ • topic_summaries: [TopicSummary, ...]                         │
│ • summaries_output: {executive_summary, topics[]}              │
│ • current_stage: "generate_newsletter"                         │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: GENERATE NEWSLETTER                                    │
├─────────────────────────────────────────────────────────────────┤
│ Function: generate_newsletter()                                 │
│ Agent: ChiefEditorAgent                                         │
│                                                                 │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 1. Generate HTML Newsletter                     │         │
│   │    • ChiefEditorAgent.generate_newsletter_html()│         │
│   │    • Professional responsive design             │         │
│   │    • Sections for each topic                    │         │
│   │    • Executive summary at top                   │         │
│   │    • Links to source articles                   │         │
│   │    • Mobile-responsive CSS                      │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 2. Generate Markdown Report                     │         │
│   │    • ChiefEditorAgent.generate_markdown_report()│         │
│   │    • Same content, markdown format              │         │
│   │    • Easy to archive and share                  │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 3. Create Structured Data Export                │         │
│   │    • JSON format with all data                  │         │
│   │    • Topics, articles, summaries                │         │
│   │    • Metadata and timestamps                    │         │
│   └─────────────────────────────────────────────────┘         │
│                                                                 │
│ State Updated:                                                  │
│ • newsletter_content: NewsletterContent                        │
│ • current_stage: "save_outputs"                                │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 5: SAVE OUTPUTS                                           │
├─────────────────────────────────────────────────────────────────┤
│ Function: save_outputs()                                        │
│                                                                 │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 1. Create outputs/ directory                    │         │
│   │    • FileManager.ensure_directory()             │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 2. Save Files with Timestamps                   │         │
│   │    • newsletter_YYYYMMDD_HHMMSS.html            │         │
│   │    • report_YYYYMMDD_HHMMSS.md                  │         │
│   │    • data_YYYYMMDD_HHMMSS.json                  │         │
│   │    • run_results_YYYYMMDD_HHMMSS.json           │         │
│   └─────────────────────────────────────────────────┘         │
│                     │                                           │
│                     ▼                                           │
│   ┌─────────────────────────────────────────────────┐         │
│   │ 3. Log Results                                  │         │
│   │    • Print file paths                           │         │
│   │    • Show agent performance metrics             │         │
│   │    • Display execution times                    │         │
│   │    • Report any errors                          │         │
│   └─────────────────────────────────────────────────┘         │
│                                                                 │
│ State Updated:                                                  │
│ • outputs: {html: path, markdown: path, json: path}            │
│ • status: "completed"                                           │
│ • agent_results: [performance data]                            │
└─────────────────────────────────────────────────────────────────┘
  │
  ▼
END: Workflow Complete ✅
  │
  └─ User receives:
     • Professional HTML newsletter
     • Markdown research report
     • Structured JSON data
     • Complete workflow results
```

---

## 🎯 Prompt Loading Flow (NEW!)

```
┌──────────────────────────────────────────────────────────────┐
│              YAML-BASED PROMPT MANAGEMENT                     │
└──────────────────────────────────────────────────────────────┘

Agent needs a prompt
  │
  ▼
┌────────────────────────────────────────┐
│ from prompt_loader import load_prompt  │
└────────────────────────────────────────┘
  │
  ▼
┌───────────────────────────────────────────────────────┐
│ load_prompt('research_agent', 'analyze_relevance')    │
└───────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────┐
│ PromptLoader                                           │
│  1. Reads config/prompts.yaml                         │
│  2. Finds agent section: research_agent               │
│  3. Finds prompt: analyze_relevance                   │
│  4. Extracts system & human messages                  │
│  5. Creates ChatPromptTemplate                        │
└────────────────────────────────────────────────────────┘
  │
  ▼
┌────────────────────────────────────────────────────────┐
│ Returns ChatPromptTemplate ready for LLM              │
│  • system: "You are {role}. {backstory}"             │
│  • human: "Score this article's relevance..."        │
└────────────────────────────────────────────────────────┘
  │
  ▼
Agent uses prompt:
  chain = prompt | llm
  response = chain.invoke({variables})
```

---

## 📊 Data Flow Diagram

```
┌──────────┐     ┌──────────────┐     ┌─────────────┐     ┌───────────┐
│  Topics  │────▶│    Search    │────▶│   Filter    │────▶│  Articles │
│  Config  │     │   (Tavily)   │     │  (LLM Score)│     │  Per Topic│
└──────────┘     └──────────────┘     └─────────────┘     └───────────┘
                                                                  │
                                                                  ▼
┌──────────┐     ┌──────────────┐     ┌─────────────┐     ┌───────────┐
│ Newsletter│◀────│   Format     │◀────│  Executive  │◀────│   Topic   │
│ HTML + MD │     │   (HTML/MD)  │     │   Summary   │     │ Summaries │
└──────────┘     └──────────────┘     └─────────────┘     └───────────┘
      │
      ▼
┌──────────┐
│ outputs/ │
│  Files   │
└──────────┘
```

---

## 🔧 Technology Stack

```
┌─────────────────────────────────────────────────────────┐
│ FRAMEWORK & ORCHESTRATION                               │
├─────────────────────────────────────────────────────────┤
│ • LangGraph - Workflow orchestration & state management │
│ • LangChain - LLM integration & tool management         │
│ • Pydantic - Data validation & models                   │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ LLMs & APIs                                             │
├─────────────────────────────────────────────────────────┤
│ • OpenAI (GPT-4o, GPT-4o-mini) - Content generation    │
│ • Tavily - Search API for research articles            │
│ • Serper (optional) - Fallback search                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ CONFIGURATION & DATA                                    │
├─────────────────────────────────────────────────────────┤
│ • YAML - Prompts, agents, tasks configuration          │
│ • JSON - Topics configuration & data export            │
│ • Python-dotenv - Environment variable management      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ PYTHON LIBRARIES                                        │
├─────────────────────────────────────────────────────────┤
│ • PyYAML - YAML parsing                                │
│ • Requests - HTTP requests                             │
│ • DateTime - Timestamp management                      │
└─────────────────────────────────────────────────────────┘
```

---

## 🎭 Agent Roles & Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                     RESEARCH AGENT                          │
├─────────────────────────────────────────────────────────────┤
│ Role: Junior AI News Researcher                            │
│ Goal: Discover recent, relevant AI news in Cancer care     │
│                                                             │
│ Responsibilities:                                           │
│ • Generate optimized search queries                        │
│ • Search medical/research domains                          │
│ • Analyze article relevance (LLM scoring)                  │
│ • Filter and rank results                                  │
│                                                             │
│ Prompts Used:                                              │
│ • analyze_relevance                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                      EDITOR AGENT                           │
├─────────────────────────────────────────────────────────────┤
│ Role: Senior AI Researcher                                 │
│ Goal: Curate and editorialize top findings                 │
│                                                             │
│ Responsibilities:                                           │
│ • Summarize articles per topic                             │
│ • Extract key insights & trends                            │
│ • Identify breakthrough developments                       │
│ • Create executive summary                                 │
│ • Recommend further reading                                │
│                                                             │
│ Prompts Used:                                              │
│ • summarize_articles                                       │
│ • executive_summary                                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   CHIEF EDITOR AGENT                        │
├─────────────────────────────────────────────────────────────┤
│ Role: Chief Editor of AI Digest Weekly                    │
│ Goal: Create professional, engaging newsletter             │
│                                                             │
│ Responsibilities:                                           │
│ • Generate HTML newsletter with styling                    │
│ • Create markdown report                                   │
│ • Format content professionally                            │
│ • Ensure mobile responsiveness                             │
│ • Add proper citations & links                             │
│                                                             │
│ Prompts Used:                                              │
│ • refine_content (available in prompts.yaml)              │
│ • generate_subject_line (available in prompts.yaml)       │
└─────────────────────────────────────────────────────────────┘
```

---

## 📝 Key Files Reference

| File | Purpose | Key Components |
|------|---------|----------------|
| `main.py` | Entry point | CLI, env loading, orchestration |
| `graph.py` | Workflow engine | StateGraph, node functions, routing |
| `agents.py` | Agent definitions | ResearchAgent, EditorAgent, ChiefEditorAgent |
| `tools.py` | Tool implementations | NewsSearchTool, DocumentProcessor, FileManager |
| `prompt_loader.py` | Prompt management | PromptLoader, load_prompt() |
| `schemas.py` | Data models | Pydantic models for validation |
| `models.py` | Domain models | NewsItem, SubTopic definitions |
| `config/prompts.yaml` | ⭐ All prompts | System & human message templates |
| `config/agents.yaml` | Agent configs | Roles, goals, backstories |
| `config/tasks.yaml` | Task definitions | Descriptions, dependencies |
| `config/topics_cancer.json` | Research topics | Topic names, queries |

---

## 🚀 Execution Example

```bash
# User runs the application
$ python -m ai_news_langgraph.main

# System executes:

✅ Loaded .env from current directory
🚀 Starting AI News Multi-Agent Research System...
============================================================
📋 Main Topic: AI in Cancer Care
📁 Topics Config: .../config/topics_cancer.json
============================================================

# Stage 1: Initialize
[Initializing] Loading topics configuration...
[Initializing] Found 5 sub-topics to research

# Stage 2: Fetch News (per topic)
[Research Agent] Searching: Cancer Research...
[Research Agent] Found 12 articles, analyzing relevance...
[Research Agent] Kept 8 relevant articles (score > 0.5)
[Research Agent] Searching: Early Detection...
[Research Agent] Found 10 articles, analyzing relevance...
[Research Agent] Kept 7 relevant articles (score > 0.5)
... (continues for all topics)

# Stage 3: Summarize Topics
[Editor Agent] Summarizing Cancer Research findings...
[Editor Agent] Creating executive summary...

# Stage 4: Generate Newsletter
[Chief Editor] Generating HTML newsletter...
[Chief Editor] Generating Markdown report...

# Stage 5: Save Outputs
[FileManager] Saving to outputs/newsletter_20241009_123045.html
[FileManager] Saving to outputs/report_20241009_123045.md
[FileManager] Saving to outputs/data_20241009_123045.json

✅ Workflow Completed!
============================================================
📊 Status: Success

📁 Generated Files:
  - html: outputs/newsletter_20241009_123045.html
  - markdown: outputs/report_20241009_123045.md
  - json: outputs/data_20241009_123045.json

🤖 Agent Performance:
  - research_assistant: fetch_ai_news (45.23s)
  - editor_assistant: summarize_ai_news (32.15s)
  - chief_editor: generate_newsletter (18.67s)

💾 Full results saved to: outputs/run_results_20241009_123045.json
```

---

## 🔒 Security & Best Practices

1. **API Keys**: Stored in `.env`, never committed to git
2. **Error Handling**: Each stage has try-catch with fallbacks
3. **Rate Limiting**: API calls are controlled and logged
4. **Data Validation**: Pydantic models ensure type safety
5. **State Management**: LangGraph tracks complete workflow state
6. **Checkpointing**: Can resume from any stage if interrupted
7. **Logging**: Detailed logs for debugging and monitoring

---

This architecture enables a scalable, maintainable, and extensible system for AI-powered research aggregation and newsletter generation!

