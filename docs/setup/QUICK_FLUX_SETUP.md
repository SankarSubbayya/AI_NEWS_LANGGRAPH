# Quick Flux Setup Guide (2 Minutes)

## TL;DR - Get Flux Images Auto-Generating

### 1. Get Token (30 seconds)
Go to: https://replicate.com/account/api-tokens
→ Sign up → Create token → Copy it

### 2. Add to .env (15 seconds)
```bash
REPLICATE_API_TOKEN=r8_paste_your_token_here
```

### 3. Install (30 seconds)
```bash
pip install replicate
```

### 4. Run (Done!)
```bash
python -m ai_news_langgraph.main
```

That's it! Flux images will auto-generate in `outputs/images/flux_cover_*.png`

---

## What You Get

✅ **DALL-E images** (artistic, 5-10 sec)
✅ **Flux images** (photorealistic, 10-30 sec) ⭐ **NEW!**
✅ **Flux prompts** (backup for manual use)

## Where to Find Images

```
outputs/
├── images/
│   ├── cover_*.png          ← DALL-E
│   └── flux_cover_*.png     ← Flux ⭐
└── flux_prompts/
    └── flux_prompts_*.txt   ← Backup
```

## Cost

- **DALL-E**: $0.04 per image
- **Flux Schnell**: $0.003 per image (10x cheaper!) ✅
- **Both**: $0.043 per newsletter

## Without Token?

No problem! System falls back to:
- ✅ DALL-E images still generate
- ✅ Flux prompts saved for manual use
- ℹ️ Helpful message shown

## Full Documentation

- [FLUX_AUTO_GENERATION.md](FLUX_AUTO_GENERATION.md) - Complete guide
- [FLUX_AUTO_IMPLEMENTATION_SUMMARY.md](FLUX_AUTO_IMPLEMENTATION_SUMMARY.md) - Technical details

---

**Questions?** See the full documentation above or check the [README.md](README.md)
