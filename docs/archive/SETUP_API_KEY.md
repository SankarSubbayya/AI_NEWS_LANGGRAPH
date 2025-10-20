# 🔑 How to Set Your OpenAI API Key

## ✅ YOU HAVE 3 OPTIONS

---

## 🎯 OPTION 1: Streamlit Sidebar (Easiest!) ⭐

**Streamlit is running on:** http://localhost:8502

1. Open the app in your browser
2. Look at the **LEFT SIDEBAR**
3. Find the **"🔑 OpenAI API Key"** input field
4. Paste your key: `sk-proj-...`
5. The key is saved for this session!

**This is the EASIEST way!** ✨

---

## 🎯 OPTION 2: .env File (Permanent)

**Create a .env file:**

```bash
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH

# Create .env file
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-your-actual-key-here
EOF

# Restart Streamlit to load the key
lsof -ti:8502 | while read pid; do kill -9 $pid; done
streamlit run streamlit_newsletter_app.py
```

**Get your OpenAI key from:**
https://platform.openai.com/api-keys

---

## 🎯 OPTION 3: Terminal Export (Temporary)

**In your terminal (current session only):**

```bash
# Set the key
export OPENAI_API_KEY='sk-proj-your-actual-key-here'

# Verify it's set
echo $OPENAI_API_KEY

# Restart Streamlit
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH
lsof -ti:8502 | while read pid; do kill -9 $pid; done
streamlit run streamlit_newsletter_app.py
```

**Note:** This only works for the current terminal session!

---

## 📋 FULL WORKFLOW CHECKLIST

Once your key is set, to generate rich newsletters:

### ✅ Step 1: Open Streamlit
```
http://localhost:8502
```

### ✅ Step 2: Configure Sidebar

**Generation Mode:**
- ⚫ Full AI Workflow (Comprehensive) ⭐ **SELECT THIS!**

**Data Source:**
- ⚫ Config File Topics (Real) ⭐ **SELECT THIS!**

**OpenAI API Key:**
- Paste your key: `sk-proj-...` **OR** set in .env file

### ✅ Step 3: Generate Newsletter
- Click **"Generate Newsletter"**
- Wait 2-5 minutes
- Progress bar shows which agent is working

### ✅ Step 4: Enjoy Rich Content!
- 100+ real articles with links
- Real sources (ScienceDirect, PubMed, Nature)
- Quality scores
- Knowledge graph
- Glossary

---

## 🔍 HOW TO GET AN OPENAI API KEY

### 1. Go to OpenAI Platform
```
https://platform.openai.com/api-keys
```

### 2. Sign In or Create Account
- Use your OpenAI account
- Or create a new one

### 3. Create API Key
- Click **"+ Create new secret key"**
- Name it: "AI Newsletter Generator"
- Copy the key: `sk-proj-...`
- **Save it securely!** (You can't see it again)

### 4. Add Billing (Required)
```
https://platform.openai.com/account/billing
```
- Add payment method
- Set usage limits (recommended: $10/month)

### 5. Cost Estimate
```
Per Newsletter (Full Workflow):
- Research: ~$0.05
- Summarization: ~$0.03
- Editor: ~$0.01
- Quality Review: ~$0.01
Total: ~$0.10 per newsletter
```

---

## 🐛 TROUBLESHOOTING

### "API Key not recognized"
```bash
# Check if key starts with 'sk-proj-' or 'sk-'
echo $OPENAI_API_KEY | cut -c1-8

# Should show: sk-proj- or sk-
```

### "Still getting error after setting key"
```bash
# Restart Streamlit to load the key
lsof -ti:8502 | while read pid; do kill -9 $pid; done
streamlit run streamlit_newsletter_app.py
```

### "Key set in .env but not working"
```bash
# Verify .env file exists and has the key
cat .env | grep OPENAI_API_KEY

# Make sure no spaces around the =
# Correct:   OPENAI_API_KEY=sk-proj-abc123
# Wrong:     OPENAI_API_KEY = sk-proj-abc123
```

### "Streamlit not loading .env file"
```bash
# Install python-dotenv if needed
pip install python-dotenv

# Restart Streamlit
lsof -ti:8502 | while read pid; do kill -9 $pid; done
streamlit run streamlit_newsletter_app.py
```

---

## ✅ VERIFY IT'S WORKING

### After Setting the Key:

1. **Open Streamlit:** http://localhost:8502

2. **Check Sidebar:**
   - If key is in .env: You'll see "✅ API key loaded from .env"
   - If key is empty: You'll see the input field to paste it

3. **Try Full Workflow:**
   - Select "Full AI Workflow (Comprehensive)"
   - Select "Config File Topics (Real)"
   - Click "Generate Newsletter"
   - Should start working! (2-5 min wait)

4. **Look for Progress:**
   ```
   🚀 Initializing multi-agent workflow... 5%
   🔍 Research Agent: Fetching news... 20%
   📊 Summarizer Agent: Analyzing... 50%
   ✍️  Editor Agent: Creating summary... 70%
   ⭐ Quality Reviewer: Scoring... 85%
   🎨 Generating visuals... 100%
   ✅ Newsletter Generated Successfully!
   ```

---

## 🎯 QUICK START (RECOMMENDED)

**The easiest way - use Streamlit sidebar:**

1. Open: http://localhost:8502
2. Look at left sidebar
3. Find "🔑 OpenAI API Key" field
4. Paste your key
5. Done! ✨

---

## 📚 NEXT STEPS

Once your key is set:

1. ✅ Read: `HOW_TO_GET_RICH_NEWSLETTERS.md`
2. ✅ Read: `RICH_NEWSLETTER_COMPARISON.md`
3. ✅ Generate your first rich newsletter!
4. ✅ Browse past newsletters in "View Newsletters" tab

---

## 🔒 SECURITY NOTES

### ✅ DO:
- Store key in `.env` file (ignored by git)
- Use environment variables
- Set usage limits on OpenAI dashboard
- Keep key private

### ❌ DON'T:
- Commit `.env` to git (it's in .gitignore)
- Share your key publicly
- Hardcode key in source files
- Push key to GitHub

---

## 💰 COST MANAGEMENT

### Set Usage Limits:
```
https://platform.openai.com/account/limits
```

**Recommended Settings:**
- Hard limit: $10/month
- Email alert: $5
- Soft limit: $8

**Cost Per Newsletter:**
- Quick (Sample): $0
- Full Workflow: ~$0.10

**Monthly Estimate:**
- 10 newsletters: ~$1
- 50 newsletters: ~$5
- 100 newsletters: ~$10

---

**Choose OPTION 1 (Streamlit Sidebar) for the quickest setup!** 🚀

Open: http://localhost:8502

