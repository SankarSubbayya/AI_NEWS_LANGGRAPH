# Troubleshooting Guide

## ⚠️ Common Issues and Solutions

### Issue 1: GraphRecursionError - Recursion Limit Exceeded

**Error Message:**
```
langgraph.errors.GraphRecursionError: Recursion limit of 25 reached without hitting a stop condition.
```

**Cause:**
The application processes **5 topics** sequentially in a loop:
- Fetch news for Topic 1
- Summarize Topic 1
- Fetch news for Topic 2
- Summarize Topic 2
- ... (continues for all 5 topics)

Each topic requires ~10 graph steps, so 5 topics = ~50 steps, which exceeds LangGraph's default recursion limit of 25.

**✅ FIXED:**
Updated `graph.py` line 562 to increase recursion limit to 100:
```python
config = {
    "configurable": {"thread_id": "research_thread_1"},
    "recursion_limit": 100  # Increased from default 25
}
```

**Alternative Solution:**
Reduce number of topics in `topics_cancer.json` for faster testing:
```json
{
  "main_topic": "AI in Cancer Care",
  "sub_topics": [
    {
      "name": "Cancer Research",
      "description": "AI in oncology research",
      "query": "+AI cancer research oncology"
    }
  ]
}
```

---

### Issue 2: Tavily API Unauthorized Error

**Error Message:**
```
Tavily search error: Unauthorized: missing or invalid API key.
```

**Cause:**
- API key not set in `.env`
- API key has expired
- API key format is incorrect

**Solution:**

1. **Check your API key:**
```bash
cat .env | grep TAVILY_API_KEY
```

2. **Verify it's not a placeholder:**
```bash
# Bad (placeholder):
TAVILY_API_KEY="your-tavily-api-key-here"

# Good (real key):
TAVILY_API_KEY="tvly-abc123..."
```

