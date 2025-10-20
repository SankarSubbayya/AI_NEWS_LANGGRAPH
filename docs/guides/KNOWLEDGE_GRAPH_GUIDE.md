# Knowledge Graph & Glossary Builder

**Purpose**: Extract keywords, build knowledge graphs, and generate AI-powered glossaries for newsletter content  
**Status**: ✅ Fully Implemented  
**Date**: October 19, 2025

---

## 📖 Overview

The **Knowledge Graph & Glossary Builder** automatically analyzes your newsletter content to:

1. **Extract Keywords** - Identify the most important terms
2. **Build Knowledge Graphs** - Map relationships between concepts
3. **Calculate Centrality** - Find the most influential terms
4. **Generate Glossaries** - Create AI-powered definitions for key terms

This enhances your newsletter by providing context and helping readers understand complex terminology.

---

## ✨ Key Features

### 1. **Keyword Extraction** 🔑
- Automatically extracts important terms
- Ranks by frequency, centrality, and importance
- Filters noise and stop words
- Multi-word term support (n-grams)

### 2. **Knowledge Graph Building** 🕸️
- Maps relationships between terms
- Identifies co-occurrence patterns
- Calculates term centrality (influence)
- Categorizes terms by domain

### 3. **Centrality Analysis** 📊
- Finds most influential terms
- Measures term connectivity
- Ranks by importance
- Identifies key concepts

### 4. **AI-Powered Glossaries** 📚
- Generates definitions using GPT-4
- Focuses on high-centrality terms
- Context-aware explanations
- Beautiful HTML/Markdown formatting

---

## 🚀 Quick Start

### Basic Usage

```python
from ai_news_langgraph.knowledge_graph_builder import KnowledgeGraphBuilder
from ai_news_langgraph.glossary_generator import generate_glossary_for_newsletter

# Your newsletter content
executive_summary = "AI revolutionizes cancer treatment..."
topic_summaries = [...]

# Build knowledge graph
builder = KnowledgeGraphBuilder()
graph_data = builder.build_from_newsletter(
    executive_summary,
    topic_summaries
)

print(f"Extracted {graph_data['total_terms']} terms")
print(f"Found {graph_data['total_relationships']} relationships")

# Top keywords
for kw in graph_data['top_keywords'][:10]:
    print(f"{kw['term']}: {kw['score']}")
```

### Generate Glossary

```python
# Generate AI-powered glossary
result = generate_glossary_for_newsletter(
    executive_summary,
    topic_summaries,
    top_n=15,
    output_format="html"
)

# Use in newsletter
glossary_html = result['html']
glossary_entries = result['glossary']

print(f"Generated {result['total_terms']} definitions")
```

---

## 📊 Knowledge Graph Features

### What is a Knowledge Graph?

A knowledge graph represents terms (nodes) and their relationships (edges):

```
    Machine Learning
         ↓    ↓
    Cancer  Treatment
         ↓    ↓
      Diagnosis
```

### Building the Graph

```python
from ai_news_langgraph.knowledge_graph_builder import KnowledgeGraphBuilder

builder = KnowledgeGraphBuilder()

# From newsletter content
graph_data = builder.build_from_newsletter(
    executive_summary="...",
    topic_summaries=[...],
    articles=[...]  # optional
)

# Graph statistics
print(f"Terms: {graph_data['total_terms']}")
print(f"Relationships: {graph_data['total_relationships']}")

# Top keywords
for kw in graph_data['top_keywords']:
    print(f"{kw['term']}: score={kw['score']}, connections={kw['connections']}")

# High centrality terms (most influential)
for term, score in graph_data['high_centrality_terms']:
    print(f"{term}: centrality={score}")
```

### Centrality Calculation

**Centrality** measures how "influential" a term is based on:
1. **Connections** - How many other terms it relates to
2. **Frequency** - How often it appears
3. **Context** - Where it appears (e.g., executive summary = more important)

**High centrality terms** are good candidates for glossary definitions.

---

