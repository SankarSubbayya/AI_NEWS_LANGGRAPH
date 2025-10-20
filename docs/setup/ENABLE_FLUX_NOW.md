# Enable Flux Image Generation (2 Minutes)

## You're Almost There! 🎉

Your system is **fully configured** and ready for Flux image generation. You're just missing the API token.

## Current Status

✅ **Working:**
- Knowledge graphs generating
- AI-powered glossaries in newsletters
- DALL-E cover images
- Flux prompts being saved

⏸️ **Waiting for Token:**
- Flux auto-image generation (needs REPLICATE_API_TOKEN)

## Quick Setup (2 Minutes)

### Step 1: Get Your FREE Replicate Token

1. Open: **https://replicate.com/account/api-tokens**
2. Sign up with GitHub/Google (free!)
3. Click "**Create Token**"
4. Copy the token (looks like `r8_abc123...`)

### Step 2: Add Token to .env File

Open `.env` file and **uncomment + paste your token**:

```bash
# Change this line (currently commented):
# REPLICATE_API_TOKEN=r8_paste_your_token_here

# To this (uncommented with YOUR token):
REPLICATE_API_TOKEN=r8_your_actual_token_here
```

**Quick edit command:**
```bash
# Open .env in your editor
code .env
# or
nano .env
```

### Step 3: Verify Setup

```bash
# Check token is set
grep REPLICATE_API_TOKEN .env

# Should show:
# REPLICATE_API_TOKEN=r8_your_token_here (not commented!)
```

### Step 4: Generate Newsletter

```bash
# Via Streamlit (recommended)
streamlit run streamlit_newsletter_app.py

# Or via CLI
python -m ai_news_langgraph.main
```

## What You'll See

### Before (Current):
```
⏭️  Flux image generation skipped (no REPLICATE_API_TOKEN)
   Get your token at: https://replicate.com/account/api-tokens
✓ Flux prompts saved: outputs/flux_prompts/flux_prompts_*.txt
  → Use these prompts on CivitAI for manual ultra-high-quality Flux images
```

### After (With Token):
```
✅ Flux image generator initialized with Replicate API
🎨 Generating Flux cover image (this may take 10-30 seconds)...
📝 Prompt: Professional cover image for an AI in Cancer Care newsletter...
⬇️  Downloading Flux image from https://replicate.delivery/...
✅ Flux image saved: outputs/images/flux_cover_20251019_123456.png
```

## Results

You'll get **TWO cover images** per newsletter:

```
outputs/images/
├── cover_image_*.png       ← DALL-E (artistic, fast)
└── flux_cover_*.png        ← Flux (photorealistic, amazing!) ⭐ NEW
```

## Cost

| Service | Per Image | Quality |
|---------|-----------|---------|
| DALL-E 3 | $0.040 | Good |
| Flux Schnell | **$0.003** | Excellent (10x cheaper!) |

**Replicate Free Tier:** First $5 of credits free - that's ~1,600 Flux images!

## Troubleshooting

### "Command not found: python"
```bash
# Use python3 instead
python3 -m ai_news_langgraph.main
```

### "Module 'replicate' not found"
```bash
pip install replicate
# or
uv pip install replicate
```

### Token Not Being Read
```bash
# Make sure line is NOT commented (no # at start)
# Wrong:
# REPLICATE_API_TOKEN=r8_abc123

# Correct:
REPLICATE_API_TOKEN=r8_abc123
```

### Want to Skip Flux?
Just leave the token commented out. System will:
- ✅ Still generate DALL-E images
- ✅ Still save Flux prompts for manual use
- ✅ Continue working normally

## Example .env Configuration

```bash
# Required
OPENAI_API_KEY="sk-proj-..."
TAVILY_API_KEY="tvly-dev-..."

# Optional but Recommended for Flux Auto-Generation
REPLICATE_API_TOKEN=r8_your_token_here  # ← ADD THIS!

# Other optional configs
OPENAI_MODEL=gpt-4o-mini
AI_NEWS_TOPIC="AI in Cancer Care"
```

## Verify Everything Works

After adding token and generating a newsletter:

```bash
# Check for Flux images
ls -lh outputs/images/flux_cover_*.png

# Should show:
# flux_cover_20251019_123456.png  (2-4 MB, photorealistic!)

# Check both images exist
ls -lh outputs/images/cover_*.png outputs/images/flux_cover_*.png
```

## Next Steps

1. ✅ Get token from Replicate
2. ✅ Add to `.env` (uncomment the line!)
3. ✅ Run newsletter generation
4. ✅ Find amazing Flux images in `outputs/images/`
5. 🎉 Enjoy photorealistic cover images!

---

**Questions?** See the full docs:
- [QUICK_FLUX_SETUP.md](QUICK_FLUX_SETUP.md) - Quick start guide
- [FLUX_AUTO_GENERATION.md](FLUX_AUTO_GENERATION.md) - Complete documentation

**Your current warning is NORMAL** - it's just telling you the token isn't set yet. Once you add it, Flux images will auto-generate! 🚀
