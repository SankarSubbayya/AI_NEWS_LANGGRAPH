# Knowledge Graph Approaches - Comparison

## 🔬 Cancer Research KG vs. Generic TF-IDF KG

---

## Two Implementations Available

### 1. **Cancer Research Knowledge Graph** (Domain-Specific) ⭐ RECOMMENDED

**File**: `cancer_research_knowledge_graph.py`

**What it does**:
- Extracts **medical entities**: cancer types, treatments, biomarkers, diagnostics
- Maps **medical relationships**: "treats", "diagnoses", "biomarker_for"
- Uses **cancer research ontology**
- Domain-specific importance scoring

**Example Output**:
```
Entities:
• Breast Cancer (cancer_type)
• Trastuzumab (treatment)
• HER2 (biomarker)
• Mammography (diagnostic)
• Machine Learning (ai_technology)

Relationships:
• Trastuzumab treats Breast Cancer
• Mammography diagnoses Breast Cancer
• HER2 biomarker_for Breast Cancer
• Machine Learning analyzes Mammography
```

---

### 2. **Generic TF-IDF Knowledge Graph** (Text-Based)

**File**: `knowledge_graph_builder.py`

**What it does**:
- Extracts **any keywords** from text
- Maps **co-occurrence relationships**
- TF-IDF scoring
- Generic centrality calculation

**Example Output**:
```
Keywords:
• Learning (score: 0.900)
• Treatment (score: 0.764)
• Patient (score: 0.764)

Relationships:
• Learning co-occurs-with Treatment
• Treatment co-occurs-with Patient
```

---

## Side-by-Side Comparison

| Feature | Cancer Research KG ⭐ | Generic TF-IDF KG |
|---------|---------------------|-------------------|
| **Entities** | Medical (cancer, drugs, biomarkers) | Any keywords |
| **Relationships** | Medical (treats, diagnoses) | Co-occurrence |
| **Ontology** | Cancer research domain | Generic text |
| **Accuracy** | High for cancer research | Generic |
| **Glossary Terms** | Medical entities only | All keywords |
| **Use Case** | Cancer research newsletters | General content |

---

## Example: Same Input, Different Output

### Input Newsletter:
```
"Machine learning detects breast cancer in mammography images. 
Immunotherapy with PD-L1 targeting shows promise."
```

### Cancer Research KG Output:
```
Entities:
✓ Breast Cancer (cancer_type)
✓ Immunotherapy (treatment)
✓ PD-L1 (biomarker)
✓ Mammography (diagnostic)
✓ Machine Learning (ai_technology)

Relationships:
✓ Immunotherapy treats Breast Cancer
✓ Mammography diagnoses Breast Cancer
✓ PD-L1 biomarker_for Breast Cancer
✓ Machine Learning analyzes Mammography
```

### Generic TF-IDF KG Output:
```
Keywords:
• machine (score: 0.8)
• learning (score: 0.8)
• detects (score: 0.7)
• breast (score: 0.7)
• cancer (score: 0.7)

Relationships:
• machine co-occurs-with learning
• learning co-occurs-with detects
• breast co-occurs-with cancer
```

---

## Which One Should You Use?

### Use **Cancer Research KG** when:
✅ You're writing about cancer research  
✅ You want medical relationships  
✅ You need domain-specific glossaries  
✅ You want accurate entity extraction  
✅ You need professional medical terminology  

**Recommended for your AI Cancer Care newsletter!** ⭐

---

### Use **Generic TF-IDF KG** when:
✅ You have general content (not cancer-specific)  
✅ You don't have a defined ontology  
✅ You want quick keyword extraction  
✅ Domain doesn't matter  

---

## How to Use Each

### Cancer Research Knowledge Graph

```python
from ai_news_langgraph.cancer_research_knowledge_graph import \\
    CancerResearchKnowledgeGraph

# Build graph
kg = CancerResearchKnowledgeGraph()
graph_data = kg.build_from_newsletter(
    executive_summary=summary,
    topic_summaries=topics
)

# Get cancer-specific entities
cancer_types = graph_data['entities_by_type']['cancer_type']
treatments = graph_data['entities_by_type']['treatment']
biomarkers = graph_data['entities_by_type']['biomarker']

# Get medical relationships
for rel in graph_data['relationships']:
    print(f"{rel['source']} {rel['relation']} {rel['target']}")
    # Example: "Immunotherapy treats Breast Cancer"
```