## 📚 Glossary Generation

### How It Works

1. **Extract Terms** - Knowledge graph identifies key terms
2. **Calculate Centrality** - Ranks terms by importance
3. **Generate Definitions** - GPT-4 creates context-aware explanations
4. **Format Output** - Beautiful HTML or Markdown

### Basic Glossary

```python
from ai_news_langgraph.glossary_generator import GlossaryGenerator

# Build knowledge graph first
kg_builder = KnowledgeGraphBuilder()
kg_builder.build_from_newsletter(exec_summary, topics)

# Generate glossary
glossary_gen = GlossaryGenerator()
glossary = glossary_gen.generate_from_knowledge_graph(
    kg_builder,
    min_centrality=0.1,  # Only terms with centrality > 0.1
    top_n=15,            # Maximum 15 terms
    context="AI in Cancer Care"
)

# Each entry contains:
for entry in glossary:
    print(f"Term: {entry['term']}")
    print(f"Definition: {entry['definition']}")
    print(f"Related: {entry['related_terms']}")
    print(f"Importance: {entry['importance']}")  # high, medium, low
```

### HTML Formatting

```python
# Format as beautiful HTML
html = glossary_gen.format_glossary_html(glossary)

# Use in newsletter
newsletter_html = f"""
<html>
  <body>
    {newsletter_content}
    {html}  <!-- Add glossary at the end -->
  </body>
</html>
"""
```

### Markdown Formatting

```python
# Format as Markdown
markdown = glossary_gen.format_glossary_markdown(glossary)

# Save or display
with open('glossary.md', 'w') as f:
    f.write(markdown)
```

---

## 🎯 Advanced Features

### Export Graph to JSON

```python
# Export complete graph data
builder.export_graph_json('outputs/knowledge_graph.json')
```

**Output includes**:
- All terms and frequencies
- All relationships
- Contexts where terms appear
- Metadata

### Visualization Data

```python
# Get data for visualization libraries (D3.js, NetworkX, etc.)
viz_data = builder.visualize_graph_data()

# Nodes
for node in viz_data['nodes']:
    print(f"Node: {node['label']}")
    print(f"  Frequency: {node['frequency']}")
    print(f"  Centrality: {node['centrality']}")
    print(f"  Category: {node['group']}")

# Edges (relationships)
for edge in viz_data['edges']:
    print(f"Edge: {edge['source']} -> {edge['target']}")
    print(f"  Weight: {edge['weight']}")
```

### Custom Term Categories

The system automatically categorizes terms:

- **cancer** - Cancer-related terms
- **ai_ml** - AI/ML terms
- **medical** - Medical procedures
- **research** - Research-related
- **other** - General terms

```python
# Get category distribution
viz_data = builder.visualize_graph_data()
categories = {}
for node in viz_data['nodes']:
    group = node['group']
    categories[group] = categories.get(group, 0) + 1

for category, count in categories.items():
    print(f"{category}: {count} terms")
```

---

## 💡 Use Cases

### 1. Newsletter Enhancement

**Problem**: Readers unfamiliar with technical terms  
**Solution**: Auto-generate glossary for complex terms

```python
# Generate glossary for newsletter
result = generate_glossary_for_newsletter(
    executive_summary,
    topic_summaries,
    top_n=15
)

# Add to newsletter
newsletter_with_glossary = newsletter_html + result['html']
```

### 2. Keyword Extraction for SEO

**Problem**: Need keywords for search optimization  
**Solution**: Extract top keywords automatically

```python
builder = KnowledgeGraphBuilder()
graph_data = builder.build_from_newsletter(...)

# Top 20 keywords for SEO
seo_keywords = [kw['term'] for kw in graph_data['top_keywords'][:20]]
```

### 3. Content Analysis

**Problem**: Understanding content themes  
**Solution**: Analyze knowledge graph structure

```python
# Most connected terms = main themes
for term, score in graph_data['high_centrality_terms'][:10]:
    print(f"Main theme: {term}")
```

