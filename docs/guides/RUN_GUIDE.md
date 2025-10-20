# How to Run the AI Cancer Newsletter App 🚀

## Quick Start (2 minutes)

### Prerequisites
- Python 3.9+
- OpenAI API Key (`sk-proj-...`)
- Terminal/Command line

### Step 1: Set Up Environment
```bash
# Navigate to project directory
cd AI_NEWS_LANGGRAPH

# Set your OpenAI API key
export OPENAI_API_KEY="sk-proj-your-key-here"

# Optional: Set Replicate token for Flux images
export REPLICATE_API_TOKEN="r8_your-token-here"

# Optional: Set LangSmith API key for tracing
export LANGSMITH_API_KEY="lsv2_pt_your-key-here"
```

### Step 2: Start the App
```bash
# Using uv (recommended)
uv run streamlit run final_newsletter_app.py --server.port 8501

# Or using Python directly
python -m streamlit run final_newsletter_app.py --server.port 8501
```

### Step 3: Open in Browser
```
http://localhost:8501
```

### Step 4: Generate Newsletter
1. Look at the **left sidebar**
2. Click **"🚀 Generate Newsletter"** button
3. Wait 2-5 minutes for generation
4. **Newsletter displays on the page** with:
   - Metrics dashboard
   - Executive summary
   - Topic details (in tabs)
   - Medical glossary
   - Download button for HTML

---

## Full Setup Guide

### Installation

#### Option A: Using uv (Fastest)
```bash
# Install uv if needed
brew install uv  # macOS
# or: choco install uv  # Windows
# or: pip install uv

# Navigate to project
cd AI_NEWS_LANGGRAPH

# Install dependencies
uv sync

# Run app
uv run streamlit run final_newsletter_app.py
```

#### Option B: Using pip + venv
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or: .venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run final_newsletter_app.py
```

### Configuration

#### Required: OpenAI API Key
```bash
# Add to .env file
OPENAI_API_KEY=sk-proj-your-key-here
```

Get your key from: https://platform.openai.com/api-keys

#### Optional: Replicate Token (for Flux images)
```bash
# Add to .env file
REPLICATE_API_TOKEN=r8_your-token-here
```

Get your token from: https://replicate.com/account/api-tokens

#### Optional: LangSmith API Key (for tracing)
```bash
# Add to .env file
LANGSMITH_API_KEY=lsv2_pt_your-key-here
```

Get your key from: https://smith.langchain.com/

---

## Running the App

### Start Streamlit
```bash
# From the AI_NEWS_LANGGRAPH directory
uv run streamlit run final_newsletter_app.py --server.port 8501
```

### Expected Output
```
Local URL: http://localhost:8501
Network URL: http://10.x.x.x:8501
```

### Access the App
Open your browser and go to:
```
http://localhost:8501
```

---

## Using the App

### Step 1: Check Sidebar
- **Observability**: LangSmith status (if configured)
- **Topics**: Shows loaded topics from config
- **Generate Button**: Red button with "🚀 Generate Newsletter"

### Step 2: Generate Newsletter
Click the **"🚀 Generate Newsletter"** button

You'll see:
```
🔄 Generating newsletter... This may take 2-5 minutes
```

The workflow will:
1. 🔍 Fetch latest research articles
2. 📝 Summarize findings
3. ✏️ Edit and refine content
4. ⭐ Rate quality
5. 🖼️ Generate cover image
6. 📊 Create knowledge graph
7. 📖 Generate glossary

### Step 3: View Newsletter
Once complete, you'll see:

**📊 Newsletter Metrics**
- Articles analyzed
- Topics covered
- Average quality
- Glossary terms

**📋 Executive Summary**
- High-level overview of all topics

**🔍 Detailed Analysis**
- 5 tabs (one per topic)
- Each tab shows:
  - Topic overview
  - Key findings
  - Notable trends
  - Top articles with links

**📖 Medical Glossary**
- 15 medical/AI terms
- AI-generated definitions
- Related terms
- Term type (Diagnostic, Treatment, etc.)

**⬇️ Download Button**
- Save full newsletter as HTML
- Can open in any browser

### Step 4: Explore Saved Newsletters
Click **"📊 Saved Newsletters"** tab to:
- See list of previous newsletters
- Click to view any past newsletter
- All newsletters saved in `outputs/`

---

## Different Newsletters

You can generate different types by modifying configuration:

### Config File Topics (Default)
Loads 5 configured topics from:
```
src/ai_news_langgraph/config/topics_cancer.json
```

Configured topics:
- Early Detection with AI
- Precision Treatment Planning
- Clinical Trials & Research
- Prevention & Screening
- Patient Outcomes & Recovery

### All Newsletters Save To
```
outputs/newsletter_YYYYMMDD_HHMMSS.html
```

Find them:
```bash
# List all newsletters (most recent first)
ls -lt outputs/newsletter_*.html | head -10

