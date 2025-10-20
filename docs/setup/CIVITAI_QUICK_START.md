# 🚀 CivitAI Quick Start Guide

**Create stunning newsletter covers in 5 minutes using Flux AI!**

---

## 📋 Prerequisites

- ✅ Python environment setup
- ✅ This repository cloned
- ✅ CivitAI account (free): https://civitai.com/

---

## 🎯 Quick Start (5 Steps)

### Step 1: Generate Flux Prompt (30 seconds)

```bash
# Activate your environment
cd /path/to/AI_NEWS_LANGGRAPH
source .venv/bin/activate

# Run the prompt generator
python examples/generate_flux_prompts.py
```

**OR use Python directly**:

```python
from ai_news_langgraph.flux_prompt_generator import generate_flux_prompt_for_newsletter

prompts = generate_flux_prompt_for_newsletter(
    executive_summary="AI revolutionizes cancer treatment with breakthrough...",
    main_topic="AI in Cancer Care",
    topics=["Cancer Research", "Early Detection", "Treatment Planning"],
    style="professional"  # Choose: professional, modern, abstract, scientific, 
                          #         futuristic, cinematic, minimalist
)

print("📝 POSITIVE PROMPT:")
print(prompts['positive'])
print("\n🚫 NEGATIVE PROMPT:")
print(prompts['negative'])
```

---

### Step 2: Copy the Prompts (5 seconds)

Copy both:
1. ✅ **Positive Prompt** - The main generation prompt
2. ✅ **Negative Prompt** - What to avoid

---

### Step 3: Go to CivitAI (10 seconds)

1. Open https://civitai.com/
2. Sign in (or create free account)
3. Click **"Create"** at the top
4. Select **Image Generation**

---

### Step 4: Configure Settings (30 seconds)

#### Model Selection
- **Flux.1 Dev** (FREE, recommended for testing)
- **Flux.1 Pro** (Paid, best quality)

#### Settings
```
Positive Prompt: [Paste your generated prompt]
Negative Prompt: [Paste your negative prompt]

Aspect Ratio: 16:9 (1792×1024)  ← IMPORTANT for newsletter covers
Steps: 25
CFG Scale: 7.5
Sampler: DPM++ 2M Karras
```

#### Click "Generate" 🎨

---

### Step 5: Download & Use (30 seconds)

1. Wait 10-30 seconds for generation
2. View your stunning cover image!
3. Click **Download**
4. Save to `outputs/images/`
5. Use in your newsletter HTML

---

## 🎨 Style Showcase

### Professional
**Best for**: Corporate newsletters, formal medical content
```python
style="professional"
```
**Result**: Clean medical illustration, trustworthy, high-end journal quality

---

### Modern
**Best for**: Tech-focused, contemporary content
```python
style="modern"
```
**Result**: Bold geometric shapes, vibrant gradients, Instagram-worthy

---

### Futuristic
**Best for**: Innovation, cutting-edge technology
```python
style="futuristic"
```
**Result**: High-tech aesthetic, holographic interfaces, neon accents, sci-fi

---

### Cinematic
**Best for**: Dramatic, eye-catching covers
```python
style="cinematic"
```
**Result**: Movie poster style, dramatic lighting, epic scale

---

### Scientific
**Best for**: Research-focused, academic content
```python
style="scientific"
```
**Result**: Technical illustrations, data-driven, academic journal style

---

### Abstract
**Best for**: Creative, artistic newsletters
```python
style="abstract"
```
**Result**: Flowing organic shapes, conceptual, thought-provoking

---

### Minimalist
**Best for**: Clean, elegant, simple designs
```python
style="minimalist"
```
**Result**: Ultra-minimal, white space, zen aesthetic, elegant

---

## 💡 Pro Tips

### Tip 1: Start with Professional
For your first attempt, use `style="professional"` - it's the most reliable for medical/scientific content.

### Tip 2: Use the Exact Prompt First
Don't modify the generated prompt on your first try. See what it produces, then refine if needed.

### Tip 3: Try Multiple Styles
Generate prompts for 2-3 different styles and create all of them on CivitAI to see which you prefer.

### Tip 4: Save Your Favorites
When you find a prompt/style combination you love, save it! You can reuse similar prompts.

### Tip 5: Experiment with Steps
- **Steps 15-20**: Faster, good for testing
- **Steps 25-30**: Best quality (recommended)
- **Steps 30+**: Diminishing returns, slower

---

## 🎯 Complete Example

### Input Newsletter Content

```python
executive_summary = """
This week, we spotlight the groundbreaking integration of artificial intelligence
in clinical trial design and patient matching, which is revolutionizing oncology
research. AI's capacity to analyze vast datasets is enhancing the precision of
participant selection, thereby accelerating the pace of clinical trials.
"""

topics = [
    "Cancer Research",
    "Early Detection",
    "Treatment Planning"
]
```

### Generate Prompt

```python
from ai_news_langgraph.flux_prompt_generator import generate_flux_prompt_for_newsletter

prompts = generate_flux_prompt_for_newsletter(
    executive_summary=executive_summary,
    main_topic="AI in Cancer Care",
    topics=topics,
    style="professional"
)
```

