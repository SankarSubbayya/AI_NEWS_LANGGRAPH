# 🌐 Streamlit Newsletter Generator - User Guide

**Interactive web app for generating AI-powered cancer research newsletters**

---

## 🚀 Quick Start

### 1. Launch the App

```bash
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH
streamlit run streamlit_newsletter_app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 📋 Features

### ✨ Core Features
- ✅ **Interactive Web Interface** - No command line needed!
- ✅ **Sample Data** - Start generating immediately
- ✅ **Multiple Cover Styles** - Professional, Modern, Abstract, Scientific
- ✅ **Knowledge Graph** - Automatic medical entity extraction
- ✅ **Glossary Generation** - AI-powered or mock definitions
- ✅ **Live Preview** - See newsletter before downloading
- ✅ **One-Click Download** - Get HTML file instantly

### 🤖 AI Features (Optional)
- 🎨 **DALL-E 3 Covers** - AI-generated artwork
- 📚 **GPT-4 Glossary** - Professional definitions
- 🌟 **Flux Prompts** - For CivitAI generation

---

## 🎯 Step-by-Step Usage

### Step 1: Configure Settings (Sidebar)

**Newsletter Topic:**
```
Default: "AI in Cancer Care"
Customize: Enter your own topic
```

**Cover Image Style:**
- **Professional** - Hexagonal pattern, corporate aesthetic
- **Modern** - Diagonal lines, bright cyan-blue
- **Abstract** - Organic blobs, pink-purple gradient
- **Scientific** - Network nodes, teal with grid

**AI Features:**
- ☑️ **Use OpenAI for Glossary** - GPT-4o-mini definitions (requires API key)
- ☑️ **Use DALL-E 3 for Cover** - AI-generated cover art (requires API key)
- ☑️ **Show Flux Prompt** - Display CivitAI prompt for external generation

**Data Source:**
- ☑️ **Use Sample Data** - Quick start with pre-filled content
- ☐ **Custom Data** - Input your own newsletter content

---

### Step 2: Add Content (Content Tab)

#### Option A: Use Sample Data (Quick Start)
✅ **Enabled by default** - Just click generate!

#### Option B: Custom Content
1. **Uncheck** "Use Sample Data" in sidebar
2. **Enter Executive Summary:**
   ```
   Example: "This week, we spotlight groundbreaking 
   advances in AI-powered cancer diagnostics..."
   ```

3. **Set Number of Topics:** 1-5

4. **For Each Topic:**
   - Topic name (e.g., "AI Diagnostics")
   - Overview (brief description)
   - Key findings (one per line)

---

### Step 3: Generate Newsletter (Preview & Generate Tab)

1. **Review Settings:**
   - Check cover preview info
   - Verify newsletter stats

2. **Click "Generate Newsletter"** 🚀

3. **Wait for Processing:**
   - 📸 Generating cover image...
   - 🧠 Building knowledge graph...
   - 🔑 Extracting medical terms...
   - 📚 Generating glossary...
   - 📄 Creating HTML...
   - 💾 Saving newsletter...

4. **Success! You'll see:**
   - ✅ Success message with 🎈 balloons
   - 📊 Newsletter statistics
   - 📥 Download button
   - 👁️ Live preview

---

### Step 4: Download & Share

**Download Button:**
```
📥 Download Newsletter HTML
```
- Saves as `newsletter_YYYYMMDD_HHMMSS.html`
- Self-contained (includes all images)
- Ready to share or print

**Preview:**
- Expander shows live rendered newsletter
- Scrollable view
- Exactly how it will look when opened

---

## 📊 Knowledge Graph Tab

View detailed analysis of your newsletter:

### Metrics Dashboard
- **Cancer Types** - Number of cancer types mentioned
- **Treatments** - Treatment approaches identified
- **Biomarkers** - Genetic markers found
- **Diagnostics** - Diagnostic methods mentioned

### Top 15 Entities
- Ranked by importance score
- Shows entity type
- Displays centrality score

### Medical Relationships
- Sample of identified relationships
- Shows context from newsletter
- Examples:
  - "Immunotherapy treats Lung Cancer"
  - "Mammography diagnoses Breast Cancer"

---

## ℹ️ Help Tab

Complete guide including:
- Quick start instructions
- Cover style descriptions
- AI feature explanations
- Knowledge graph details
- Tips and best practices
- Flux prompt generator (if enabled)

---

## 🎨 Cover Styles Explained

### 1. Professional (Default)
**Best for:** Corporate reports, medical journals, presentations
- Hexagonal geometric pattern
- Purple-blue gradient (#667eea → #764ba2)
- Concentric circles
- Clean and sophisticated

### 2. Modern
**Best for:** Tech conferences, startup pitches, digital media
- Diagonal line pattern
- Bright cyan-blue gradient
- High energy aesthetic
- Contemporary feel

### 3. Abstract
**Best for:** Creative contexts, art exhibitions, non-traditional venues
- Organic blob shapes
- Pink-purple gradient
- Artistic composition
- Eye-catching design

### 4. Scientific
**Best for:** Academic papers, research symposiums, lab presentations
- Network node pattern
- Teal gradient with grid
- Technical aesthetic
- Research-focused

---

## 🤖 AI Features Setup

### OpenAI Glossary (Recommended)

**Setup:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
streamlit run streamlit_newsletter_app.py
```