# Open latest
open outputs/newsletter_*.html | head -1 | xargs open
```

---

## Troubleshooting

### App Won't Start

**Error: "Port 8501 is already in use"**
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Then start again
uv run streamlit run final_newsletter_app.py
```

**Error: "No module named 'langchain_openai'"**
```bash
# Reinstall dependencies
uv sync --refresh

# Or with pip
pip install langchain-openai langchain-core langgraph
```

### Generation Issues

**Error: "OPENAI_API_KEY not found"**
```bash
# Check if key is set
echo $OPENAI_API_KEY

# If empty, set it
export OPENAI_API_KEY="sk-proj-..."

# Then restart app
```

**Generation takes too long**
- Normal time: 2-5 minutes
- Check network connection
- Check OpenAI API status

**No glossary appearing**
- Glossary appears at bottom of newsletter
- Scroll down to see it
- It's embedded directly in the display

### Display Issues

**Content not showing on page**
- Refresh browser (Cmd+R or Ctrl+R)
- Check sidebar for errors
- Look at terminal output for error messages

**Newsletter only in preview**
- Using old app version
- Use `final_newsletter_app.py` (not `streamlit_newsletter_app.py`)
- Restart with correct app file

---

## Environment Variables

### Required
```bash
OPENAI_API_KEY=sk-proj-your-key
```

### Optional
```bash
# For Flux image generation
REPLICATE_API_TOKEN=r8_your-token

# For observability tracing
LANGSMITH_API_KEY=lsv2_pt_your-key

# For knowledge graph exports
EXPORT_KNOWLEDGE_GRAPH=true

# For custom project name
LANGCHAIN_PROJECT=My-Project-Name
```

### Set in .env File
Create `.env` in the project root:
```bash
cat > .env << EOF
OPENAI_API_KEY=sk-proj-your-key-here
REPLICATE_API_TOKEN=r8_your-token-here
LANGSMITH_API_KEY=lsv2_pt_your-key-here
EOF
```

---

## Advanced Usage

### Custom Port
```bash
# Use different port
uv run streamlit run final_newsletter_app.py --server.port 9000

# Then access at: http://localhost:9000
```

### Run in Background
```bash
# macOS/Linux
uv run streamlit run final_newsletter_app.py &

# Windows (PowerShell)
Start-Process powershell -ArgumentList "uv run streamlit run final_newsletter_app.py"
```

### Development Mode
```bash
# With hot reload disabled (more stable)
uv run streamlit run final_newsletter_app.py --logger.level=debug
```

### Check Status
```bash
# Is Streamlit running?
lsof -i:8501

# Kill if needed
kill -9 $(lsof -t -i:8501)
```

---

## File Structure

