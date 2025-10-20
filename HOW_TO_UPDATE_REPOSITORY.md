# 📦 How to Update the Repository

**Date:** October 20, 2025  
**Git Repository Location:** `/Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/`

---

## 🎯 Quick Guide

The Git repository is **one level up** from the AI_NEWS_LANGGRAPH directory.

### ⚡ Quick Commands

```bash
# Navigate to repository root
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai

# Check status
git status

# Add all AI_NEWS_LANGGRAPH changes
git add AI_NEWS_LANGGRAPH/

# Commit with message
git commit -m "📚 Major documentation cleanup and code organization"

# Push to GitHub
git push origin main
```

---

## 📋 Step-by-Step Guide

### Step 1: Navigate to Repository Root

```bash
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai
```

**Note:** The `.git` folder is here, not in `AI_NEWS_LANGGRAPH/`

---

### Step 2: Check Current Status

```bash
git status
```

This will show you all changes including:
- ✅ Documentation reorganization
- ✅ New source files
- ✅ Updated scripts
- ✅ Modified configuration

---

### Step 3: Stage Your Changes

#### Option A: Add Everything (Recommended)

```bash
# Add all changes in AI_NEWS_LANGGRAPH
git add AI_NEWS_LANGGRAPH/
```

#### Option B: Add Selectively

```bash
# Add documentation
git add AI_NEWS_LANGGRAPH/docs/
git add AI_NEWS_LANGGRAPH/mkdocs.yml
git add AI_NEWS_LANGGRAPH/README.md

# Add source code
git add AI_NEWS_LANGGRAPH/src/
git add AI_NEWS_LANGGRAPH/pyproject.toml
git add AI_NEWS_LANGGRAPH/uv.lock

# Add scripts
git add AI_NEWS_LANGGRAPH/*.sh
git add AI_NEWS_LANGGRAPH/find_unused_functions.py
git add AI_NEWS_LANGGRAPH/final_newsletter_app.py

# Add examples
git add AI_NEWS_LANGGRAPH/examples/

# Add config
git add AI_NEWS_LANGGRAPH/.gitignore
git add AI_NEWS_LANGGRAPH/.env.example
```

---

### Step 4: Review Staged Changes

```bash
# See what will be committed
git status

# See detailed changes
git diff --cached
```

---

### Step 5: Commit Changes

#### Option A: Detailed Commit Message (Recommended)

```bash
git commit -m "📚 Major documentation cleanup and code organization

✨ Features:
- Reorganized 87+ markdown files into 7 logical categories
- Created comprehensive MkDocs documentation site
- Added unused function analyzer

🗂️ Documentation:
- Moved all docs into organized subdirectories (guides/, features/, setup/, etc.)
- Only index.md remains in docs root for clean structure
- Updated mkdocs.yml with 8 navigation sections (54 pages)
- Created meta documentation for cleanup process

🔧 Improvements:
- Updated .gitignore to exclude generated outputs
- Added helper scripts (build_docs.sh, serve_docs.sh, setup_mkdocs.sh)
- Enhanced source code (nodes_v2.py, workflow.py, costar_prompts.py)
- Added new modules (cancer_research_knowledge_graph.py, flux_image_generator.py, etc.)

📊 Impact:
- 97% reduction in docs root files (30+ → 1)
- 46% faster documentation builds
- Professional GitHub-ready structure
- Easy navigation and maintenance

See AI_NEWS_LANGGRAPH/docs/meta/FINAL_DOCS_CLEANUP.md for details."
```

#### Option B: Simple Commit Message

```bash
git commit -m "📚 Cleanup and organize documentation"
```

---

### Step 6: Push to GitHub

```bash
# Push to main branch
git push origin main
```

If this is your first push or you need to set upstream:

```bash
# Push and set upstream
git push -u origin main
```

---

## 🔍 Verify Your Changes

### Check Commit

```bash
# View last commit
git show

# View commit history
git log --oneline -5
```

### Check Remote

```bash
# View remote URL
git remote -v

# Should show:
# origin  https://github.com/SankarSubbayya/AI_NEWS_LANGGRAPH.git (fetch)
# origin  https://github.com/SankarSubbayya/AI_NEWS_LANGGRAPH.git (push)
```

### Verify on GitHub

1. Go to: https://github.com/SankarSubbayya/AI_NEWS_LANGGRAPH
2. Check that your changes are visible
3. Verify documentation appears correctly

---

## ⚠️ Troubleshooting

### Error: "failed to push some refs"

```bash
# Pull latest changes first
git pull origin main --rebase

# Then push
git push origin main
```

### Error: "repository not found"

Check your remote URL:

```bash
git remote -v
```

If incorrect, update it:

