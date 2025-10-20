# Flux Automatic Image Generation - Complete Guide

## Overview

The system now **automatically generates Flux AI images** using Replicate's API, in addition to DALL-E images. You no longer need to manually copy prompts to CivitAI - Flux images are created automatically during newsletter generation!

## What's New

### Before (Previous Behavior)
- ✅ DALL-E images auto-generated
- ❌ Flux prompts saved to file (manual generation required)
- 🔧 User had to copy prompts to CivitAI manually

### Now (New Behavior)
- ✅ DALL-E images auto-generated
- ✅ **Flux images auto-generated via Replicate API**
- ✅ Flux prompts still saved (as backup for manual generation)
- 🚀 Fully automated workflow!

## Setup Instructions

### 1. Get Your Replicate API Token

1. Go to [https://replicate.com/account/api-tokens](https://replicate.com/account/api-tokens)
2. Sign up or log in
3. Create a new API token
4. Copy the token (starts with `r8_...`)

### 2. Add Token to Environment

Add to your `.env` file:

```bash
# Required for Flux image generation
REPLICATE_API_TOKEN=r8_your_token_here

# Existing tokens (still needed)
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

### 3. Install Dependencies

```bash
# Install the replicate library
pip install replicate

# Or if using uv:
uv pip install replicate

# Or reinstall the project:
pip install -e .
```

### 4. Run Newsletter Generation

```bash
# Just run normally - Flux images will auto-generate!
python -m ai_news_langgraph.main

# Or via Streamlit:
streamlit run streamlit_newsletter_app.py
```

## How It Works

### Workflow Overview

1. **DALL-E Image Generation** (~5-10 seconds)
   - Generates quick, good-quality cover image
   - Uses OpenAI DALL-E 3 API
   - Saves to `outputs/images/cover_*.png`

2. **Flux Image Generation** (~10-30 seconds)
   - Generates high-quality, photorealistic cover image
   - Uses Replicate API with Flux Schnell model
   - Saves to `outputs/images/flux_cover_*.png`

3. **Flux Prompt Backup** (instant)
   - Saves prompts to `outputs/flux_prompts/flux_prompts_*.txt`
   - Includes instructions for manual generation
   - Useful if auto-generation fails or you want to regenerate

### Image Comparison

| Feature | DALL-E 3 | Flux Schnell | Flux Dev |
|---------|----------|--------------|----------|
| **Generation Time** | 5-10 sec | 10-15 sec | 20-30 sec |
| **Quality** | Good | Excellent | Outstanding |
| **Style** | Artistic | Photorealistic | Ultra-realistic |
| **Cost** | ~$0.04/image | ~$0.003/image | ~$0.055/image |
| **Auto-Generated?** | ✅ Yes | ✅ Yes | ✅ Yes (change model) |

### Model Selection

The system uses **Flux Schnell** by default (fast + cheap). To use **Flux Dev** (higher quality):

Edit [src/ai_news_langgraph/flux_image_generator.py](src/ai_news_langgraph/flux_image_generator.py:88):

```python
# Line 88: Change this
model = "black-forest-labs/flux-schnell"  # Fast (default)

# To this for higher quality:
model = "black-forest-labs/flux-dev"  # Higher quality, slower
```

## Output Files

After running, you'll find:

```
outputs/
├── images/
│   ├── cover_20251019_123456.png          # DALL-E image
│   └── flux_cover_20251019_123456.png     # Flux image ⭐ NEW!
├── flux_prompts/
│   └── flux_prompts_20251019_123456.txt   # Backup prompts
└── newsletters/
    └── newsletter_20251019_123456.html     # Newsletter
```

## What Happens Without API Token

If `REPLICATE_API_TOKEN` is not set:

```
⏭️  Flux image generation skipped (no REPLICATE_API_TOKEN)
   Get your token at: https://replicate.com/account/api-tokens
```

- DALL-E images still generate normally
- Flux prompts still saved to file
- You can add token later and regenerate

## Manual Generation (If Needed)

If you want to manually regenerate Flux images:

1. Check `outputs/flux_prompts/flux_prompts_*.txt`
2. Open [CivitAI](https://civitai.com/generate) or [Replicate](https://replicate.com)
3. Copy the **POSITIVE PROMPT**
4. Select Flux Schnell or Flux Dev
5. Generate!

## Testing Flux Generation

Test the Flux generator directly:

```bash
# Set your token first
export REPLICATE_API_TOKEN=r8_your_token_here

# Run test
python -m ai_news_langgraph.flux_image_generator
```

Expected output:
```
🧪 Testing Flux image generation...
Topic: AI in Cancer Care
Sub-topics: Cancer Research, Early Detection, Treatment Planning
🎨 Generating Flux image via Replicate API...
📝 Prompt: Professional cover image for an AI in Cancer Care newsletter...
⬇️  Downloading Flux image from https://replicate.delivery/...
✅ Flux image saved: outputs/images/flux_cover_20251019_123456.png
✅ Test successful! Image saved to: outputs/images/flux_cover_20251019_123456.png
```

## Cost Comparison

### Per Newsletter Generation

| Service | Images | Cost | Total |
|---------|--------|------|-------|
| **OpenAI DALL-E** | 1 cover | $0.04 | $0.04 |
| **Replicate Flux Schnell** | 1 cover | $0.003 | $0.003 |
| **Replicate Flux Dev** | 1 cover | $0.055 | $0.055 |

**Recommendation**: Use Flux Schnell (default) - it's 10x cheaper than DALL-E and produces excellent results!

### Monthly Estimates (30 newsletters)

- DALL-E only: $1.20/month
- DALL-E + Flux Schnell: $1.29/month (+$0.09)
- DALL-E + Flux Dev: $2.85/month (+$1.65)

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'replicate'"

```bash
pip install replicate
```

### Error: "REPLICATE_API_TOKEN not found"

Add to `.env`:
```bash
REPLICATE_API_TOKEN=r8_your_actual_token_here
```

### Error: "Replicate returned no image output"

- Check your API token is valid
- Check you have credits on Replicate
- Check network connectivity
- Review Replicate dashboard for errors

### Images Taking Too Long

- Flux Schnell: Should take 10-15 seconds
- Flux Dev: Can take 20-30 seconds
- If longer: Check Replicate status page

### Want Higher Quality Images

Change model from `flux-schnell` to `flux-dev` in [flux_image_generator.py:88](src/ai_news_langgraph/flux_image_generator.py#L88)

## API Documentation

- **Replicate Flux Schnell**: [https://replicate.com/black-forest-labs/flux-schnell](https://replicate.com/black-forest-labs/flux-schnell)
- **Replicate Flux Dev**: [https://replicate.com/black-forest-labs/flux-dev](https://replicate.com/black-forest-labs/flux-dev)
- **Replicate API Docs**: [https://replicate.com/docs](https://replicate.com/docs)

## FAQ

### Q: Do I need both DALL-E and Flux?

**A:** No, but recommended:
- DALL-E: Good quality, fast, reliable
- Flux: Excellent quality, photorealistic, cheaper
- Having both gives you options!

### Q: Which image is used in the newsletter?

**A:** Currently DALL-E. To use Flux, update the HTML template to reference `flux_image` instead of `cover_image`.

### Q: Can I disable DALL-E and only use Flux?

**A:** Yes, comment out the DALL-E generation section in [nodes_v2.py:695-708](src/ai_news_langgraph/nodes_v2.py#L695-L708)

### Q: Can I use both images in the newsletter?

**A:** Yes! Both paths are available:
- `state['outputs']['cover_image']` - DALL-E
- `state['outputs']['flux_image']` - Flux

### Q: What if I don't want Flux auto-generation?

**A:** Simply don't set `REPLICATE_API_TOKEN`. The system will skip Flux generation and only save prompts.

## Implementation Details

### Files Modified

1. **[pyproject.toml](pyproject.toml)** - Added `replicate>=0.25.0` dependency
2. **[flux_image_generator.py](src/ai_news_langgraph/flux_image_generator.py)** - NEW: Auto-generation class
3. **[nodes_v2.py:682-788](src/ai_news_langgraph/nodes_v2.py#L682-L788)** - Integrated Flux generation
4. **[nodes_v2.py:923-933](src/ai_news_langgraph/nodes_v2.py#L923-L933)** - Added `flux_image` to outputs

### Key Features

- ✅ Automatic Flux image generation via Replicate
- ✅ Graceful fallback if token not available
- ✅ Error handling and logging
- ✅ Backup prompts still saved
- ✅ Configurable model selection
- ✅ Aspect ratio control (16:9 for newsletters)
- ✅ PNG format with 90% quality

## Next Steps

1. ✅ Get Replicate API token
2. ✅ Add to `.env` file
3. ✅ Run newsletter generation
4. ✅ Check `outputs/images/` for both DALL-E and Flux images
5. ✅ Compare quality and decide which to use!

## Summary

You now have **fully automated Flux image generation**! No more manual copying of prompts. Just run the newsletter generation and get beautiful, photorealistic Flux images automatically.

**Total time added to workflow**: ~10-15 seconds (Flux Schnell)
**Total cost added per newsletter**: ~$0.003 (less than half a cent!)
**Quality improvement**: Significant - photorealistic vs artistic

🎉 Enjoy your automated, high-quality newsletter cover images!
