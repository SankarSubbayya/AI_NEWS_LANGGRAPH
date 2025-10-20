# 📚 MkDocs Documentation Guide

Complete guide for working with the MkDocs documentation system.

---

## ✅ What's Been Set Up

**MkDocs** is now fully configured with:

- ✅ **Material Theme** - Beautiful, responsive design
- ✅ **Search** - Full-text search across all docs
- ✅ **Navigation** - Organized menu structure
- ✅ **Code Highlighting** - Syntax highlighting for code blocks
- ✅ **Dark Mode** - Automatic light/dark theme switching
- ✅ **Mobile Responsive** - Works great on all devices

---

## 🚀 Quick Start

### 1. Serve Documentation Locally

**Start the development server:**
```bash
./serve_docs.sh
```

**Or manually:**
```bash
.venv/bin/python -m mkdocs serve
```

**Then open in browser:**
```
http://127.0.0.1:8000
```

**Features while serving:**
- 🔄 **Auto-reload** - Changes update instantly
- 🔍 **Search** - Full-text search enabled
- 📱 **Responsive** - Test on any device

---

### 2. Build Static Site

**Build for production:**
```bash
./build_docs.sh
```

**Or manually:**
```bash
.venv/bin/python -m mkdocs build
```

**Output:**
- Static files in `site/` directory
- Ready to deploy to any web server

---

## 📁 Project Structure

```
AI_NEWS_LANGGRAPH/
├── mkdocs.yml                  ← Configuration file
├── serve_docs.sh              ← Start dev server
├── build_docs.sh              ← Build static site
│
├── docs/                      ← All documentation
│   ├── index.md              ← Homepage
│   ├── QUICK_START.md
│   ├── RUN_GUIDE.md
│   │
│   ├── setup/                ← Setup guides
│   ├── features/             ← Feature docs
│   ├── troubleshooting/      ← Fixes & solutions
│   └── ...
│
└── site/                     ← Built site (gitignored)
```

---

## ⚙️ Configuration

### mkdocs.yml Structure

```yaml
site_name: AI News LangGraph Documentation
site_description: Comprehensive documentation...

# Theme configuration
theme:
  name: material
  palette:
    - scheme: default      # Light mode
      primary: indigo
    - scheme: slate        # Dark mode
      primary: indigo
  features:
    - navigation.tabs      # Top-level tabs
    - search.suggest       # Search suggestions
    - content.code.copy    # Copy code buttons

# Navigation structure
nav:
  - Home: index.md
  - Getting Started:
      - Quick Start: QUICK_START.md
  - Setup Guides:
      - LangSmith: setup/LANGSMITH_QUICK_START.md
  # ... more sections
```

---

## 📝 Adding New Documentation

### 1. Create a New Page

**Create markdown file in `docs/`:**
```bash
echo "# My New Page" > docs/my_new_page.md
```

### 2. Add to Navigation

**Edit `mkdocs.yml`:**
```yaml
nav:
  - Home: index.md
  - My Section:
      - My New Page: my_new_page.md  # Add here
```

### 3. View Changes

**Server auto-reloads!** Just refresh your browser.

---

## 🎨 Material Theme Features

### Admonitions (Callouts)

**In your markdown:**
```markdown
!!! note "Note Title"
    This is a note with a custom title.

!!! tip
    This is a helpful tip!

!!! warning
    Be careful with this!

!!! danger
    Critical information!
```

### Code Blocks with Highlighting

````markdown
```python
def hello_world():
    print("Hello, World!")
```
````

### Tabs

```markdown
=== "Python"
    ```python
    print("Hello")
    ```

=== "JavaScript"
    ```javascript
    console.log("Hello");
    ```
```

### Task Lists

```markdown
- [x] Completed task
- [ ] Pending task
- [ ] Another task
```

---

## 🔍 Search Configuration

**Already configured** in `mkdocs.yml`:

```yaml
plugins:
  - search:
      lang: en
      separator: '[\s\-\.]+'
```

**Features:**
- ✅ Full-text search
- ✅ Search suggestions
- ✅ Highlighting in results
- ✅ Instant results

---

## 🌐 Deployment Options

### Option 1: GitHub Pages (Recommended)

**Deploy with one command:**
```bash
mkdocs gh-deploy
```

**Result:**
- Deployed to `https://yourusername.github.io/AI_NEWS_LANGGRAPH/`
- Automatic updates on push

### Option 2: Manual Hosting

**Build and upload:**
```bash
./build_docs.sh
# Upload site/ directory to your web server
```

**Compatible with:**
- Netlify
- Vercel
- AWS S3
- Any static hosting

### Option 3: Read the Docs

**Create `.readthedocs.yml`:**
```yaml
version: 2
mkdocs:
  configuration: mkdocs.yml
python:
  version: 3.12
  install:
    - requirements: requirements.txt
```

---

## 🎨 Customization

### Change Theme Colors