3. **Get a new API key:**
   - Go to [https://tavily.com/](https://tavily.com/)
   - Sign up or log in
   - Get your API key from the dashboard

4. **Update your `.env`:**
```bash
# Remove old line
sed -i '' '/TAVILY_API_KEY/d' .env

# Add new key
echo 'TAVILY_API_KEY="tvly-your-real-key-here"' >> .env
```

5. **Verify:**
```bash
# Test the key
uv run python -c "
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()
client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
result = client.search('test')
print('✅ Tavily API key works!')
"
```

---

### Issue 3: OpenAI API Key Error

**Error Message:**
```
openai.OpenAIError: The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable
```

**Solution:**

1. **Check `.env` file:**
```bash
cat .env | grep OPENAI_API_KEY
```

2. **Add your OpenAI key:**
```bash
echo 'OPENAI_API_KEY="sk-proj-..."' >> .env
```

3. **Get a key:**
   - Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Create a new API key
   - Copy and paste into `.env`

---

### Issue 4: Application Takes Too Long

**Symptom:**
Application runs for several minutes and seems stuck.

**Cause:**
Processing 5 topics with web searches and LLM analysis takes time:
- Each topic: ~30-60 seconds
- 5 topics: ~3-5 minutes total
- Plus summarization and newsletter generation: +2-3 minutes
- **Total expected time: 5-8 minutes**

**Solutions:**

**Option 1: Use fewer topics (fastest)**
```bash
# Create test config with 1 topic
cat > test_1_topic.json << 'EOF'
{
  "main_topic": "AI in Healthcare",
  "sub_topics": [
    {
      "name": "Medical Imaging",
      "description": "AI in medical imaging",
      "query": "+AI medical imaging diagnosis"
    }
  ]
}
EOF

# Run with test config
uv run python -m ai_news_langgraph.main --config test_1_topic.json
```

**Option 2: Reduce timeouts**
Edit `config/tasks.yaml`:
```yaml
fetch_ai_news:
  timeout_seconds: 60  # Reduce from 300
  
summarize_ai_news:
  timeout_seconds: 60  # Reduce from 240
```

**Option 3: Limit search results**
Edit `graph.py`, find `news_tool.search()` calls and reduce `max_results`:
```python
results = news_tool.search(
    query=topic["query"],
    max_results=5,  # Reduce from 10
    days_back=7
)
```

---

### Issue 5: Module Not Found Error

**Error Message:**
```
ModuleNotFoundError: No module named 'ai_news_langgraph'
```

**Solution:**

1. **Reinstall the package:**
```bash
uv pip install -e .
```

2. **Verify installation:**
```bash
uv run python -c "import ai_news_langgraph; print('✅ Package installed')"
```

3. **Check you're in the right directory:**
```bash
pwd
# Should be: .../AI_NEWS_LANGGRAPH

ls pyproject.toml
# Should exist
```

---

### Issue 6: No Output Files Generated

**Symptom:**
Application completes but no files in `outputs/` directory.

**Solution:**

1. **Check for errors:**
```bash
uv run python -m ai_news_langgraph.main 2>&1 | tee run.log
grep -i error run.log
```

2. **Create outputs directory:**
```bash
mkdir -p outputs
```

3. **Check file permissions:**
```bash
ls -ld outputs/
# Should be writable
```

4. **Verify workflow completed:**
Look for this in output:
```
✅ Workflow Completed!
📁 Generated Files:
  - html: outputs/newsletter_...html
```

---

### Issue 7: Import Errors for New Modules

**Error Message:**
```
ImportError: cannot import name 'load_task_config' from 'ai_news_langgraph.task_loader'
```

**Solution:**

1. **Reinstall after code changes:**
```bash
uv pip install -e .
```

2. **Clear Python cache:**
```bash
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete
```

3. **Restart Python:**
If running in REPL or notebook, restart the kernel.

---

### Issue 8: YAML/JSON Parsing Errors

**Error Message:**
```
yaml.scanner.ScannerError: while scanning for the next token
```

**Solution:**

1. **Validate YAML:**
```bash
uv run python -c "import yaml; yaml.safe_load(open('src/ai_news_langgraph/config/tasks.yaml'))"
```

2. **Validate JSON:**
```bash
uv run python -c "import json; json.load(open('src/ai_news_langgraph/config/topics_cancer.json'))"
```

3. **Check for:**
   - Incorrect indentation (YAML)
   - Missing commas (JSON)
   - Trailing commas (JSON)
   - Special characters not escaped

---

## 🔍 Debug Mode

### Enable Verbose Logging

Add this to `graph.py` at the top:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Individual Components

**Test Tasks:**
```bash
uv run python -c "
from ai_news_langgraph.task_loader import get_task_loader
loader = get_task_loader()
print('Tasks:', loader.list_tasks())
print('Order:', loader.get_execution_order())
"
```

**Test Topics:**
```bash
uv run python -c "
from ai_news_langgraph.graph import _load_topics
topics = _load_topics('src/ai_news_langgraph/config/topics_cancer.json')
print(f'Loaded {len(topics[\"sub_topics\"])} topics')
"
```

**Test Prompts:**
```bash
uv run python -c "
from ai_news_langgraph.prompt_loader import load_prompt
prompt = load_prompt('research_agent', 'analyze_relevance')
print('✅ Prompt loaded')
"
```

---

## 📊 Performance Monitoring

### Track Execution Time

```bash
time uv run python -m ai_news_langgraph.main
```

### Monitor Progress

The application logs task execution:
```
============================================================
📋 Task: fetch_ai_news
   Agent: research_assistant (ResearchAgent)
   Timeout: 300s
   Retry: 2 attempts
============================================================
```

Watch for:
- ✅ Task starts: Good
- ⚠️ No progress for > 5 mins: Possible timeout/error
- ❌ Recursion error: Increase limit (already fixed)

---

## 🚨 Quick Diagnostics

Run this diagnostic script:
```bash
uv run python << 'EOF'
import os
from pathlib import Path
from dotenv import load_dotenv

print("🔍 AI News LangGraph Diagnostics")
print("=" * 60)

# Check .env
load_dotenv()
print("\n1. Environment Variables:")
print(f"   OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
print(f"   TAVILY_API_KEY: {'✅ Set' if os.getenv('TAVILY_API_KEY') else '❌ Missing'}")

# Check files
print("\n2. Configuration Files:")
files = [
    'src/ai_news_langgraph/config/tasks.yaml',
    'src/ai_news_langgraph/config/prompts.yaml',
    'src/ai_news_langgraph/config/topics_cancer.json',
    'src/ai_news_langgraph/config/agents.yaml'
]
for f in files:
    exists = Path(f).exists()
    print(f"   {f}: {'✅' if exists else '❌'}")

# Check module
print("\n3. Module Installation:")
try:
    import ai_news_langgraph
    print("   ai_news_langgraph: ✅ Installed")
except ImportError:
    print("   ai_news_langgraph: ❌ Not installed")

# Check dependencies
print("\n4. Key Dependencies:")
deps = ['langgraph', 'langchain', 'tavily', 'pydantic', 'yaml']
for dep in deps:
    try:
        __import__(dep)
        print(f"   {dep}: ✅")
    except ImportError:
        print(f"   {dep}: ❌")

print("\n" + "=" * 60)
print("Run 'uv pip install -e .' if any modules are missing")
EOF
```

---

## 📞 Getting Help

If you're still stuck:

1. **Check the logs:** Look for specific error messages
2. **Run diagnostics:** Use the script above
3. **Simplify:** Try with 1 topic first
4. **Check API quotas:** Ensure you haven't hit limits
5. **Review docs:** See README.md, ARCHITECTURE.md, INTEGRATION_SUMMARY.md

---

## ✅ Expected Behavior

When working correctly, you should see:

```
✅ Loaded .env from current directory
🚀 Starting AI News Multi-Agent Research System...
============================================================
📋 Main Topic: Artificial Intelligence in Cancer Care
📁 Topics Config: .../topics_cancer.json
============================================================
📋 Validating task configurations...
✅ All task dependencies valid
📊 Task execution order: fetch_ai_news → summarize_ai_news → ...

============================================================
📋 Task: fetch_ai_news
   Agent: research_assistant (ResearchAgent)
   Timeout: 300s
   Retry: 2 attempts
============================================================

[Progress continues for each topic...]

✅ Workflow Completed!
============================================================
📊 Status: Success

📁 Generated Files:
  - html: outputs/newsletter_20241009_123045.html
  - markdown: outputs/report_20241009_123045.md
  - json: outputs/data_20241009_123045.json
```

**Total expected runtime:** 5-10 minutes for 5 topics