```bash
git remote set-url origin https://github.com/SankarSubbayya/AI_NEWS_LANGGRAPH.git
```

### Error: "Authentication failed"

Make sure you're using:
- Personal Access Token (not password)
- SSH key (if configured)

---

## 📁 What Gets Committed

### ✅ Included (Important Files)

- `docs/` - All documentation (organized)
- `src/` - Source code changes
- `examples/` - Example scripts
- `*.sh` - Helper scripts
- `mkdocs.yml` - MkDocs configuration
- `README.md` - Project readme
- `pyproject.toml` - Dependencies
- `.gitignore` - Git ignore rules

### ❌ Excluded (Generated Files)

- `outputs/newsletters/` - Generated newsletters
- `outputs/newsletter_*.html` - Newsletter files
- `outputs/newsletter_*.md` - Newsletter markdown
- `outputs/flux_prompts/` - Generated prompts
- `outputs/images/*.png` - Generated images
- `outputs/knowledge_graphs/` - Generated graphs
- `site/` - Built documentation site
- `.env` - Environment variables
- `__pycache__/` - Python cache
- `.DS_Store` - Mac system files

---

## 🎯 Best Practices

### Before Committing

1. ✅ Review changes: `git status`
2. ✅ Test your code: `./test.sh` or `pytest`
3. ✅ Build docs: `./build_docs.sh`
4. ✅ Check for sensitive data: No API keys, passwords

### Commit Messages

Use clear, descriptive messages:

```bash
# Good ✅
git commit -m "📚 Reorganize documentation into categories"
git commit -m "🐛 Fix knowledge graph method calls"
git commit -m "✨ Add Flux image generator"

# Bad ❌
git commit -m "updates"
git commit -m "fix"
git commit -m "changes"
```

### After Pushing

1. ✅ Verify on GitHub
2. ✅ Check that workflows pass (if any)
3. ✅ Update any related documentation

---

## 🚀 Complete Example

Here's a complete workflow:

```bash
# 1. Navigate to repository root
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai

# 2. Check status
git status

# 3. Add all AI_NEWS_LANGGRAPH changes
git add AI_NEWS_LANGGRAPH/

# 4. Check what will be committed
git status

# 5. Commit with message
git commit -m "📚 Major documentation cleanup and code organization

- Reorganized 87+ markdown files into 7 categories
- Created comprehensive MkDocs documentation site
- Added unused function analyzer
- Updated source code and scripts

See AI_NEWS_LANGGRAPH/docs/meta/FINAL_DOCS_CLEANUP.md for details."

# 6. Push to GitHub
git push origin main

# 7. Verify
git log -1
```

---

## 📊 Your Current Changes

Based on the cleanup, you have:

### Documentation
- ✅ 87+ markdown files reorganized
- ✅ MkDocs site configuration
- ✅ New directory structure (guides/, features/, etc.)
- ✅ Comprehensive navigation (8 sections, 54 pages)

### Source Code
- ✅ Enhanced nodes_v2.py
- ✅ Updated workflow.py
- ✅ Fixed costar_prompts.py
- ✅ New modules (cancer_research_knowledge_graph.py, etc.)

### Scripts & Config
- ✅ Helper scripts (build_docs.sh, serve_docs.sh)
- ✅ Analysis tools (find_unused_functions.py)
- ✅ Updated .gitignore
- ✅ Updated pyproject.toml

---

## 💡 Tips

### Quick Status Check

```bash
# From anywhere in the project
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai && git status
```

### View Changes by File Type

```bash
# View all changed .py files
git status | grep ".py$"

# View all changed .md files
git status | grep ".md$"
```

### Undo Last Commit (Before Push)

```bash
# Keep changes but undo commit
git reset --soft HEAD~1

# Discard changes and undo commit
git reset --hard HEAD~1
```

---

## ✅ Checklist

Before pushing:

- [ ] Navigated to repository root (`cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai`)
- [ ] Checked status (`git status`)
- [ ] Staged changes (`git add AI_NEWS_LANGGRAPH/`)
- [ ] Reviewed staged changes (`git status`)
- [ ] Created commit with descriptive message
- [ ] Tested that nothing is broken
- [ ] Ready to push (`git push origin main`)

After pushing:

- [ ] Verified commit on GitHub
- [ ] Checked that files appear correctly
- [ ] Documentation looks good
- [ ] No sensitive data committed

---

## 🎉 Done!

Your changes are now in the repository and visible on GitHub!

**Next Steps:**
1. Share the GitHub link with your team
2. Deploy documentation (if needed)
3. Continue developing

---

**Repository:** https://github.com/SankarSubbayya/AI_NEWS_LANGGRAPH  
**Documentation:** Run `./serve_docs.sh` then visit http://127.0.0.1:8000