**Edit `mkdocs.yml`:**
```yaml
theme:
  palette:
    - scheme: default
      primary: blue        # Change this
      accent: blue         # And this
```

**Available colors:**
- `red`, `pink`, `purple`, `deep purple`
- `indigo`, `blue`, `light blue`, `cyan`
- `teal`, `green`, `light green`, `lime`
- `yellow`, `amber`, `orange`, `deep orange`

### Add Custom CSS

**1. Create CSS file:**
```bash
mkdir -p docs/stylesheets
cat > docs/stylesheets/extra.css << 'EOF'
.custom-class {
    color: red;
}
EOF
```

**2. Add to `mkdocs.yml`:**
```yaml
extra_css:
  - stylesheets/extra.css
```

### Add Custom JavaScript

**1. Create JS file:**
```bash
mkdir -p docs/javascripts
cat > docs/javascripts/extra.js << 'EOF'
console.log("Custom JavaScript loaded!");
EOF
```

**2. Add to `mkdocs.yml`:**
```yaml
extra_javascript:
  - javascripts/extra.js
```

---

## 📊 Analytics (Optional)

### Add Google Analytics

**Edit `mkdocs.yml`:**
```yaml
extra:
  analytics:
    provider: google
    property: G-XXXXXXXXXX
```

---

## 🔧 Troubleshooting

### Issue: "Config file not found"

**Solution:**
```bash
# Make sure you're in the project root
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH

# Verify mkdocs.yml exists
ls -la mkdocs.yml
```

### Issue: "Module not found"

**Solution:**
```bash
# Install/reinstall MkDocs
uv pip install mkdocs mkdocs-material
```

### Issue: "File not found in nav"

**Solution:**
- Check file path in `mkdocs.yml`
- Paths are relative to `docs/` directory
- Use forward slashes: `setup/GUIDE.md` not `setup\GUIDE.md`

### Issue: Port 8000 already in use

**Solution:**
```bash
# Use different port
.venv/bin/python -m mkdocs serve -a 127.0.0.1:8001
```

---

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `./serve_docs.sh` | Start development server |
| `./build_docs.sh` | Build static site |
| `mkdocs new .` | Create new MkDocs project |
| `mkdocs serve` | Serve docs (port 8000) |
| `mkdocs build` | Build to `site/` |
| `mkdocs gh-deploy` | Deploy to GitHub Pages |
| `mkdocs serve -a 127.0.0.1:8001` | Use different port |

---

## 🎯 Best Practices

### 1. Keep Navigation Organized

**Group related docs:**
```yaml
nav:
  - Setup:
      - Quick Start: setup/quickstart.md
      - Configuration: setup/config.md
  - Features:
      - Feature A: features/a.md
      - Feature B: features/b.md
```

### 2. Use Descriptive Titles

**Bad:**
```yaml
- Doc1: doc1.md
- File2: file2.md
```

**Good:**
```yaml
- Quick Start Guide: quickstart.md
- Installation Instructions: installation.md
```

### 3. Add Frontmatter (Optional)

**In your markdown files:**
```markdown
---
title: My Page Title
description: Page description for SEO
tags:
  - setup
  - configuration
---

# My Page Title

Content here...
```

### 4. Use Relative Links

**Between docs:**
```markdown
See the [Quick Start](../QUICK_START.md) guide.
```

### 5. Include Images

**Add images to docs:**
```bash
mkdir -p docs/images
```

**Reference in markdown:**
```markdown
![My Image](images/myimage.png)
```

---

## 📚 Advanced Features

### Version Selector

**Install mike:**
```bash
uv pip install mike
```

**Deploy versions:**
```bash
mike deploy 1.0 latest
mike set-default latest
```

### Multi-language Support

**Edit `mkdocs.yml`:**
```yaml
plugins:
  - i18n:
      default_language: en
      languages:
        en: English
        es: Español
```

### PDF Generation

**Install plugin:**
```bash
uv pip install mkdocs-with-pdf
```

**Configure:**
```yaml
plugins:
  - with-pdf:
      output_path: pdf/documentation.pdf
```

---

## ✅ Summary

**What you now have:**

| Feature | Status |
|---------|--------|
| MkDocs Installed | ✅ |
| Material Theme | ✅ |
| Configuration File | ✅ |
| Homepage | ✅ |
| Navigation Structure | ✅ |
| Serve Script | ✅ |
| Build Script | ✅ |
| Search | ✅ |
| Dark Mode | ✅ |

**Quick Start:**
```bash
# Serve locally
./serve_docs.sh

# Build for production
./build_docs.sh

# Deploy to GitHub Pages
mkdocs gh-deploy
```

---

## 🎓 Learning Resources

**Official Documentation:**
- [MkDocs](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)

**Tutorials:**
- [MkDocs Getting Started](https://www.mkdocs.org/getting-started/)
- [Material Setup](https://squidfunk.github.io/mkdocs-material/getting-started/)

---

**Ready to start? Run `./serve_docs.sh` and open http://127.0.0.1:8000** 🚀

