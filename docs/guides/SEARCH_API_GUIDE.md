# Search API Configuration Guide

## 🔍 Available Search APIs

Your AI News LangGraph system supports two search APIs with automatic fallback:

| API | Type | Best For | Pros | Cons |
|-----|------|----------|------|------|
| **Serper** | Google Search API | Broad search, latest news | More results, familiar ranking | Generic search |
| **Tavily** | AI-optimized search | Research & analysis | AI-optimized, domain filtering | Fewer results sometimes |

## ✅ Current Configuration

**You're now using Serper as primary!**

```
🔍 Search API: Serper (Google Search) with Tavily fallback
```

- **Primary**: Serper API (Google-powered search)
- **Fallback**: Tavily API (if Serper fails)

## 🎛️ Configuration Options

### Method 1: Environment Variable (Recommended)

Add to your `.env` file:

```bash
# Use Serper as primary (Google Search)
PREFERRED_SEARCH_API=serper

# OR use Tavily as primary (AI-optimized)
PREFERRED_SEARCH_API=tavily
```

### Method 2: Code-level Override

In `graph.py`, when calling `news_tool.search()`:

```python
# Force Serper
results = news_tool.search(query, prefer_serper=True)

# Force Tavily
results = news_tool.search(query, prefer_serper=False)

# Use environment variable setting (default)
results = news_tool.search(query)  # Uses PREFERRED_SEARCH_API
```

## 🔄 How Fallback Works

### With Serper Primary (Current):
```
Query → Try Serper → Success? ✅ Return results
                   → Fail? ❌ Try Tavily → Return results
```

### With Tavily Primary:
```
Query → Try Tavily → Success? ✅ Return results
                   → Fail? ❌ Try Serper → Return results
```

## 📊 API Comparison

### Serper API (Google Search)

**Advantages:**
- ✅ Powered by Google Search
- ✅ More comprehensive results
- ✅ Better for current events/news
- ✅ Familiar search result ranking
- ✅ Good for general topics

**Best for:**
- Broad research topics
- Latest news and articles
- Popular content
- General healthcare/medical research

**Example Results:**
```python
{
    "title": "Artificial intelligence in healthcare...",
    "url": "https://pmc.ncbi.nlm.nih.gov/articles/...",
    "snippet": "AI is transforming healthcare...",
    "source": "PubMed Central"
}
```

### Tavily API (AI-Optimized)

**Advantages:**
- ✅ Built specifically for AI agents
- ✅ Domain filtering (PubMed, Nature, NIH, etc.)
- ✅ Date filtering (last N days)
- ✅ Includes full content/raw_content
- ✅ Relevance scoring
- ✅ Better for specific academic queries

**Best for:**
- Academic research
- Medical journal articles
- Specific domain searches
- Recent publications (by date)

**Example Results:**
```python
{
    "title": "AI in Cancer Detection...",
    "url": "https://nature.com/articles/...",
    "content": "Full article text...",
    "raw_content": "Complete content...",
    "source": "Nature",
    "published_date": "2024-10-01",
    "score": 0.95
}
```

## 🎯 When to Use Each

### Use Serper When:
- ✅ You want maximum results
- ✅ Topic is broad (e.g., "AI in Healthcare")
- ✅ You need latest breaking news
- ✅ Google's ranking is preferred
- ✅ Topic has mainstream coverage

### Use Tavily When:
- ✅ You need academic/research sources
- ✅ You want specific domains only
- ✅ You need recent publications (by date)
- ✅ You want AI-optimized relevance
- ✅ You need full article content

## 🔧 Advanced Configuration

### Custom API Selection Per Topic

You can customize which API to use for different topics by modifying `graph.py`:

```python
# In fetch_news_for_topic() function
topic_name = current_topic["name"]

# Use Serper for broad topics
if topic_name in ["Cancer Research", "Healthcare Trends"]:
    results = news_tool.search(
        query=topic["query"],
        max_results=10,
        prefer_serper=True  # Use Serper
    )
# Use Tavily for specific research
elif topic_name in ["Clinical Trials", "Early Detection"]:
    results = news_tool.search(
        query=topic["query"],
        max_results=10,
        prefer_serper=False  # Use Tavily
    )
# Use environment setting for others
else:
    results = news_tool.search(
        query=topic["query"],
        max_results=10  # Uses PREFERRED_SEARCH_API
    )
```

### Search Query Optimization

**For Serper (Google-style):**
```json
{
  "query": "AI cancer research 2024 latest breakthrough"
}
```