### 4. Related Content Discovery

**Problem**: Finding related terms for tag clouds  
**Solution**: Use graph relationships

```python
# Get related terms for a specific term
term = "machine learning"
related = list(builder.graph.get(term, []))[:10]
print(f"Related to '{term}': {related}")
```

---

## 🎨 Glossary Formatting Examples

### HTML Output (Styled)

```html
<div class="glossary-section" style="...">
  <h2>📚 Key Terms Glossary</h2>
  
  <div class="glossary-entry" style="...">
    <h3>Machine Learning</h3>
    <span class="importance-badge">⭐ High Priority</span>
    <p>A subset of artificial intelligence that enables computers to learn from data...</p>
    <div class="related-terms">
      Related: Artificial Intelligence, Deep Learning, Neural Networks
    </div>
  </div>
  
  <!-- More entries... -->
</div>
```

### Markdown Output

```markdown
# 📚 Key Terms Glossary

## ⭐ High Priority Terms

### Machine Learning

A subset of artificial intelligence that enables computers to learn from data...

**Related terms**: Artificial Intelligence, Deep Learning, Neural Networks

---

### Artificial Intelligence

...
```

---

## 📈 Performance & Scalability

### Processing Speed

| Newsletter Size | Terms Extracted | Graph Build Time | Glossary Generation |
|----------------|-----------------|------------------|---------------------|
| Small (500 words) | 50-100 | < 1 sec | 10-20 sec |
| Medium (2000 words) | 150-300 | 1-2 sec | 20-40 sec |
| Large (5000 words) | 300-500 | 2-4 sec | 40-80 sec |

### Optimization Tips

1. **Limit top_n** - Only generate glossaries for top 10-15 terms
2. **Cache results** - Store generated glossaries
3. **Batch processing** - Generate glossaries offline
4. **Use GPT-4o-mini** - Faster and cheaper than GPT-4

---

## 🔧 Configuration

### Knowledge Graph Builder

```python
builder = KnowledgeGraphBuilder()

# Customize domain terms
builder.DOMAIN_TERMS.add('your_custom_term')

# Customize stop words
builder.STOP_WORDS.add('exclude_this_word')

# Build with custom settings
graph_data = builder.build_from_newsletter(...)
```

### Glossary Generator

```python
glossary_gen = GlossaryGenerator(
    model="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo"
    temperature=0.3       # 0-1, lower = more consistent
)

glossary = glossary_gen.generate_from_knowledge_graph(
    kg_builder,
    min_centrality=0.1,  # Threshold for inclusion
    top_n=15,            # Max terms
    context="Your domain context"
)
```

---

## 💰 Cost Considerations

### GPT-4o-mini Pricing (Recommended)

- **Input**: $0.15 / 1M tokens
- **Output**: $0.60 / 1M tokens

**Typical Glossary Costs**:
- 15 terms × ~100 tokens each = ~1,500 tokens input
- 15 terms × ~50 tokens each = ~750 tokens output
- **Total cost**: ~$0.0005 per glossary (< $0.001)

### Monthly Costs

| Frequency | Cost (GPT-4o-mini) |
|-----------|-------------------|
| Daily | $0.015 - $0.03 |
| Weekly | $0.004 - $0.008 |
| Monthly | $0.001 - $0.002 |

**Very affordable!**

---

## 🎓 Best Practices

### 1. Choose the Right Number of Terms

**Too few (< 10)**: Misses important concepts  
**Too many (> 20)**: Overwhelming for readers  
**Sweet spot**: **12-15 terms**

### 2. Set Appropriate Centrality Threshold

```python
# Conservative (only very important terms)
min_centrality = 0.3

# Balanced (recommended)
min_centrality = 0.1

# Inclusive (more terms)
min_centrality = 0.05
```

### 3. Provide Context

```python
# Good: Specific context
glossary_gen.generate_from_knowledge_graph(
    kg_builder,
    context="AI-powered cancer diagnostics"
)

# Less good: Vague context
context="cancer research"
```