### Example Output

**POSITIVE PROMPT**:
```
masterpiece, best quality, ultra detailed, 8k uhd, professional photography,
professional corporate style, clean and modern design, medical illustration style,
sophisticated aesthetic, business magazine cover, elegant composition,
trustworthy and authoritative feel, high-end medical journal aesthetic,
medical technology, healthcare innovation, clean clinical environment,
artificial intelligence visualization, neural network patterns,
futuristic technology interface, scientific research environment,
laboratory setting, innovative technology, data visualization,
color palette: deep blue, purple, cyan, white, professional color grading,
high contrast lighting, 16:9 aspect ratio, centered composition,
balanced layout, sharp focus, perfect lighting, studio quality,
magazine cover style, award winning composition
```

**NEGATIVE PROMPT**:
```
text, words, letters, watermark, signature, blurry, low quality,
distorted, amateur, cluttered
```

### CivitAI Settings

```
Model: Flux.1 Dev
Positive Prompt: [Paste above]
Negative Prompt: [Paste above]
Aspect Ratio: 16:9
Steps: 25
CFG Scale: 7.5
Sampler: DPM++ 2M Karras
```

### Click Generate! 🎨

**Result**: Stunning professional newsletter cover with medical AI theme

---

## 🆘 Troubleshooting

### Problem: Image has text/words
**Solution**: Make sure you included the negative prompt with `text, words, letters`

### Problem: Wrong aspect ratio
**Solution**: Set aspect ratio to **16:9** (1792×1024) in CivitAI settings

### Problem: Image doesn't match style
**Solution**: 
1. Try regenerating (same prompt, different seed)
2. Or add 1-2 more style-specific words to the prompt
3. Increase CFG scale to 8-9 for stronger prompt adherence

### Problem: Colors are off
**Solution**: Our prompts include `color palette: deep blue, purple, cyan, white` - this should work, but you can make it more specific:
```
color palette: navy blue (#001f3f), purple (#9b59b6), cyan (#00bcd4), white (#ffffff)
```

### Problem: Too abstract/not enough content
**Solution**: Try `style="professional"` or `style="scientific"` for more concrete imagery

### Problem: Too literal/not creative enough
**Solution**: Try `style="abstract"` or `style="futuristic"` for more creative interpretation

---

## 📊 Expected Results

### Quality
- **Resolution**: 1792×1024 pixels (perfect for 16:9 newsletter headers)
- **Quality**: Professional, publication-ready
- **Style**: Matches your selected style
- **Colors**: Blue, purple, cyan, white palette (medical/tech appropriate)

### Generation Time
- **Flux.1 Dev**: 10-20 seconds
- **Flux.1 Pro**: 10-15 seconds

### Cost
- **Flux.1 Dev**: FREE (with limits) or ~$0.03-0.05/image
- **Flux.1 Pro**: ~$0.05-0.08/image

---

## 🎓 Next Steps

### 1. Practice
Generate 3-5 covers with different styles to see what works best for your newsletter.

### 2. Build a Library
Save your favorite prompts and generated images for future reference.

### 3. Integrate
Use the generated covers in your newsletters with `html_generator.py`.

### 4. Share
Share your best covers with the CivitAI community! (optional)

---

## 📚 Additional Resources

### Documentation
- **Full Guide**: [FLUX_PROMPTS_GUIDE.md](FLUX_PROMPTS_GUIDE.md)
- **Summary**: [../FLUX_IMPLEMENTATION_SUMMARY.md](../FLUX_IMPLEMENTATION_SUMMARY.md)
- **Examples**: `examples/generate_flux_prompts.py`

### CivitAI
- **Website**: https://civitai.com/
- **Flux Models**: Search "Flux" on CivitAI
- **Gallery**: Browse community creations for inspiration

### Prompt Engineering
- Study high-rated images on CivitAI
- Note what prompts work well
- Experiment and iterate

---

## ✅ Checklist

Before you start:
- [ ] Python environment activated
- [ ] CivitAI account created (free)
- [ ] Newsletter content ready
- [ ] Chosen a style

During generation:
- [ ] Generated prompt with correct style
- [ ] Copied positive AND negative prompts
- [ ] Set aspect ratio to 16:9
- [ ] Set steps to 25
- [ ] Set CFG scale to 7.5

After generation:
- [ ] Downloaded image
- [ ] Saved to outputs/images/
- [ ] Used in newsletter
- [ ] Enjoyed your beautiful cover! 🎉

---

## 🎉 You're Ready!

Follow these 5 steps and you'll have a stunning newsletter cover in **under 5 minutes**!

1. ✅ Generate Prompt (30 sec)
2. ✅ Copy Prompts (5 sec)
3. ✅ Go to CivitAI (10 sec)
4. ✅ Configure & Generate (30 sec)
5. ✅ Download & Use (30 sec)

**Total: ~2 minutes + generation time (10-30 sec)**

---

**Questions?** See [FLUX_PROMPTS_GUIDE.md](FLUX_PROMPTS_GUIDE.md) for comprehensive documentation!

**Happy creating! 🎨**

