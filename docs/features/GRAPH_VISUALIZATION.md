# Graph Visualization Guide

## Overview

The LangGraph workflow can be visualized in multiple ways using the built-in graph drawing capabilities and IPython.display.

## Quick Start

### Method 1: Python Script (Easiest)

```bash
# Generate and display graph
python display_graph.py
```

This will:
- ✅ Build the workflow graph
- ✅ Generate PNG visualization
- ✅ Save to `docs/workflow_graph.png`
- ✅ Display inline (if in Jupyter/IPython)

### Method 2: Jupyter Notebook (Best for Interactive Use)

```bash
# Install Jupyter if needed
uv pip install jupyter

# Launch notebook
jupyter notebook visualize_graph.ipynb
```

Then run all cells to see the interactive visualization!

### Method 3: Full Generation Script

```bash
# Generate all formats (PNG, Mermaid, Markdown)
python visualize_graph.py
```

## Using IPython.display

The recommended approach for displaying graphs in notebooks:

```python
from IPython.display import Image, display

# Build your graph
from langgraph.graph import StateGraph, END
workflow = StateGraph(WorkflowState)
# ... add nodes and edges ...
app = workflow.compile()

# Get and display the graph
graph = app.get_graph()

try:
    display(Image(graph.draw_mermaid_png()))
except Exception:
    # Fallback if PNG generation fails
    print(graph.draw_mermaid())
```

## Generated Files

After running the visualization scripts:

```
docs/
├── workflow_graph.png        # PNG image (20KB)
├── workflow_graph.mmd         # Mermaid diagram code
└── WORKFLOW_GRAPH.md          # Full documentation with diagram
```

## Viewing the Graph

### Option 1: View PNG File

```bash
# macOS
open docs/workflow_graph.png

# Linux
xdg-open docs/workflow_graph.png

# Windows
start docs/workflow_graph.png
```

### Option 2: View in Markdown (GitHub)

Open `docs/WORKFLOW_GRAPH.md` - GitHub will render the Mermaid diagram automatically!

### Option 3: Interactive Mermaid Editor

1. Copy content from `docs/workflow_graph.mmd`
2. Go to https://mermaid.live
3. Paste and edit interactively

## Code Example

### Basic Display

```python
from IPython.display import Image, display
from ai_news_langgraph.graph import build_multi_agent_graph

# Build workflow
run_func = build_multi_agent_graph()

# Get graph (you need access to the compiled app)
# For now, use the standalone visualization scripts
```

### In Jupyter Notebook

```python
# Cell 1: Setup
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "src"))

# Cell 2: Build Graph
from langgraph.graph import StateGraph, END
from ai_news_langgraph.schemas import WorkflowState

workflow = StateGraph(WorkflowState)
# ... add nodes ...
app = workflow.compile()

# Cell 3: Display
from IPython.display import Image, display
graph = app.get_graph()
display(Image(graph.draw_mermaid_png()))
```

## Graph Structure

The workflow consists of:

**Nodes:**
1. `__start__` - Entry point
2. `fetch_news_for_topic` - Fetch articles
3. `summarize_topic_news` - Summarize articles  
4. `create_executive_summary` - Create overall summary
5. `generate_newsletter` - Generate outputs
6. `__end__` - Exit point

**Edges:**
- **Solid arrows** (→): Direct transitions
- **Dashed arrows** (-.->): Conditional transitions

**Flow:**
```
START
  ↓
fetch_news_for_topic
  ↓
summarize_topic_news
  ├──→ [more topics] → fetch_news_for_topic (LOOP)
  └──→ [all done] → create_executive_summary
                       ↓
                  generate_newsletter
                       ↓
                     END
```

## Customization

### Change Graph Style

Edit the Mermaid code in `docs/workflow_graph.mmd`:

```mermaid
---
config:
  theme: forest  # Change theme
  flowchart:
    curve: basis  # Change curve style
---
```

### Add More Details

Modify `visualize_graph.py` or `display_graph.py` to include:
- Node descriptions
- Edge labels
- Execution times
- Agent information

## Troubleshooting

### Issue: "No module named 'IPython'"

**Solution:**
```bash
uv pip install ipython
```

### Issue: "Cannot generate PNG"

This might require additional dependencies. Fallback options:
1. Use Mermaid text format instead
2. View on https://mermaid.live
3. Use GitHub's Mermaid rendering

### Issue: "Display object but no image shown"

**Solution:** You're in a terminal, not Jupyter. The PNG is still saved to `docs/workflow_graph.png`. Open it with:
```bash
open docs/workflow_graph.png
```

### Issue: "Graph looks wrong"

The visualization scripts create a simplified version for display. For the actual workflow details, see:
- `src/ai_news_langgraph/graph.py` (lines 179-670)
- `docs/ARCHITECTURE.md`

## API Reference

### `graph.draw_mermaid_png()`

Generates PNG image of the graph.

**Returns:** `bytes` - PNG image data

**Example:**
```python
png_data = graph.draw_mermaid_png()
with open("graph.png", "wb") as f:
    f.write(png_data)
```

### `graph.draw_mermaid()`

Generates Mermaid diagram code.

**Returns:** `str` - Mermaid syntax

**Example:**
```python
mermaid_code = graph.draw_mermaid()
print(mermaid_code)
```

### `IPython.display.Image`

Displays image data in Jupyter.

**Args:**
- `data` (bytes): Image data
- `width` (int): Width in pixels
- `height` (int): Height in pixels

**Example:**
```python
from IPython.display import Image, display
display(Image(png_data, width=800))
```

## Best Practices

1. **Use Jupyter for Interactive Work**
   - Best for exploration and presentations
   - Allows inline display and modification

2. **Use Python Scripts for CI/CD**
   - Generate diagrams automatically
   - Include in documentation builds

3. **Commit Generated Files**
   - Save PNG and Mermaid files to git
   - Makes diagrams visible on GitHub

4. **Update Documentation**
   - Regenerate diagrams when workflow changes
   - Keep WORKFLOW_GRAPH.md in sync

## Related Documentation

- [Architecture](ARCHITECTURE.md) - Overall system architecture
- [Workflow Graph](WORKFLOW_GRAPH.md) - Detailed workflow description
- [Tasks Guide](TASKS_GUIDE.md) - Task configuration

## Tools and Resources

- **Mermaid Live Editor**: https://mermaid.live
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **IPython Docs**: https://ipython.readthedocs.io/
- **Jupyter**: https://jupyter.org/

---

**Questions?** Check the [Troubleshooting Guide](TROUBLESHOOTING.md) or open an issue on GitHub.

