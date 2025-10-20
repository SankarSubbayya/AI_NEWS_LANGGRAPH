# Quick Reference Guide 📚

## 🚀 Start the App (1 Command)

```bash
uv run streamlit run final_newsletter_app.py
```

**Then open:** http://localhost:8501

---

## 📖 What You Need to Know

### Setup (One-Time)
```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-proj-your-key-here"

# Optional: LangSmith for tracing
export LANGSMITH_API_KEY="lsv2_pt_your-key-here"

# Optional: Replicate for Flux images
export REPLICATE_API_TOKEN="r8_your-token-here"
```

### Run (Every Time)
```bash
uv run streamlit run final_newsletter_app.py
```

### Use
1. Click **"🚀 Generate Newsletter"** in sidebar
2. Wait 2-5 minutes
3. **View content on page**
4. Scroll to see:
   - Metrics (top)
   - Executive summary
   - 5 topic tabs
   - Glossary (bottom)
5. Download HTML if needed

---

## 📂 Important Files

| File | What It Does |
|------|-------------|
| `final_newsletter_app.py` | **USE THIS** - Main Streamlit app |
| `.env` | Create this with API keys |
| `RUN_GUIDE.md` | Full setup instructions |
| `LANGSMITH_QUICK_START.md` | LangSmith setup (optional) |

---

## 🔧 Troubleshooting

**"Port 8501 already in use"**
```bash
pkill -f streamlit
```

**"OPENAI_API_KEY not found"**
```bash
export OPENAI_API_KEY="sk-proj-..."
```

**App won't start**
```bash
uv sync --refresh
```

**Kill everything and restart**
```bash
pkill -9 -f streamlit
sleep 2
uv run streamlit run final_newsletter_app.py
```

---

## 📊 What Gets Generated

✅ **Newsletter HTML** - Download-ready
✅ **Cover Image** - AI-generated (DALL-E)
✅ **Executive Summary** - AI-written overview
✅ **5 Topics** - With findings, trends, articles
✅ **Glossary** - 15 AI-defined medical terms
✅ **Knowledge Graph** - Entity relationships (JSON)
✅ **Metrics** - Quality scores, article count

---

## 🔗 Important Links

| Resource | URL |
|----------|-----|
| **Your App** | http://localhost:8501 |
| **LangSmith** | https://smith.langchain.com/ |
| **OpenAI Keys** | https://platform.openai.com/api-keys |
| **Replicate** | https://replicate.com/account/api-tokens |

---

## ⌚ Timeline

```
Click Generate
    ↓
0-10s   → Initializing workflow
10-20s  → Fetching research articles
20-40s  → Summarizing findings
40-60s  → Editing content
60-80s  → Quality review
80-120s → Generating cover image
120-200s→ Building knowledge graph
200-300s→ Creating glossary
    ↓
Display on page!
```

**Total Time: 2-5 minutes**

---

## 📱 In Your Browser

### Sidebar
- **Observability**: LangSmith status
- **Topics**: Shows 5 loaded topics
- **Generate**: Red button to start

### Main Page
**Tab 1: Newsletter**
- 📊 Metrics at top
- 📋 Executive summary
- 🔍 5 topic tabs
- 📖 Glossary at bottom

**Tab 2: Saved Newsletters**
- List of past newsletters
- Click to view any

---

## 💾 Where Files Go

```
outputs/
├── newsletter_20251019_123456.html  ← Your newsletters
├── newsletter_20251019_120000.html
├── newsletter_20251019_110000.html
├── images/
│   └── dalle_cover_*.png            ← Cover images
└── knowledge_graphs/
    └── newsletter_*.json             ← Knowledge graphs
```

---

## 🔍 Topics Generated

Each newsletter covers 5 cancer care topics:
1. **Early Detection with AI** - AI for diagnosis
2. **Precision Treatment** - Personalized medicine
3. **Clinical Trials** - Research progress
4. **Prevention & Screening** - Early intervention
5. **Patient Outcomes** - Recovery and survival

---

## 🎯 Features

### Newsletter Content
- ✅ AI-generated from real news
- ✅ Quality scored (0-100%)
- ✅ Top articles linked
- ✅ Key findings highlighted
- ✅ Notable trends included

### Visual Design
- ✅ Beautiful gradient header
- ✅ Card-based layout
- ✅ Color-coded quality badges
- ✅ Responsive design (mobile-friendly)
- ✅ Professional styling

### Data Features
- ✅ 15 medical terms glossary
- ✅ Knowledge graph with entities
- ✅ Article relevance scores
- ✅ Trend analysis
- ✅ Quality metrics

---

## 🌐 Observability (Optional)

### Without LangSmith
- ✅ App works fine
- ✅ Newsletter generates normally
- Sidebar shows: "⚠️ LangSmith not configured"

### With LangSmith
- ✅ All AI operations traced
- ✅ Dashboard shows in sidebar
- ✅ Track token usage & costs
- ✅ See LLM calls & responses

**To enable:**
1. Get API key: https://smith.langchain.com/
2. Set: `export LANGSMITH_API_KEY="lsv2_pt_..."`
3. Restart app

---

## 📞 Common Tasks

### Generate First Newsletter
```bash
uv run streamlit run final_newsletter_app.py
# Click button
# Wait
# Enjoy!
```

### Generate Another
1. Go to http://localhost:8501
2. Click "Generate Newsletter" again
3. Wait
4. New one appears!

### View Old Newsletter
1. Click "Saved Newsletters" tab
2. See list of past newsletters
3. Click "View" to see it

### Download Newsletter
1. Scroll to bottom of generated newsletter
2. Click "⬇️ Download Full Newsletter (HTML)"
3. Opens in browser or downloads

### Stop the App
```bash
Ctrl+C  # In terminal
# or
pkill -f streamlit
```

---

## 🆘 Getting Help

**Check:**
1. `RUN_GUIDE.md` - Full instructions
2. `LANGSMITH_QUICK_START.md` - LangSmith help
3. Terminal output - Error messages
4. Browser console - JavaScript errors

**Debug:**
```bash
# See all environment variables
env | grep -E "OPENAI|LANGSMITH|REPLICATE"

# Check app is running
lsof -i:8501

# View recent newsletters
ls -lt outputs/newsletter_*.html | head -5

# Check config
cat src/ai_news_langgraph/config/topics_cancer.json
```

---

## ✨ That's It!

**You're all set!**

Just:
1. Set API key
2. Run: `uv run streamlit run final_newsletter_app.py`
3. Click button
4. Enjoy your AI-generated newsletter!

🚀 **Happy newsletter generating!**