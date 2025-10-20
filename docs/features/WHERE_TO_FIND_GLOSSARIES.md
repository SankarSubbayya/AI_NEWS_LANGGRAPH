# Where to Find Glossaries 📖

## Quick Answer

**Glossaries are embedded in your HTML newsletters!** They are NOT saved as separate files.

## Location

### 📁 Primary Location: HTML Newsletters
```
outputs/newsletters/streamlit_newsletter_*.html
```

Each newsletter contains a **"Medical Glossary"** section with 15 AI-generated medical term definitions.

## How to View Glossaries

### Method 1: Open Newsletter in Browser
```bash
# Open the latest newsletter
open outputs/newsletters/streamlit_newsletter_*.html

# Or specific file
open outputs/newsletters/streamlit_newsletter_20251019_031525.html
```

Then scroll down to the **📖 Medical Glossary** section.

### Method 2: Extract from HTML via Command Line
```bash
# View glossary section from latest newsletter
grep -A 50 "Medical Glossary" outputs/newsletters/streamlit_newsletter_*.html | tail -100
```

### Method 3: Via Streamlit App
1. Run: `streamlit run streamlit_newsletter_app.py`
2. Generate newsletter
3. Scroll down in preview to see glossary

## What's in the Glossary

Each glossary contains **15 terms** selected from the knowledge graph with:

### Term Information:
- **Term Name**: e.g., "NGS", "Clinical Trial", "Immunotherapy"
- **Category**: e.g., "Diagnostic", "Treatment", "Technology"
- **AI-Generated Definition**: 1-2 sentences of context-specific explanation
- **Importance Score**: Based on centrality in knowledge graph
- **Related Terms**: Connected entities from knowledge graph

### Example Glossary Entry:
```
NGS (Diagnostic)
Next-Generation Sequencing (NGS) is a revolutionary diagnostic technology
that allows for the rapid sequencing of DNA and RNA, enabling comprehensive
analysis of genetic mutations associated with cancer...
```

## Sample Terms You'll Find

Recent newsletters include terms like:
- **NGS** - Next-Generation Sequencing
- **Clinical Trial** - Research studies
- **Screening** - Early detection methods
- **Genomics** - Genetic analysis
- **Immunotherapy** - Treatment approach
- **Biomarker** - Diagnostic indicators
- **Precision Medicine** - Targeted treatment
- **Deep Learning** - AI technology
- **Tumor** - Cancer growth
- **Radiomics** - Imaging analysis

## How Glossaries Are Generated

### Pipeline:
1. **Newsletter content** → Knowledge graph extraction
2. **Knowledge graph** → Top 15 entities by importance
3. **Entity selection** → AI definition generation (GPT-4o-mini)
4. **Formatted output** → Embedded in HTML newsletter

### Where in the HTML:
Look for this section structure:
```html
<!-- Medical Glossary -->
<div class="section" style="background: linear-gradient(...)">
    <h2>📖 Medical Glossary</h2>
    <p>Key medical and AI terms from this cancer research newsletter</p>

    <!-- Term entries -->
    <div style="background: white; ...">
        <h3>Term Name</h3>
        <span>Category</span>
        <p>AI-generated definition...</p>
    </div>
    ...
</div>
```

## Extract Glossary to Separate File

If you want glossaries as separate files, here's a quick script:

```python
# extract_glossary.py
import re
from bs4 import BeautifulSoup
import json

def extract_glossary(html_file):
    with open(html_file, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Find glossary section
    glossary_section = soup.find('h2', string=re.compile('Medical Glossary'))

    if not glossary_section:
        return []

    glossary_entries = []
    parent = glossary_section.find_parent('div')

    for entry in parent.find_all('div', style=re.compile('background: white')):
        term = entry.find('h3').text.strip()
        category = entry.find('span').text.strip()
        definition = entry.find('p').text.strip()

        glossary_entries.append({
            'term': term,
            'category': category,
            'definition': definition
        })

    return glossary_entries

# Extract from latest newsletter
latest = "outputs/newsletters/streamlit_newsletter_20251019_031525.html"
glossary = extract_glossary(latest)

# Save as JSON
with open('outputs/glossary_extracted.json', 'w') as f:
    json.dump(glossary, f, indent=2)

print(f"Extracted {len(glossary)} terms")
```

## Why Embedded in HTML?

Glossaries are embedded in newsletters because:
1. **Context**: They're specific to that newsletter's content
2. **Convenience**: Everything in one file for distribution
3. **Integration**: Seamlessly part of the newsletter design
4. **No extra files**: Simpler to manage and share

## Quick Commands

### View Latest Glossary
```bash
# See glossary terms in latest newsletter
ls -t outputs/newsletters/*.html | head -1 | xargs grep -A 5 "Medical Glossary"
```

### Count Glossary Terms
```bash
# Count terms in latest newsletter
grep -c '<h3 style="color: #2d3748' outputs/newsletters/streamlit_newsletter_*.html | tail -1
```

### Extract All Terms
```bash
# Get all term names
grep '<h3 style="color: #2d3748' outputs/newsletters/streamlit_newsletter_*.html | \
    sed 's/.*<h3.*>//' | sed 's/<\/h3>//' | sort | uniq
```

## Summary

✅ **Glossaries ARE being generated** - In every newsletter
✅ **Location**: Inside HTML newsletters (`outputs/newsletters/*.html`)
✅ **Content**: 15 AI-generated medical term definitions
✅ **Based on**: Knowledge graph with importance scoring
✅ **Quality**: Professional, contextual definitions via GPT-4o-mini

To see your glossaries:
1. Open any recent newsletter HTML file
2. Scroll to "📖 Medical Glossary" section
3. You'll see 15 beautifully formatted term definitions!

## Want Separate Glossary Files?

If you'd prefer glossaries saved as separate JSON/MD files, I can modify the code to:
- Save glossaries to `outputs/glossaries/glossary_*.json`
- Export as markdown files
- Create a glossary database

Just let me know if you want this feature added!