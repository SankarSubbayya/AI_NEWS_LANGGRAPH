# Cover Image Generator

**Purpose**: Automatically create contextually relevant cover images based on editorial or article text.  
**Status**: ✅ Implemented  
**Date**: October 13, 2025

## 📖 Overview

The Cover Image Generator is a new AI-powered tool that creates professional, contextually relevant cover images for your AI News newsletters. It analyzes the newsletter content and generates beautiful visual headers that enhance the presentation and engagement.

## ✨ Features

### 1. **AI-Powered Generation**
- Uses OpenAI DALL-E 3 for high-quality image generation
- Analyzes executive summary and topics
- Creates contextually relevant visuals
- Professional medical/scientific aesthetic

### 2. **Multiple Style Options**
- **Professional**: Clean, corporate medical illustration
- **Modern**: Minimalist design with bold colors
- **Abstract**: Artistic interpretation with flowing shapes
- **Scientific**: Technical data-driven visualization
- **Futuristic**: High-tech digital art aesthetic

### 3. **Fallback System**
- Simple gradient-based cover if AI generation fails
- No external API dependency for fallback
- Always provides a cover image

### 4. **HTML Integration**
- Base64 encoding for embedded images
- No external file dependencies
- Responsive design
- Clean integration with existing newsletter

## 🚀 Usage

### Basic Usage

```python
from ai_news_langgraph.cover_image_generator import generate_newsletter_cover

# Generate a cover image
image_path = generate_newsletter_cover(
    executive_summary="This week, we spotlight the groundbreaking integration...",
    main_topic="AI in Cancer Care",
    topics=["Cancer Research", "Early Detection", "Treatment Planning"],
    style="professional"
)

print(f"Cover image generated: {image_path}")
# Output: Cover image generated: outputs/images/cover_image_20251013_120000.png
```

### Advanced Usage

```python
from ai_news_langgraph.cover_image_generator import CoverImageGenerator

# Initialize generator
generator = CoverImageGenerator(api_key="your-openai-key")

# Generate with custom settings
image_path = generator.generate_cover_image(
    executive_summary=executive_summary,
    main_topic="AI in Oncology",
    topics=topics_list,
    output_dir="custom/output/path",
    style="futuristic"
)

# Embed in HTML
if image_path:
    base64_image = generator.embed_image_in_html(image_path)
    # Use in newsletter HTML
```

### Integration with Newsletter Generation

```python
from ai_news_langgraph.html_generator import HTMLNewsletterGenerator
from ai_news_langgraph.cover_image_generator import generate_newsletter_cover

# Generate cover image
cover_path = generate_newsletter_cover(
    executive_summary=exec_summary,
    main_topic="AI in Cancer Care",
    topics=topic_names,
    style="professional"
)

# Convert to base64 for HTML
if cover_path:
    with open(cover_path, 'rb') as f:
        import base64
        cover_base64 = base64.b64encode(f.read()).decode()
        cover_image = f"data:image/png;base64,{cover_base64}"
else:
    cover_image = None

# Generate newsletter with cover
html = HTMLNewsletterGenerator.generate_newsletter_html(
    executive_summary=exec_summary,
    topic_summaries=topic_summaries,
    main_topic="AI in Cancer Care",
    metrics=metrics,
    chart_images=chart_paths,
    cover_image=cover_image  # 🆕 New parameter
)
```

## 🎨 Style Options

### 1. Professional (Default)
- Clean medical illustration style
- Corporate aesthetic
- Suitable for formal newsletters
- Colors: Blues, purples, white

```python
generate_newsletter_cover(..., style="professional")
```

### 2. Modern
- Minimalist design
- Bold geometric shapes
- Contemporary look
- Eye-catching colors

```python
generate_newsletter_cover(..., style="modern")
```

### 3. Abstract
- Artistic interpretation
- Flowing organic shapes
- Creative and unique
- Visually striking

```python
generate_newsletter_cover(..., style="abstract")
```

### 4. Scientific
- Technical visualization style
- Data-driven appearance
- Analytical aesthetic
- Research-focused

```python
generate_newsletter_cover(..., style="scientific")
```

### 5. Futuristic
- High-tech digital art
- Advanced technology feel
- Innovation-focused
- Bold and modern

