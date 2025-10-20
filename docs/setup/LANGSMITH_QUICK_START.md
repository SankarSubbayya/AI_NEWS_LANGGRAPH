# LangSmith Quick Start ⚡

## TL;DR (30 seconds)

1. **Get API Key**: Go to https://smith.langchain.com/ → Sign up → Get API key
2. **Set in .env**:
   ```
   LANGSMITH_API_KEY=lsv2_pt_your_key_here
   ```
3. **Restart Streamlit**:
   ```bash
   pkill -f streamlit
   uv run streamlit run final_newsletter_app.py
   ```
4. **Generate Newsletter**: Click "Generate Newsletter" button
5. **View Traces**: Click the dashboard link in the sidebar

## That's it! ✅

Your AI operations are now being traced and visible in the LangSmith cloud dashboard.

---

## Why LangSmith?

✅ **No local server needed** (unlike Phoenix)
✅ **Cloud-based dashboard** (always available)
✅ **Automatic tracing** (zero code changes needed)
✅ **FREE tier** with unlimited traces
✅ **Real-time updates** as operations run

---

## What Gets Traced?

- 🤖 Every GPT-4o-mini call
- 🖼️ DALL-E image generation
- 📊 Token usage & costs
- ⏱️ Operation latency
- ❌ Errors & exceptions
- 📈 Workflow execution timeline

---

## See Your Data

### Dashboard Link
```
https://smith.langchain.com/projects/p/AI-News-LangGraph
```

### Or from Streamlit
- Look in sidebar: **"📊 Observability"**
- Click blue **"🔗 View Dashboard"** link

---

## Example Trace

When you generate a newsletter, LangSmith shows:

```
Generate Newsletter (AI-News-LangGraph project)
├─ Research Agent
│  ├─ LLM Call: "Fetch articles about cancer research..."
│  ├─ Tokens: 2,450 in, 1,200 out
│  └─ Time: 3.2s
├─ Summarizer
│  ├─ LLM Call: "Summarize these findings..."
│  ├─ Tokens: 3,100 in, 800 out
│  └─ Time: 2.1s
├─ Cover Image
│  ├─ DALL-E Call: "Generate cover image..."
│  └─ Time: 8.5s
└─ Total: $0.047 (estimated cost)
```

---

## Troubleshooting

**"LangSmith not configured"?**
```bash
# Check if key is set
echo $LANGSMITH_API_KEY

# If not, set it
export LANGSMITH_API_KEY="lsv2_pt_..."
```

**No traces appearing?**
1. Generate a newsletter (to create traces)
2. Wait 5 seconds
3. Refresh dashboard
4. Check you're in the right project

**Wrong project?**
- Check sidebar shows: **"AI-News-LangGraph"**
- Dashboard should match

---

## Cost Tracking

FREE tier includes:
- ✅ Unlimited traces
- ✅ 30 days history
- ✅ Full analytics
- ✅ Cost estimation

**View your costs:**
1. LangSmith dashboard → Analytics
2. See breakdown by model
3. View token usage trends

---

## Advanced: Custom Project

Want a different project name?

Edit `.env`:
```
LANGSMITH_API_KEY=your_key
LANGCHAIN_PROJECT=My-Custom-Project
```

New traces will go to your custom project.

---

## Resources

- 📚 Full Setup Guide: `LANGSMITH_SETUP.md`
- 🔑 Get Key: https://smith.langchain.com/
- 📖 Docs: https://docs.smith.langchain.com/
- 💬 Support: https://smith.langchain.com/support

---

**Ready to trace your AI?** 🚀

Get your API key and restart Streamlit!