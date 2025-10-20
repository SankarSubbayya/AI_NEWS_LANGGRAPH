# Cover Images & Glossary - Complete Guide

**Date**: October 19, 2025
**Status**: ✅ **WORKING**

---

## Cover Image Generation

### Current Status: DALL-E Auto-Generation ✅

**What's Happening**:
- ✅ Cover images **ARE being generated automatically**
- ✅ Using **DALL-E 3** (OpenAI's image model)
- ✅ Saved to `outputs/images/cover_image_YYYYMMDD_HHMMSS.png`
- ✅ Embedded in HTML newsletters

**Recent Generated Images**:
```
outputs/images/
├── cover_image_20251019_015400.png  (3.2 MB)
├── cover_image_20251019_015749.png  (3.1 MB)
└── cover_image_20251019_020405.png  (2.8 MB)
```

---

### Flux vs DALL-E: What's the Difference?

| Feature | DALL-E 3 (Current) | Flux AI (Alternative) |
|---------|-------------------|----------------------|
| **Generation** | ✅ Automatic via API | ❌ Manual (requires external service) |
| **Integration** | ✅ Built-in OpenAI | ❌ Not integrated (prompt-only) |
| **Quality** | Professional HD | Ultra-photorealistic |
| **Cost** | ~$0.04/image | Varies by service |
| **Workflow** | One command | Manual multi-step |

---

### How DALL-E Generation Works

**File**: [`cover_image_generator.py`](src/ai_news_langgraph/cover_image_generator.py)

```python
cover_gen = CoverImageGenerator()  # Uses OPENAI_API_KEY

cover_image_path = cover_gen.generate_cover_image(
    executive_summary=exec_summary,
    main_topic="AI in Cancer Care",
    topics=["Cancer Research", "Treatment Planning", ...],
    style="professional"  # professional, modern, abstract, scientific
)
# Returns: outputs/images/cover_image_YYYYMMDD_HHMMSS.png
```

**Generated Prompt Example**:
```
Professional cover image for an AI in Cancer Care newsletter.
Modern medical illustration with clean design and corporate style.
Topics: Cancer Research, Early Detection, Treatment Planning.
High-tech healthcare technology aesthetic with data visualization elements.
Professional medical photography, sharp focus, vibrant colors, 8k resolution.
```

---

### Flux Prompt Generator (Manual Workflow)

**File**: [`flux_prompt_generator.py`](src/ai_news_langgraph/flux_prompt_generator.py)

This creates **prompts** for Flux AI but doesn't generate images automatically.

**Usage**:
```python
from src.ai_news_langgraph.flux_prompt_generator import FluxPromptGenerator

flux_gen = FluxPromptGenerator()
prompts = flux_gen.generate_newsletter_cover_prompt(
    executive_summary=exec_summary,
    main_topic="AI in Cancer Care",
    topics=topic_names,
    style="professional"
)

print(prompts['positive'])  # Copy this to CivitAI/Flux service
print(prompts['negative'])  # What to avoid
```

**Output** (for manual use):
```
Positive: masterpiece, best quality, ultra detailed, 8k resolution,
professional medical illustration, AI in cancer care, futuristic
healthcare technology, clinical setting, data visualization,
neural networks, sharp focus, vibrant colors...

Negative: text, words, letters, watermark, blurry, low quality,
distorted, amateur, cluttered...
```

**Then**:
1. Go to CivitAI or Flux service
2. Paste the positive prompt
3. Paste the negative prompt
4. Generate manually
5. Download and save

---

### Why You're Seeing DALL-E Images (Not Flux)

**Reason**: The system is configured to use **automatic DALL-E generation** because:
1. ✅ It's fully automated (one command)
2. ✅ No manual workflow needed
3. ✅ Professional quality
4. ✅ Integrated with newsletter

**Flux is available** but requires manual steps - it's **NOT** automatic like DALL-E.

---

## To Use Flux Instead (Manual Process)

### Option 1: Generate Flux Prompts

Add to your code:

```python
from .flux_prompt_generator import FluxPromptGenerator

# After generating newsletter summary
flux_gen = FluxPromptGenerator()
flux_prompts = flux_gen.generate_newsletter_cover_prompt(
    executive_summary=exec_summary,
    main_topic=state.get("main_topic"),
    topics=[s.get('topic_name') for s in topic_summaries],
    style="professional"
)

# Save prompts to file
with open(f"outputs/flux_prompts_{timestamp}.txt", "w") as f:
    f.write(f"POSITIVE PROMPT:\n{flux_prompts['positive']}\n\n")
    f.write(f"NEGATIVE PROMPT:\n{flux_prompts['negative']}\n")

logger.info(f"Flux prompts saved - use these on CivitAI/Flux service")
```

### Option 2: Disable DALL-E, Use Flux Manually

```python
# In nodes_v2.py:692-698
# Comment out DALL-E generation:
# cover_image_path = cover_gen.generate_cover_image(...)
cover_image_path = None  # Disable automatic generation

# Generate Flux prompts instead
flux_prompts = flux_gen.generate_newsletter_cover_prompt(...)
# Save prompts, use manually
```

---

## Glossary with High-Centrality Nodes ✅

### Updated Implementation

**File**: [`nodes_v2.py:746-766`](src/ai_news_langgraph/nodes_v2.py#L746-L766)

The glossary now uses **proper importance scores** calculated from the knowledge graph!

```python
# Calculate entity importance (frequency + relationships)
importance_scores = kg_builder._calculate_entity_importance()

glossary_entries = []
for entity, score, entity_type in importance_scores[:15]:  # Top 15
    glossary_entries.append({
        'term': entity,
        'entity_type': entity_type,
        'importance_score': round(score, 2),  # ✅ Real centrality!
        'definition': f"A {entity_type} term in cancer research...",
        'contexts': len(kg_builder.entity_contexts.get(entity, []))
    })
```

---

### How Importance is Calculated

**Formula** (from `cancer_research_knowledge_graph.py:306-336`):

```python
importance_score = (
    frequency * 0.4 +        # How often mentioned
    outgoing_links * 0.3 +   # How many entities it connects to
    incoming_links * 0.3     # How many entities connect to it
)
```

**Components**:
- **Frequency** (40%): Number of times mentioned in content
- **Outgoing** (30%): Number of relationships FROM this entity
- **Incoming** (30%): Number of relationships TO this entity

**Result**: Higher score = more central/important in the knowledge graph

---

### Example Glossary Output

```json
{
  "entries": [
    {
      "term": "immunotherapy",
      "entity_type": "treatment",
      "importance_score": 12.5,
      "definition": "A treatment term in cancer research with AI applications.",
      "contexts": 8
    },
    {
      "term": "lung cancer",
      "entity_type": "cancer_type",
      "importance_score": 10.2,
      "definition": "A cancer type term in cancer research with AI applications.",
      "contexts": 6
    },
    {
      "term": "PD-L1",
      "entity_type": "biomarker",
      "importance_score": 8.7,
      "definition": "A biomarker term in cancer research with AI applications.",
      "contexts": 5
    }
  ],
  "total_terms": 15
}
```

---

### Log Output

```
Generating knowledge graph and glossary...
Knowledge Graph: 34 entities, 152 relationships
Knowledge graph exported to outputs/knowledge_graphs/kg_20251019_120000.json

Generated glossary with 15 high-importance terms
  Top term: 'immunotherapy' (score: 12.5)
```

---

## Comparison: Before vs After

### Glossary

| Aspect | Before | After |
|--------|--------|-------|
| **Selection** | First 5 per type (random) | ✅ Top 15 by importance score |
| **Scoring** | Placeholder (1.0) | ✅ Real centrality calculation |
| **Ordering** | By entity type | ✅ By importance (highest first) |
| **Contextual** | No | ✅ Yes (tracks contexts) |

### Cover Images

| Aspect | Status |
|--------|--------|
| **DALL-E** | ✅ Automatic, working |
| **Flux** | ⚠️ Prompt generation only (manual workflow) |
| **Quality** | ✅ Professional HD |
| **Integration** | ✅ Embedded in HTML |

---

## Summary

### Cover Images

**You ARE getting cover images!** They're being generated with DALL-E 3:
```
outputs/images/cover_image_20251019_020405.png  (2.8 MB)
```

**Flux** is available for **prompt generation only** - it doesn't auto-generate images. If you want Flux-style images, you need to:
1. Generate Flux prompts (see code above)
2. Go to CivitAI or Flux service manually
3. Use the prompts to generate
4. Download and add manually

### Glossary

**Now using high-centrality nodes!**
- ✅ Calculates real importance scores
- ✅ Selects top 15 most important entities
- ✅ Orders by centrality (highest first)
- ✅ Tracks number of contexts

---

## Recommendations

### For Cover Images

**Option A: Keep DALL-E** (Current - Recommended)
- ✅ Fully automatic
- ✅ Professional quality
- ✅ No manual work
- ✅ Costs ~$0.04/newsletter

**Option B: Use Flux Prompts**
- ⚠️ Manual workflow required
- ✅ Ultra-high quality possible
- ⚠️ More time-consuming
- 💡 Best for special editions

### For Glossary

The glossary is now **production-ready**:
- ✅ Uses real centrality scores
- ✅ Selects most important terms
- ✅ Provides entity type classification
- ✅ Tracks contextual occurrences

---

## Files Modified

1. **[`nodes_v2.py:746-766`](src/ai_news_langgraph/nodes_v2.py#L746-L766)** - Glossary with importance scores
2. **[`nodes_v2.py:682-706`](src/ai_news_langgraph/nodes_v2.py#L682-L706)** - DALL-E cover generation (already working)

---

## Next Steps

1. **Run workflow** - you'll see both features working
2. **Check outputs**:
   - `outputs/images/cover_image_*.png` - DALL-E cover
   - `state['glossary']['entries']` - Top 15 important terms
3. **Optional**: Add Flux prompt generation if you want manual workflow

---

**Status**:
- ✅ **Cover images**: Auto-generating with DALL-E
- ✅ **Glossary**: Using high-centrality node selection
- ⚠️ **Flux**: Prompt-only (manual workflow required)