```python
generate_newsletter_cover(..., style="futuristic")
```

## 🔧 Configuration

### Environment Variables

```bash
# Required for AI generation
export OPENAI_API_KEY="sk-your-openai-api-key"

# Optional: Customize output directory
export COVER_IMAGE_OUTPUT_DIR="outputs/images"
```

### API Key Setup

1. **Get OpenAI API Key**:
   - Go to: https://platform.openai.com/api-keys
   - Create new API key
   - Copy the key

2. **Set in Environment**:
   ```bash
   # In .env file
   OPENAI_API_KEY=sk-your-key-here
   
   # Or in shell
   export OPENAI_API_KEY="sk-your-key-here"
   ```

3. **Programmatic Setup**:
   ```python
   generator = CoverImageGenerator(api_key="sk-your-key-here")
   ```

## 📊 Technical Details

### Image Specifications

- **Size**: 1792x1024 pixels (16:9 aspect ratio)
- **Format**: PNG
- **Quality**: Standard (or HD for premium)
- **Model**: DALL-E 3
- **Generation Time**: 10-30 seconds

### Prompt Engineering

The system creates detailed prompts that include:
- Main topic and sub-topics
- Key themes from executive summary
- Style specifications
- Technical requirements (no text, color palette, etc.)
- Quality constraints

**Example Prompt**:
```
Create a compelling cover image for a newsletter about AI in Cancer Care.

The newsletter focuses on: Cancer Research, Early Detection, Treatment Planning.

Key theme: This week, we spotlight the groundbreaking integration of artificial 
intelligence in clinical trial design...

Style: professional medical illustration, clean design, corporate style

Requirements:
- Professional and suitable for a medical/scientific newsletter
- Include abstract representations of AI technology and healthcare
- Use a color palette of blues, purples, and white
- No text or words in the image
- High quality, suitable for newsletter header
- Aspect ratio 16:9 (landscape)
- Clean, uncluttered composition
```

### Fallback Image

If AI generation fails (no API key, quota exceeded, error), a simple gradient-based cover is created using Pillow:

- Gradient background (purple to blue)
- Newsletter title text
- Subtitle ("AI-Powered Research Newsletter")
- Clean, professional appearance

## 💰 Cost Considerations

### DALL-E 3 Pricing (as of 2025)

- **Standard Quality (1024×1792)**: $0.080 per image
- **HD Quality**: $0.120 per image

### Cost Optimization

1. **Use Standard Quality**: Perfectly suitable for newsletters
2. **Enable Fallback**: Only generate AI images when needed
3. **Cache Images**: Reuse covers for similar topics
4. **Batch Generation**: Generate weekly, not daily

**Example Costs**:
- 1 newsletter/week: ~$0.32/month
- 4 newsletters/week: ~$1.28/month
- Daily newsletters: ~$2.40/month

## 🎯 Best Practices

### 1. Content Quality
- Provide detailed executive summaries
- Include specific topic names
- Use descriptive main topics
- Better content → Better images

### 2. Style Selection
- Match your brand identity
- Consider your audience
- Professional for corporate
- Modern/Futuristic for tech-focused

### 3. Testing
- Test with fallback first
- Verify API key works
- Check image quality
- Review generation time

### 4. Error Handling
```python
try:
    image_path = generate_newsletter_cover(...)
    if not image_path:
        logger.warning("Using fallback image")
        # Fallback is automatic
except Exception as e:
    logger.error(f"Cover generation failed: {e}")
    # Proceed without cover
```

## 📁 File Structure

```
outputs/
└── images/
    ├── cover_image_20251013_120000.png      # AI-generated
    ├── cover_image_20251013_140000.png      # AI-generated
    └── cover_fallback_20251013_150000.png   # Fallback
```

## 🔍 Troubleshooting

### Issue 1: No API Key Error

**Error**: `WARNING: No OpenAI API key provided`

**Solution**:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### Issue 2: Generation Failed

**Error**: `Failed to generate cover image`

**Possible Causes**:
- API quota exceeded
- Network issues
- Invalid API key
- Rate limiting

**Solution**:
- Check API key validity
- Verify internet connection
- Check OpenAI status page
- Use fallback image

### Issue 3: Image Not Appearing in Newsletter