### 4. Format for Your Audience

- **General public**: Simple definitions, avoid jargon
- **Healthcare professionals**: Technical but clear
- **Researchers**: Detailed, academic style

Adjust the GPT-4 prompt in `GlossaryGenerator._generate_definition()` to match your audience.

---

## 🔍 Examples

### Example 1: Basic Keyword Extraction

```python
from ai_news_langgraph.knowledge_graph_builder import build_knowledge_graph_from_newsletter

# Simple one-liner
graph_data = build_knowledge_graph_from_newsletter(
    executive_summary="AI revolutionizes cancer care...",
    topic_summaries=[...]
)

# Get top keywords
for kw in graph_data['top_keywords'][:10]:
    print(f"{kw['term']}: {kw['score']}")
```

### Example 2: Complete Glossary Workflow

```python
from ai_news_langgraph.glossary_generator import generate_glossary_for_newsletter

# One function does it all
result = generate_glossary_for_newsletter(
    executive_summary=exec_summary,
    topic_summaries=topics,
    articles=articles,
    top_n=15,
    output_format="both"  # HTML and Markdown
)

# Use results
glossary_html = result['html']
glossary_markdown = result['markdown']
glossary_data = result['glossary']

# Save
with open('glossary.html', 'w') as f:
    f.write(glossary_html)
```

### Example 3: Interactive Graph Visualization

```python
# Get visualization data
viz_data = builder.visualize_graph_data()

# Export for D3.js, Cytoscape.js, etc.
import json
with open('graph_viz.json', 'w') as f:
    json.dump(viz_data, f)

# Or use NetworkX for Python visualization
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
for node in viz_data['nodes']:
    G.add_node(node['id'], **node)
for edge in viz_data['edges']:
    G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

nx.draw(G, with_labels=True)
plt.show()
```

---

## 🆘 Troubleshooting

### Issue 1: Too Many Generic Terms

**Problem**: Keywords include common words like "the", "and"

**Solution**: Already handled by STOP_WORDS, but you can add more:
```python
builder.STOP_WORDS.update(['word1', 'word2', 'word3'])
```

### Issue 2: Missing Domain-Specific Terms

**Problem**: Important domain terms not recognized

**Solution**: Add to DOMAIN_TERMS:
```python
builder.DOMAIN_TERMS.update([
    'your_term_1',
    'your_term_2',
    'multi word term'
])
```

### Issue 3: Glossary Definitions Too Technical

**Problem**: Definitions too complex for audience

**Solution**: Adjust the system prompt in `glossary_generator.py`:
```python
# Make it simpler
system_message = """Generate simple, easy-to-understand definitions 
suitable for a general audience..."""
```

### Issue 4: Slow Glossary Generation

**Problem**: Takes too long to generate definitions

**Solution**:
1. Reduce `top_n` to 10 or fewer
2. Use `gpt-3.5-turbo` instead of `gpt-4`
3. Batch generate glossaries offline

---

## 📚 Additional Resources

- **Examples**: `examples/generate_knowledge_graph.py`
- **Source**: `src/ai_news_langgraph/knowledge_graph_builder.py`
- **Glossary Generator**: `src/ai_news_langgraph/glossary_generator.py`
- **NetworkX Docs**: https://networkx.org/
- **D3.js for Graphs**: https://d3js.org/

---

## 🆕 Future Enhancements

Planned features:
- [ ] Interactive graph visualization in HTML
- [ ] Temporal knowledge graphs (track term evolution over time)
- [ ] Semantic similarity between terms
- [ ] Auto-linking terms in newsletter content
- [ ] Export to graph databases (Neo4j)
- [ ] Multi-language support
- [ ] Entity recognition for people, organizations
- [ ] Automatic taxonomy generation

---

**🎉 Ready to enhance your newsletter with knowledge graphs and glossaries!**

For more information, see:
- [README.md](../README.md) - Project overview
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture

---

**Questions?** Check the examples or open an issue!