```
AI_NEWS_LANGGRAPH/
├── final_newsletter_app.py          ← USE THIS (main app)
├── streamlit_newsletter_app.py       ← Old version (don't use)
├── simple_newsletter_app.py          ← Simplified version
├── src/
│   └── ai_news_langgraph/
│       ├── nodes_v2.py              ← Workflow nodes
│       ├── workflow.py              ← Main workflow
│       ├── html_generator.py         ← HTML newsletter generation
│       ├── glossary_generator.py     ← Glossary generation
│       ├── langsmith_observability.py ← LangSmith integration
│       ├── config/
│       │   └── topics_cancer.json    ← Newsletter topics
│       └── ...
├── outputs/
│   ├── newsletter_*.html             ← Generated newsletters
│   ├── images/                       ← Cover images
│   └── knowledge_graphs/             ← Knowledge graph JSON
├── .env                              ← API keys (create this)
├── LANGSMITH_SETUP.md                ← LangSmith guide
├── LANGSMITH_QUICK_START.md          ← Quick LangSmith ref
└── RUN_GUIDE.md                      ← This file
```

---

## What Each File Does

| File | Purpose |
|------|---------|
| `final_newsletter_app.py` | Main Streamlit app - USE THIS |
| `nodes_v2.py` | Workflow nodes (research, summarize, etc.) |
| `workflow.py` | LangGraph workflow orchestration |
| `html_generator.py` | Converts content to HTML newsletter |
| `glossary_generator.py` | AI-powered glossary generation |
| `langsmith_observability.py` | LangSmith tracing integration |
| `topics_cancer.json` | Newsletter topics configuration |

---

## Commands Reference

```bash
# Start app
uv run streamlit run final_newsletter_app.py

# Different port
uv run streamlit run final_newsletter_app.py --server.port 9000

# Kill app
pkill -f streamlit

# Check if running
lsof -i:8501

# List newsletters
ls -lt outputs/newsletter_*.html

# View latest newsletter
open outputs/newsletter_*.html | sort -r | head -1 | xargs open

# Check config topics
cat src/ai_news_langgraph/config/topics_cancer.json

# View environment variables
echo $OPENAI_API_KEY
echo $LANGSMITH_API_KEY
```

---

## Monitoring While Running

### In Terminal
```bash
# Watch the logs as they appear
# Shows progress of newsletter generation
# Errors will be highlighted in red
```

### In Browser
```bash
# Sidebar shows:
# - Observability status
# - Topics loaded
# - Current generation progress

# Main page shows:
# - Live generation status
# - Final results once complete
```

### Viewing Generated Files
```bash
# Check what was generated
ls -lh outputs/newsletter_*.html | tail -5

# Check file size
du -h outputs/newsletter_*.html | tail -5
```

---

## Performance Tips

### Faster Generation
1. Reduce number of topics in config
2. Use simpler prompts
3. Disable Flux image generation (use DALL-E only)

### Better Results
1. Ensure good internet connection
2. Use GPT-4 tier API key
3. Add more topics for richer content

### Storage
- Each newsletter: ~500KB - 2MB
- Keep outputs directory clean:
  ```bash
  # Remove old newsletters (older than 7 days)
  find outputs/newsletter_*.html -mtime +7 -delete
  ```

---

## Getting Help

### Check Documentation
- `LANGSMITH_SETUP.md` - LangSmith setup
- `LANGSMITH_QUICK_START.md` - Quick reference
- `NEWSLETTER_DISPLAY_COMPLETE.md` - Display features
- `RUN_GUIDE.md` - This file

### Debug Issues
1. Check terminal output (error messages)
2. Verify API keys are set
3. Check internet connection
4. Try refreshing the browser
5. Restart the app

### Restart Clean
```bash
# Kill all Streamlit processes
pkill -9 -f streamlit

# Wait a moment
sleep 2

# Start fresh
uv run streamlit run final_newsletter_app.py
```

---

## Summary

**To run the app:**
1. Set `OPENAI_API_KEY` in `.env`
2. Run: `uv run streamlit run final_newsletter_app.py`
3. Open: `http://localhost:8501`
4. Click: **"🚀 Generate Newsletter"**
5. Wait 2-5 minutes
6. **View content on page** (no preview needed!)
7. See **glossary at bottom**
8. **Download as HTML** if needed

That's it! 🎉

---

**Happy newsletter generating!** 📰✨