**Check**:
1. Verify image was generated
2. Check base64 encoding
3. Verify HTML parameter passed
4. Check browser console for errors

**Debug**:
```python
if cover_path:
    print(f"Image exists: {os.path.exists(cover_path)}")
    print(f"Image size: {os.path.getsize(cover_path)} bytes")
```

### Issue 4: Slow Generation

**Expected**: 10-30 seconds for DALL-E 3

**Optimization**:
- Use standard quality (faster)
- Cache generated images
- Generate during off-peak hours
- Use fallback for testing

## 📈 Performance Metrics

### Generation Times (Typical)

- **AI Generation**: 10-30 seconds
- **Fallback Generation**: < 1 second
- **Base64 Encoding**: < 1 second
- **HTML Embedding**: Negligible

### Image Sizes

- **AI Generated**: 200-500 KB
- **Fallback**: 50-100 KB
- **Base64 Encoded**: +33% size (in HTML)

## 🔄 Integration with Workflow

Add to `nodes_v2.py` in the `generate_newsletter` function:

```python
async def generate_newsletter(self, state: dict) -> dict:
    # ... existing code ...
    
    # Generate cover image
    try:
        from .cover_image_generator import generate_newsletter_cover
        
        logger.info("Generating cover image...")
        topic_names = [s.get('topic_name') for s in topic_summaries]
        
        cover_path = generate_newsletter_cover(
            executive_summary=exec_summary,
            main_topic=state.get("main_topic", "AI in Cancer Care"),
            topics=topic_names,
            style="professional"
        )
        
        # Convert to base64
        if cover_path:
            with open(cover_path, 'rb') as f:
                cover_base64 = base64.b64encode(f.read()).decode()
                cover_image = f"data:image/png;base64,{cover_base64}"
        else:
            cover_image = None
            
    except Exception as e:
        logger.error(f"Cover image generation failed: {e}")
        cover_image = None
    
    # Generate HTML with cover
    html_content = HTMLNewsletterGenerator.generate_newsletter_html(
        executive_summary=exec_summary,
        topic_summaries=topic_summaries,
        main_topic=state.get("main_topic", "AI in Cancer Care"),
        metrics=metrics,
        chart_images=chart_paths,
        cover_image=cover_image  # Pass cover image
    )
    
    # ... rest of code ...
```

## 📚 Examples

### Example 1: Basic Newsletter Cover

```python
image_path = generate_newsletter_cover(
    executive_summary="AI transforms cancer research...",
    main_topic="AI in Cancer Care",
    topics=["Research", "Detection", "Treatment"]
)
```

**Result**: Professional medical illustration with AI and cancer care themes

### Example 2: Modern Style

```python
image_path = generate_newsletter_cover(
    executive_summary="Breakthrough in genomics...",
    main_topic="Precision Oncology",
    topics=["Genomics", "Immunotherapy"],
    style="modern"
)
```

**Result**: Bold, minimalist design with contemporary aesthetic

### Example 3: Using Fallback

```python
image_path = generate_newsletter_cover(
    executive_summary="Weekly roundup...",
    main_topic="Cancer Research News",
    topics=[],
    use_fallback=True
)
```

**Result**: Simple gradient cover with text

## 🎓 Learning Resources

- [DALL-E 3 Documentation](https://platform.openai.com/docs/guides/images)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/images)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [HTML Image Embedding](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)

## 🆕 Future Enhancements

Planned features:
- [ ] Multiple cover variants per newsletter
- [ ] A/B testing for cover effectiveness
- [ ] Custom color palette configuration
- [ ] Logo overlay option
- [ ] Text overlay with headline
- [ ] Template-based generation
- [ ] Support for other AI models (Stability AI, Midjourney)
- [ ] Cover image library/gallery
- [ ] Seasonal/themed variations

## 📝 Related Documentation

- [HTML_GENERATOR.md](HTML_GENERATOR.md) - HTML newsletter generation
- [CHARTS_FIX.md](CHARTS_FIX.md) - Chart visualization
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture

---

**Status**: ✅ Ready to use  
**Dependencies**: `openai`, `requests`, `Pillow`  
**Cost**: ~$0.08 per cover image (DALL-E 3)  
**Generation Time**: 10-30 seconds