**Benefits:**
- Professional, accurate definitions
- Context-aware explanations
- Related terms included

**Cost:**
- ~$0.001 per term
- ~$0.015 for 15-term glossary

---

### DALL-E 3 Cover (Optional)

**Setup:**
Same as above (uses same API key)

**Benefits:**
- Custom AI-generated artwork
- Contextual imagery
- Unique every time

**Cost:**
- ~$0.04 per image (1792×1024)

---

### Flux Prompt (FREE Alternative)

**How to Use:**
1. ☑️ Enable "Show Flux Prompt" in sidebar
2. Go to Help tab
3. Scroll to "Flux Prompt for CivitAI"
4. Copy positive and negative prompts
5. Visit https://civitai.com/
6. Generate image with recommended settings
7. Download and use in future newsletters

**Benefits:**
- Highest quality images
- FREE on CivitAI
- Community models available

---

## 💡 Pro Tips

### For Best Results:
1. **Use descriptive executive summaries** - More detail = better knowledge graph
2. **Add 3-5 topics** - Optimal for comprehensive coverage
3. **Set OpenAI API key** - Dramatically improves glossary quality
4. **Try different cover styles** - Match to your audience
5. **Preview before downloading** - Ensure everything looks perfect

### Performance Tips:
- First generation takes 10-20 seconds
- Sample data generates fastest
- DALL-E adds 15-20 seconds
- Glossary with GPT adds 5-10 seconds

### Sharing Tips:
- HTML is self-contained (no external dependencies)
- Works in all modern browsers
- Mobile-responsive design
- Print-friendly layout

---

## 🔧 Troubleshooting

### App Won't Start
```bash
# Check Streamlit is installed
pip list | grep streamlit

# If not installed:
pip install streamlit
```

### "Module not found" errors
```bash
# Ensure you're in the correct directory
cd /Users/sankar/sankar/courses/agentic-ai/sv-agentic-ai/AI_NEWS_LANGGRAPH

# Check Python path
python -c "import sys; print(sys.path)"
```

### OpenAI Features Not Working
```bash
# Check API key is set
echo $OPENAI_API_KEY

# If empty, set it:
export OPENAI_API_KEY="sk-your-key-here"

# Restart app
```

### Newsletter Not Generating
- Check that executive summary is filled
- Ensure at least one topic is added
- Try using sample data first
- Check browser console for errors

---

## 📁 Output Files

All generated newsletters are saved to:
```
outputs/newsletters/streamlit_newsletter_YYYYMMDD_HHMMSS.html
```

**File contains:**
- Enhanced cover image (embedded as base64)
- Executive summary with highlighted keywords
- All topics with findings
- Knowledge graph statistics
- Complete glossary
- Responsive CSS styling

---

## 🎓 Example Workflows

### Workflow 1: Quick Demo (30 seconds)
1. Launch app
2. Use default sample data
3. Click "Generate Newsletter"
4. Preview and download

### Workflow 2: Custom Newsletter (5 minutes)
1. Launch app
2. Uncheck "Use Sample Data"
3. Enter your executive summary
4. Add 3 custom topics
5. Choose cover style
6. Generate and download

### Workflow 3: Professional Publication (10 minutes)
1. Launch app
2. Set OpenAI API key
3. Enable "Use OpenAI for Glossary"
4. Enable "Use DALL-E 3 for Cover"
5. Input detailed custom content
6. Choose Professional style
7. Generate
8. Review knowledge graph
9. Download and share

### Workflow 4: CivitAI High-Quality (15 minutes)
1. Launch app
2. Enable "Show Flux Prompt"
3. Input content
4. Generate newsletter (gets Flux prompt)
5. Go to Help tab
6. Copy Flux prompts
7. Visit civitai.com
8. Generate cover there
9. Download cover
10. Regenerate newsletter with downloaded cover

---

## 📞 Support

**Documentation:**
- Main README: `README.md`
- Cover Guide: `COVER_IMAGE_SUMMARY.md`
- Flux Guide: `docs/FLUX_PROMPTS_GUIDE.md`
- KG Guide: `docs/KNOWLEDGE_GRAPH_GUIDE.md`

**Examples:**
- `examples/generate_complete_newsletter.py`
- `examples/regenerate_with_better_cover.py`

---

## 🎉 Summary

The Streamlit app provides:
- ✅ **Zero-code** newsletter generation
- ✅ **Interactive** web interface
- ✅ **Professional** output quality
- ✅ **Flexible** customization
- ✅ **Fast** generation (< 30 seconds)
- ✅ **Beautiful** enhanced covers
- ✅ **Intelligent** knowledge graphs
- ✅ **Accurate** glossaries

**Perfect for:**
- Researchers creating summaries
- Marketing teams making newsletters
- Educators developing materials
- Anyone needing professional cancer research communications

---

**Ready to start? Launch the app now!** 🚀

```bash
streamlit run streamlit_newsletter_app.py
```

