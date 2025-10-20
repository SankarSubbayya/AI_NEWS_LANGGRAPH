# ⚡ QUICK API KEY SETUP

## 🎯 EASIEST WAY (30 seconds!)

### Streamlit is Running: http://localhost:8502

**Just do this:**

1. Open http://localhost:8502 in your browser
2. Look at the **LEFT SIDEBAR**
3. Find **"🔑 OpenAI API Key"**
4. Paste your key: `sk-proj-...`
5. Done! ✨

---

## 🔑 Don't Have an API Key Yet?

Get one here: https://platform.openai.com/api-keys

1. Sign in to OpenAI
2. Click "+ Create new secret key"
3. Copy the key (starts with `sk-proj-`)
4. Paste in Streamlit sidebar

**Cost:** ~$0.10 per newsletter

---

## 💾 Want to Save Key Permanently?

Run this command in your terminal:

```bash
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH

# Create .env file (replace YOUR-KEY with your actual key)
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-YOUR-KEY-HERE
EOF

# Restart Streamlit
lsof -ti:8502 | while read pid; do kill -9 $pid; done
streamlit run streamlit_newsletter_app.py
```

**Replace `sk-proj-YOUR-KEY-HERE` with your actual OpenAI key!**

---

## ✅ VERIFY IT WORKS

After setting the key:

1. Open http://localhost:8502
2. Select **"Full AI Workflow (Comprehensive)"**
3. Select **"Config File Topics (Real)"**
4. Click **"Generate Newsletter"**
5. See progress bar (2-5 min wait)
6. Get rich newsletter! 🎉

---

**For detailed guide, see:** `SETUP_API_KEY.md`