**For Tavily (Domain-specific):**
```json
{
  "query": "+AI +cancer +research +oncology site:pubmed.gov OR site:nature.com"
}
```

## 🧪 Testing Both APIs

### Test Serper:
```bash
uv run python -c "
import os
os.environ['PREFERRED_SEARCH_API'] = 'serper'
from ai_news_langgraph.tools import NewsSearchTool
tool = NewsSearchTool()
results = tool.search('AI in radiology', max_results=3)
print(f'Found {len(results)} results')
for r in results[:2]:
    print(f'  - {r[\"title\"][:60]}')
"
```

### Test Tavily:
```bash
uv run python -c "
import os
os.environ['PREFERRED_SEARCH_API'] = 'tavily'
from ai_news_langgraph.tools import NewsSearchTool
tool = NewsSearchTool()
results = tool.search('AI in radiology', max_results=3)
print(f'Found {len(results)} results')
for r in results[:2]:
    print(f'  - {r[\"title\"][:60]}')
"
```

### Compare Results:
```bash
uv run python << 'EOF'
from ai_news_langgraph.tools import NewsSearchTool

query = "AI cancer detection"

# Test Serper
print("=" * 60)
print("SERPER RESULTS:")
print("=" * 60)
tool1 = NewsSearchTool()
tool1.preferred_api = "serper"
serper_results = tool1.search(query, max_results=5)
for r in serper_results[:3]:
    print(f"  {r['title'][:60]}")
    print(f"  {r['url']}\n")

# Test Tavily
print("\n" + "=" * 60)
print("TAVILY RESULTS:")
print("=" * 60)
tool2 = NewsSearchTool()
tool2.preferred_api = "tavily"
tavily_results = tool2.search(query, max_results=5)
for r in tavily_results[:3]:
    print(f"  {r['title'][:60]}")
    print(f"  {r['url']}\n")
EOF
```

## 💰 API Costs & Limits

### Serper
- **Free Tier**: 2,500 queries/month
- **Paid**: $50/month for 20,000 queries
- **Cost per query**: ~$0.0025
- **Get key**: [https://serper.dev/](https://serper.dev/)

### Tavily
- **Free Tier**: 1,000 queries/month
- **Paid**: Various tiers
- **Cost per query**: Varies by plan
- **Get key**: [https://tavily.com/](https://tavily.com/)

## 🔐 API Key Management

Your `.env` should have:

```bash
# Both keys (for automatic fallback)
SERPER_API_KEY=your-serper-key-here
TAVILY_API_KEY=your-tavily-key-here

# Choose primary
PREFERRED_SEARCH_API=serper
```

**Security Best Practices:**
- ✅ Never commit `.env` to git
- ✅ Use different keys for dev/prod
- ✅ Rotate keys periodically
- ✅ Monitor usage/costs

## 📈 Performance Tips

1. **Use Serper for speed** - Generally faster response times
2. **Use Tavily for quality** - Better for academic sources
3. **Enable both** - Automatic fallback ensures reliability
4. **Reduce max_results** - Faster queries, lower costs
5. **Cache results** - Avoid redundant searches

## 🐛 Troubleshooting

### Issue: "Serper search error"

```bash
# Check your key
cat .env | grep SERPER_API_KEY

# Test the key
curl -X POST https://google.serper.dev/search \
  -H "X-API-KEY: your-key-here" \
  -H "Content-Type: application/json" \
  -d '{"q":"test"}'
```

### Issue: "No results found"

Both APIs failed. Check:
1. Both API keys are valid
2. APIs are not rate-limited
3. Query is not too specific
4. Network connection works

### Issue: "Tavily unauthorized"

Your Tavily key may be invalid or expired:
```bash
# Get new key from https://tavily.com/
echo 'TAVILY_API_KEY="tvly-new-key"' >> .env
```

## 🎯 Recommendation

**Current Setup (Serper Primary) is GOOD for:**
- ✅ General AI news aggregation
- ✅ Broad healthcare topics
- ✅ Latest breaking news
- ✅ Maximum result coverage

**Consider Switching to Tavily if:**
- You need more academic sources
- You want domain-specific filtering
- You prefer AI-optimized relevance
- You need publication dates

## 📝 Summary

✅ **You're now using Serper as primary**
✅ **Tavily is configured as fallback**
✅ **Both APIs have valid keys**
✅ **Configuration is in `.env` file**
✅ **Easy to switch if needed**

To switch back to Tavily:
```bash
# Edit .env
PREFERRED_SEARCH_API=tavily
```

That's it! Your search is now powered by Google via Serper API! 🚀

