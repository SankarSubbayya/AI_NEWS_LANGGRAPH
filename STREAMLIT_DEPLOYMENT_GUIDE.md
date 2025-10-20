# 🚀 Streamlit Community Cloud Deployment Guide

Quick guide to deploy your AI Newsletter Generator to Streamlit Community Cloud.

---

## 📋 Prerequisites

- ✅ GitHub account
- ✅ Code in a GitHub repository (PUBLIC for free tier)
- ✅ Streamlit Community Cloud account (free at https://share.streamlit.io)
- ✅ API keys (OpenAI, Tavily, optionally Replicate)

---

## 🎯 Step-by-Step Deployment

### 1. Push Code to GitHub

```bash
# Make sure you're in the project directory
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH

# Push your code (if not done yet)
git push -u origin main
```

**Verify:** Go to https://github.com/SankarSubbayya/AI_NEWS_LANGGRAPH and confirm your files are there.

---

### 2. Deploy on Streamlit Community Cloud

1. **Go to:** https://share.streamlit.io/

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Fill in the details:**
   - **Repository:** `SankarSubbayya/AI_NEWS_LANGGRAPH`
   - **Branch:** `main`
   - **Main file path:** `final_newsletter_app.py`
   - **App URL:** (choose a custom name or use default)

5. **Click "Deploy"**

Streamlit will start building and deploying your app (this takes 2-5 minutes).

---

### 3. Configure Secrets (API Keys)

Once deployed, you need to add your API keys:

1. **Go to your app dashboard** on Streamlit Cloud

2. **Click the ⚙️ Settings icon**

3. **Go to "Secrets" tab**

4. **Add your secrets in TOML format:**

```toml
# Required
OPENAI_API_KEY = "sk-your-openai-key-here"
TAVILY_API_KEY = "tvly-your-tavily-key-here"

# Optional (for Flux image generation)
REPLICATE_API_TOKEN = "r8_your-replicate-token-here"

# Optional (fallback search)
SERPER_API_KEY = "your-serper-key-here"
```

5. **Click "Save"**

The app will automatically restart with the new secrets.

---

## 🎨 Customization

### Change App Title and Icon

Edit `final_newsletter_app.py`:

```python
st.set_page_config(
    page_title="AI Newsletter Generator",  # Change this
    page_icon="📰",  # Change this emoji
    layout="wide"
)
```

### Update Repository Settings

In your Streamlit Cloud app settings:
- **General:** Change app name, description
- **Resources:** Adjust if needed (free tier has limits)
- **Sharing:** Make public or private

---

## 🔍 Troubleshooting

### Error: "Unable to deploy - code not connected to GitHub"

**Solution:** Push your code to GitHub first!
```bash
git push -u origin main
```

---

### Error: "Module not found" during deployment

**Solution:** Make sure `pyproject.toml` or `requirements.txt` includes all dependencies.

Check that these are in your `pyproject.toml`:
```toml
[project]
dependencies = [
    "streamlit>=1.28.0",
    "langgraph>=0.2.0",
    "langchain>=0.3.0",
    "langchain-openai>=0.2.0",
    # ... other dependencies
]
```

---

### Error: "API Key not found"

**Solution:** Add secrets in Streamlit Cloud settings (see Step 3 above).

---

### App is slow or timing out

**Causes:**
1. Free tier has resource limits
2. LangGraph workflow is computationally intensive
3. Multiple API calls

**Solutions:**
1. Use "Quick (Sample Data)" mode for demos
2. Consider upgrading to paid tier for production
3. Optimize workflow (reduce topics, cache results)

---

### Error: "Repository not found"

**Causes:**
1. Repository is private (free tier needs PUBLIC repos)
2. Wrong repository name
3. Not authorized

**Solutions:**
1. Make repository public on GitHub
2. Double-check repository name
3. Reconnect GitHub account in Streamlit settings

---

## 📊 Resource Limits (Free Tier)

- **Memory:** 1 GB RAM
- **CPU:** Shared resources
- **Storage:** Limited
- **Apps:** 3 apps max
- **Users:** Unlimited viewers

**If you need more:** Upgrade to Streamlit Cloud paid tiers.

---

## 🎯 Best Practices

### 1. Use Environment Variables

Never hardcode API keys in your code!

```python
# ❌ Don't do this
OPENAI_API_KEY = "sk-1234567890"

# ✅ Do this
import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### 2. Add Error Handling

```python
try:
    # Your workflow code
    result = workflow.execute(initial_state)
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.info("Please check your API keys and try again.")
```

### 3. Show Progress

```python
with st.spinner("Running AI workflow..."):
    # Long-running operation
    result = workflow.execute()
st.success("Complete!")
```

### 4. Cache Results

```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def expensive_function():
    # Expensive operation
    return result
```

### 5. Optimize for Free Tier

- Use "Quick (Sample Data)" as default
- Show full workflow as optional
- Cache API responses
- Limit number of topics

---

## 🔄 Updating Your Deployed App

When you make changes:

```bash
# 1. Make changes locally
# 2. Commit changes
git add .
git commit -m "Update description"

# 3. Push to GitHub
git push origin main
```

Streamlit Cloud will **automatically redeploy** when you push to GitHub!

---

## 📱 Sharing Your App

After deployment, your app is available at:

```
https://[your-app-name].streamlit.app
```

**Share it:**
- Share the URL directly
- Embed in documentation
- Add to your portfolio
- Share on social media

---

## 🎓 Advanced Features

### Custom Domain

Paid tiers can use custom domains:
1. Go to app settings
2. Add custom domain
3. Configure DNS

### Analytics

View usage analytics in Streamlit Cloud:
- Total views
- Active users
- Resource usage
- Error rates

### GitHub Integration

Auto-deploy from GitHub:
- Push to main → auto-deploy
- Use branches for testing
- PR preview deployments (paid)

---

## 📚 Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **Deployment Guide:** https://docs.streamlit.io/streamlit-community-cloud
- **Secrets Management:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- **Support:** https://discuss.streamlit.io/

---

## ✅ Deployment Checklist

Before deploying:

- [ ] Code is in PUBLIC GitHub repository
- [ ] `final_newsletter_app.py` exists and works locally
- [ ] `pyproject.toml` or `requirements.txt` includes all dependencies
- [ ] No hardcoded API keys in code
- [ ] Tested app locally (`streamlit run final_newsletter_app.py`)
- [ ] Committed and pushed all changes

During deployment:

- [ ] Connected GitHub account to Streamlit Cloud
- [ ] Selected correct repository and branch
- [ ] Specified correct main file path
- [ ] Added all required secrets (API keys)
- [ ] Watched deployment logs for errors

After deployment:

- [ ] Tested app in Streamlit Cloud
- [ ] Verified all features work
- [ ] Tested with different modes (Quick vs Full)
- [ ] Shared app URL

---

## 🆘 Getting Help

If you're stuck:

1. **Check logs** in Streamlit Cloud (view logs button)
2. **Search docs** at https://docs.streamlit.io
3. **Ask community** at https://discuss.streamlit.io
4. **Check GitHub issues** for similar problems

---

## 🎉 Success!

Once deployed, your AI Newsletter Generator will be:

✅ **Live** on the internet  
✅ **Accessible** to anyone with the link  
✅ **Auto-updated** when you push to GitHub  
✅ **Free** (on community cloud tier)  

**Your app URL:** `https://[your-app-name].streamlit.app`

---

**Ready to deploy? Push your code and get started!** 🚀

