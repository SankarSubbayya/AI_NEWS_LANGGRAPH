# 🧹 Clean Repository Setup for AI_NEWS_LANGGRAPH

This guide will help you create a clean repository with **only AI_NEWS_LANGGRAPH**.

---

## 🎯 Goal

Create a new Git repository containing **only** the AI_NEWS_LANGGRAPH project, removing ai_news and crew-ai projects.

---

## ⚡ Quick Method (Recommended)

### Step 1: Create a new repository on GitHub

1. Go to: https://github.com/new
2. Repository name: `AI_NEWS_LANGGRAPH`
3. Description: "AI-powered newsletter generator using LangGraph"
4. Choose Public or Private
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

### Step 2: Set up clean repository

```bash
# Navigate to AI_NEWS_LANGGRAPH
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH

# Initialize new git repository (fresh start)
rm -rf .git  # Remove any existing git submodule
git init

# Add all files
git add .

# Create initial commit
git commit -m "🎉 Initial commit: AI Newsletter Generator with LangGraph

✨ Features:
- Multi-agent LangGraph workflow (Research, Editor, Reviewer, Chief Editor)
- Cancer research knowledge graph with medical ontology
- Flux AI image generation for newsletter covers
- AI-powered glossary generation
- Comprehensive MkDocs documentation (87+ pages)
- Interactive Streamlit app
- COSTAR prompt engineering framework

📚 Documentation:
- 7 organized categories (guides, features, setup, troubleshooting, etc.)
- 54 pages with 8 navigation sections
- Professional MkDocs site with Material theme

🔧 Technology:
- LangGraph for workflow orchestration
- OpenAI GPT-4 for content generation
- Replicate Flux for image generation
- Phoenix & LangSmith observability
- Pydantic for data validation
- Plotly for visualizations

See docs/meta/FINAL_DOCS_CLEANUP.md for complete documentation overview."

# Add your new GitHub repository as remote
git remote add origin https://github.com/YourUsername/AI_NEWS_LANGGRAPH.git

# Push to GitHub
git push -u origin main
```

### Step 3: Clean up old directory (AFTER successful push)

```bash
# Go back to parent directory
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai

# Delete old projects (ONLY after confirming push succeeded)
rm -rf ai_news/
rm -rf crew-ai/
rm -rf .git  # Remove old git repository

# Optional: Remove parent directory if no longer needed
cd ..
rm -rf sv-agentic-ai/
```

---

## 📋 Alternative Method: Keep Current Location

If you want to keep AI_NEWS_LANGGRAPH in the current location but clean up:

```bash
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai

# Backup first (recommended)
cp -r AI_NEWS_LANGGRAPH ~/Desktop/AI_NEWS_LANGGRAPH_backup

# Delete other projects
rm -rf ai_news/
rm -rf crew-ai/

# Reset git repository
rm -rf .git
git init

# Move AI_NEWS_LANGGRAPH contents to root
mv AI_NEWS_LANGGRAPH/* .
mv AI_NEWS_LANGGRAPH/.* . 2>/dev/null
rmdir AI_NEWS_LANGGRAPH

# Create new commit
git add .
git commit -m "🎉 Initial commit: AI Newsletter Generator"

# Add remote and push
git remote add origin https://github.com/YourUsername/AI_NEWS_LANGGRAPH.git
git push -u origin main
```

---

## ✅ Recommended Approach: Move to Clean Location

The cleanest approach is to move AI_NEWS_LANGGRAPH to its own directory:

```bash
# Create new clean directory
mkdir -p ~/projects/AI_NEWS_LANGGRAPH

# Copy AI_NEWS_LANGGRAPH to new location
cp -r /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH/* ~/projects/AI_NEWS_LANGGRAPH/
cp -r /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH/.* ~/projects/AI_NEWS_LANGGRAPH/ 2>/dev/null

# Navigate to new location
cd ~/projects/AI_NEWS_LANGGRAPH

# Remove any old git data
rm -rf .git

# Initialize fresh git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "🎉 Initial commit: AI Newsletter Generator with LangGraph"

# Add your new GitHub repository
git remote add origin https://github.com/YourUsername/AI_NEWS_LANGGRAPH.git

# Push to GitHub
git push -u origin main

# After successful push, delete old directory
rm -rf /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai
```

---

## 🔍 Verify Before Deleting

Before deleting the old projects, verify everything is in AI_NEWS_LANGGRAPH:

```bash
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH

# Check all important files exist
ls -la
ls -la src/
ls -la docs/
ls -la examples/

# Verify git status (if using current location)
git status
```

---

## ⚠️ Important Notes

### What Gets Deleted
- ❌ `ai_news/` - Old CrewAI version
- ❌ `crew-ai/` - Crew AI examples
- ❌ Old git repository (if doing clean setup)

### What Gets Kept
- ✅ All AI_NEWS_LANGGRAPH files
- ✅ Documentation (87+ files)
- ✅ Source code
- ✅ Examples
- ✅ Scripts and configuration

### Backup First!
Always backup before deleting:
```bash
# Backup entire directory
cp -r /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai ~/Desktop/sv-agentic-ai-backup
```

---

## 🎯 My Recommendation

**Use the "Move to Clean Location" approach:**

1. ✅ Creates a fresh, clean repository
2. ✅ No mixing with old projects
3. ✅ Professional directory structure
4. ✅ Easy to manage
5. ✅ Can safely delete old directory after verification

**New location:** `~/projects/AI_NEWS_LANGGRAPH`

This gives you a clean slate and removes all association with the old multi-project setup.

---

## 📦 What Your New Repository Will Contain

```
AI_NEWS_LANGGRAPH/
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
├── .env.example
├── mkdocs.yml
├── src/
│   └── ai_news_langgraph/
├── docs/
│   ├── index.md
│   ├── guides/
│   ├── features/
│   ├── setup/
│   ├── troubleshooting/
│   ├── references/
│   ├── meta/
│   └── archive/
├── examples/
├── tests/
├── outputs/
└── *.sh (helper scripts)
```

**Total:** 142 files, 31,948 lines of code

---

## 🚀 Quick Start After Setup

```bash
# Install dependencies
cd ~/projects/AI_NEWS_LANGGRAPH
uv sync

# View documentation
./serve_docs.sh

# Run the app
python -m streamlit run final_newsletter_app.py
```

---

## ✅ Checklist

Before proceeding:
- [ ] Created new GitHub repository
- [ ] Backed up current directory
- [ ] Verified all files in AI_NEWS_LANGGRAPH
- [ ] Decided on approach (move vs. restructure)

During setup:
- [ ] Initialized new git repository
- [ ] Created initial commit
- [ ] Added remote origin
- [ ] Pushed to GitHub successfully

After setup:
- [ ] Verified repository on GitHub
- [ ] Tested documentation site
- [ ] Tested application runs
- [ ] Deleted old directories (if desired)

---

**Ready to proceed?** Choose your preferred method and let me know which approach you want to use!