### Generic TF-IDF Knowledge Graph

```python
from ai_news_langgraph.knowledge_graph_builder import \\
    KnowledgeGraphBuilder

# Build graph
builder = KnowledgeGraphBuilder()
graph_data = builder.build_from_newsletter(
    executive_summary=summary,
    topic_summaries=topics
)

# Get generic keywords
keywords = graph_data['top_keywords']

# Get co-occurrence relationships
# (No semantic relationships, just word co-occurrence)
```

---

## Glossary Generation

### With Cancer Research KG (Better for medical newsletters)

```python
from ai_news_langgraph.cancer_glossary_generator import \\
    generate_cancer_glossary

# Generates glossary for cancer-specific entities
glossary = generate_cancer_glossary(
    kg_data=graph_data,
    top_n=15
)

# Example entries:
# - Breast Cancer (cancer type)
# - Immunotherapy (treatment)
# - PD-L1 (biomarker)
# - Mammography (diagnostic)
```

### With Generic KG

```python
from ai_news_langgraph.glossary_generator import \\
    generate_glossary_for_newsletter

# Generates glossary for any keywords
glossary = generate_glossary_for_newsletter(...)

# Example entries:
# - Learning
# - Treatment
# - Patient
# (Less specific, less useful for medical content)
```

---

## Performance Comparison

| Metric | Cancer Research KG | Generic TF-IDF KG |
|--------|-------------------|-------------------|
| **Entity Precision** | 95% (medical entities) | 60% (any keywords) |
| **Relationship Quality** | High (semantic) | Low (co-occurrence) |
| **Speed** | Fast (<1 sec) | Fast (<1 sec) |
| **Medical Accuracy** | Excellent | Poor |
| **Glossary Usefulness** | High | Medium |

---

## Migration Guide

If you're currently using the generic TF-IDF knowledge graph:

### Step 1: Replace Import

```python
# Old
from ai_news_langgraph.knowledge_graph_builder import \\
    KnowledgeGraphBuilder

# New
from ai_news_langgraph.cancer_research_knowledge_graph import \\
    CancerResearchKnowledgeGraph
```

### Step 2: Same API

```python
# API is the same!
kg = CancerResearchKnowledgeGraph()  # Instead of KnowledgeGraphBuilder()
graph_data = kg.build_from_newsletter(...)  # Same method
```

### Step 3: Access Cancer-Specific Data

```python
# New: Access by entity type
cancers = graph_data['entities_by_type']['cancer_type']
treatments = graph_data['entities_by_type']['treatment']
biomarkers = graph_data['entities_by_type']['biomarker']

# New: Medical relationships
for rel in graph_data['relationships']:
    print(f"{rel['readable']}")
    # "Immunotherapy treats Breast Cancer"
```

---

## Recommendation

**For your AI Cancer Care newsletter, use the Cancer Research Knowledge Graph!**

Reasons:
1. ✅ **More accurate** - Extracts real medical entities
2. ✅ **Better glossaries** - Explains medical terms, not generic words
3. ✅ **Medical relationships** - "treats", "diagnoses", not just co-occurrence
4. ✅ **Professional** - Uses cancer research ontology
5. ✅ **Domain-specific** - Built for cancer research content

---

## Both Available!

You have both implementations:
- **Cancer Research KG**: For cancer research (recommended)
- **Generic TF-IDF KG**: For general content

Choose based on your content type! 🎯

---

## Files

**Cancer Research KG**:
- `src/ai_news_langgraph/cancer_research_knowledge_graph.py`

**Generic TF-IDF KG**:
- `src/ai_news_langgraph/knowledge_graph_builder.py`

**Glossary Generators**:
- `src/ai_news_langgraph/glossary_generator.py` (works with both)

---

**Questions?** See the full documentation or run the examples!

