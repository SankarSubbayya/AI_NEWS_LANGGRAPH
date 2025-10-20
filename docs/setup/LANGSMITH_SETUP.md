# LangSmith Observability Setup Guide 🔍

## What is LangSmith?

LangSmith is a cloud-based tracing and observability platform from LangChain that:
- ✅ Requires **NO local server** (unlike Phoenix)
- ✅ Automatically traces all LangChain operations
- ✅ Works with **minimal setup** (just an API key)
- ✅ Provides **real-time dashboards** and analytics
- ✅ Tracks **every LLM call**, **tokens used**, and **latency**

## Why LangSmith Over Phoenix?

| Feature | LangSmith | Phoenix |
|---------|-----------|---------|
| Setup Complexity | 🟢 Simple | 🔴 Complex |
| Local Server | ❌ Not needed | ✅ Required (port 6006) |
| Cloud Dashboard | ✅ Built-in | ❌ Optional |
| Python Compatibility | ✅ Works fine | ⚠️ Syntax errors |
| Tracing Coverage | ✅ Automatic | ⚠️ Manual |
| Cost | 🟢 Free tier available | 🟢 Free tier available |

## Setup Steps

### Step 1: Get Your LangSmith API Key

1. Go to: https://smith.langchain.com/
2. Sign up for a free account
3. Click on your profile/settings
4. Find **API Keys** section
5. Create a new API key
6. Copy the key

### Step 2: Set Environment Variable

Add your API key to `.env`:

```bash
# .env file
LANGSMITH_API_KEY=lsv2_pt_your_api_key_here
```

Or set it in your terminal:

```bash
export LANGSMITH_API_KEY="lsv2_pt_your_api_key_here"
```

### Step 3: Verify Setup

The app will automatically initialize LangSmith when you generate a newsletter. You'll see:

- ✅ In Streamlit sidebar: "LangSmith Active"
- 🔗 Dashboard link to your project
- 📊 All AI operations being traced

## What Gets Traced?

### Automatically Traced:
- ✅ **Every LLM call** (GPT-4o-mini, DALL-E)
- ✅ **Token usage** and costs
- ✅ **Prompts and responses**
- ✅ **Latency** for each operation
- ✅ **Errors and exceptions**
- ✅ **Agent execution flow**

### Dashboard Shows:
- 📊 **Traces Tab**: Timeline of operations
- 🤖 **LLM Tab**: Detailed LLM call information
- 📈 **Metrics Tab**: Token usage and costs
- ⚠️ **Errors Tab**: Any issues that occurred

## How to Use

### Generate Newsletter with Tracing

1. Open: http://localhost:8501
2. Look for **"📊 Observability"** in the sidebar
3. Click **"🚀 Generate Newsletter"**
4. Watch as operations are traced in real-time
5. Click the dashboard link to see traces

### View Your Traces

1. Go to: https://smith.langchain.com/
2. Select **"AI-News-LangGraph"** project
3. See all your newsletter generations
4. Click on any trace to inspect details

## Environment Setup

### For Production:

```bash
# .env file
LANGSMITH_API_KEY=lsv2_pt_your_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=AI-News-LangGraph
OPENAI_API_KEY=sk-proj-your-key
```

### For Development:

```bash
export LANGSMITH_API_KEY="your_key"
export LANGCHAIN_TRACING_V2="true"
export LANGCHAIN_PROJECT="AI-News-LangGraph"
```

## Viewing Real-Time Traces

### Method 1: Direct Dashboard
```
https://smith.langchain.com/projects/p/AI-News-LangGraph
```

### Method 2: From Streamlit
- Click the dashboard link in the sidebar
- Opens directly to your project

### Method 3: Command Line
```bash
# Check if tracing is working
echo $LANGSMITH_API_KEY
# Should show: lsv2_pt_...
```

## Understanding the Dashboard

### Project Overview
- Shows all traces for this project
- Filters by date, status, duration
- Export data to CSV

### Trace Details
For each newsletter generation:
- **Trace ID**: Unique identifier
- **Duration**: How long it took
- **Tokens**: Total tokens used
- **Cost**: Estimated API cost
- **Status**: Success/Failure

### LLM Calls Section
For each AI call:
- **Model**: GPT-4o-mini, DALL-E, etc.
- **Prompt**: What was asked
- **Response**: What was returned
- **Tokens**: In/Out
- **Latency**: Response time

## Cost Tracking

LangSmith FREE tier includes:
- ✅ Unlimited traces
- ✅ 30 days of history
- ✅ All analytics features
- ✅ Dashboard access

### See Your Costs:
1. Go to LangSmith dashboard
2. Look for **"Analytics"** or **"Metrics"**
3. View estimated costs by model
4. See token usage over time

## Troubleshooting

### "LangSmith not configured"
```bash
# Check if API key is set
echo $LANGSMITH_API_KEY

# If empty, set it:
export LANGSMITH_API_KEY="your_key"

# Then restart Streamlit
pkill -f streamlit
uv run streamlit run final_newsletter_app.py
```

### Dashboard shows no data
1. Generate a newsletter to create traces
2. Wait 5-10 seconds for sync
3. Refresh the dashboard
4. Check if you're in the right project

### Can't connect to LangSmith
1. Verify API key is correct
2. Check internet connection
3. Try: `curl https://smith.langchain.com/`
4. Check firewall settings

## Advanced Usage

### Custom Project Names
```python
from src.ai_news_langgraph.langsmith_observability import initialize_langsmith

observer = initialize_langsmith(project_name="My-Custom-Project")
```

### Manual Tracing
```python
from src.ai_news_langgraph.langsmith_observability import trace_node

@trace_node
def my_function():
    # This function is automatically traced
    pass
```

### View Metrics
```python
observer = st.session_state.get('langsmith_observer')
summary = observer.get_trace_summary()
print(summary)
```

## Comparing Workflows

### Without LangSmith
```
Newsletter Generation
└─ Logs to console only
```

### With LangSmith
```
Newsletter Generation
└─ Research Agent → Logged to LangSmith
└─ Summarizer → Logged to LangSmith
└─ Editor → Logged to LangSmith
└─ Quality Reviewer → Logged to LangSmith
└─ Cover Image Gen → Logged to LangSmith
└─ All visible in dashboard
```

## Next Steps

1. **Get API Key**: https://smith.langchain.com/
2. **Set LANGSMITH_API_KEY** in .env
3. **Restart Streamlit** app
4. **Generate a newsletter** to see traces
5. **View dashboard** to explore data

## Resources

- 📚 LangSmith Docs: https://docs.smith.langchain.com/
- 🔑 Get API Key: https://smith.langchain.com/
- 💬 Support: https://smith.langchain.com/support
- 📖 Examples: https://github.com/langchain-ai/langsmith-sdk

---

**That's it!** LangSmith is now integrated and ready to trace your AI newsletter generation workflow. 🚀