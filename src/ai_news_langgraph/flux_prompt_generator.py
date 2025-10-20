"""Flux Prompt Generator for Newsletter Cover Images.

Creates high-quality prompts for Flux AI image generation, inspired by CivitAI community standards.
Flux models produce photorealistic, detailed images perfect for professional newsletters.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class FluxPromptGenerator:
    """Generate optimized prompts for Flux AI image generation."""
    
    # CivitAI-inspired quality tags
    QUALITY_TAGS = [
        "masterpiece",
        "best quality",
        "ultra detailed",
        "8k resolution",
        "professional",
        "sharp focus",
        "high contrast",
        "vibrant colors"
    ]
    
    # Medical/Scientific specific tags
    MEDICAL_TAGS = [
        "medical illustration",
        "scientific visualization",
        "clinical setting",
        "healthcare technology",
        "medical research",
        "professional medical photography"
    ]
    
    # AI/Technology tags
    AI_TAGS = [
        "artificial intelligence",
        "neural networks",
        "futuristic technology",
        "digital interface",
        "data visualization",
        "holographic display",
        "tech innovation"
    ]
    
    # Negative prompts (what to avoid)
    NEGATIVE_PROMPTS = [
        "text",
        "words",
        "letters",
        "watermark",
        "signature",
        "blurry",
        "low quality",
        "distorted",
        "amateur",
        "cluttered"
    ]
    
    @staticmethod
    def generate_newsletter_cover_prompt(
        executive_summary: str,
        main_topic: str,
        topics: List[str],
        style: str = "professional"
    ) -> Dict[str, str]:
        """Generate optimized Flux prompts for newsletter covers.
        
        Args:
            executive_summary: Newsletter summary text
            main_topic: Main topic (e.g., "AI in Cancer Care")
            topics: List of sub-topics
            style: Visual style preference
            
        Returns:
            Dict with 'positive' and 'negative' prompts
        """
        # Extract key themes
        themes = FluxPromptGenerator._extract_themes(
            executive_summary, main_topic, topics
        )
        
        # Build positive prompt based on style
        positive = FluxPromptGenerator._build_positive_prompt(
            themes, style, main_topic
        )
        
        # Build negative prompt
        negative = ", ".join(FluxPromptGenerator.NEGATIVE_PROMPTS)
        
        return {
            "positive": positive,
            "negative": negative,
            "style": style,
            "themes": themes
        }
    
    @staticmethod
    def _extract_themes(
        summary: str,
        main_topic: str,
        topics: List[str]
    ) -> Dict[str, any]:
        """Extract visual themes from content."""
        summary_lower = summary.lower()
        
        themes = {
            "is_medical": any(word in summary_lower for word in [
                "cancer", "clinical", "patient", "treatment", "diagnosis",
                "oncology", "medical", "healthcare", "therapy"
            ]),
            "is_ai_focused": any(word in summary_lower for word in [
                "artificial intelligence", "machine learning", "ai", "neural",
                "algorithm", "model", "prediction", "automation"
            ]),
            "is_research": any(word in summary_lower for word in [
                "research", "study", "trial", "discovery", "breakthrough",
                "innovation", "development"
            ]),
            "is_data": any(word in summary_lower for word in [
                "data", "analysis", "statistics", "visualization", "insights",
                "metrics", "patterns"
            ]),
            "topics": topics[:3],  # Limit to top 3 for clarity
            "main_topic": main_topic
        }
        
        return themes
    
    @staticmethod
    def _build_positive_prompt(
        themes: Dict,
        style: str,
        main_topic: str
    ) -> str:
        """Build comprehensive positive prompt for Flux."""
        
        # Start with quality tags
        prompt_parts = [
            "masterpiece",
            "best quality",
            "ultra detailed",
            "8k uhd",
            "professional photography"
        ]
        
        # Style-specific prompts
        style_prompts = {
            "professional": FluxPromptGenerator._professional_style(themes),
            "modern": FluxPromptGenerator._modern_style(themes),
            "abstract": FluxPromptGenerator._abstract_style(themes),
            "scientific": FluxPromptGenerator._scientific_style(themes),
            "futuristic": FluxPromptGenerator._futuristic_style(themes),
            "cinematic": FluxPromptGenerator._cinematic_style(themes),
            "minimalist": FluxPromptGenerator._minimalist_style(themes)
        }
        
        # Add style-specific elements
        style_prompt = style_prompts.get(style, style_prompts["professional"])
        prompt_parts.extend(style_prompt)
        
        # Add theme-based elements
        if themes["is_medical"]:
            prompt_parts.extend([
                "medical technology",
                "healthcare innovation",
                "clean clinical environment"
            ])
        
        if themes["is_ai_focused"]:
            prompt_parts.extend([
                "artificial intelligence visualization",
                "neural network patterns",
                "futuristic technology interface"
            ])
        
        if themes["is_research"]:
            prompt_parts.extend([
                "scientific research environment",
                "laboratory setting",
                "innovative technology"
            ])
        
        if themes["is_data"]:
            prompt_parts.extend([
                "data visualization",
                "analytical displays",
                "information graphics"
            ])
        
        # Add color palette
        prompt_parts.extend([
            "color palette: deep blue, purple, cyan, white",
            "professional color grading",
            "high contrast lighting"
        ])
        
        # Composition and framing
        prompt_parts.extend([
            "16:9 aspect ratio",
            "centered composition",
            "balanced layout",
            "negative space",
            "professional framing"
        ])
        
        # Technical quality
        prompt_parts.extend([
            "sharp focus",
            "perfect lighting",
            "studio quality",
            "magazine cover style",
            "award winning composition"
        ])
        
        return ", ".join(prompt_parts)
    
    @staticmethod
    def _professional_style(themes: Dict) -> List[str]:
        """Professional corporate style prompt."""
        return [
            "professional corporate style",
            "clean and modern design",
            "medical illustration style",
            "sophisticated aesthetic",
            "business magazine cover",
            "elegant composition",
            "trustworthy and authoritative feel",
            "high-end medical journal aesthetic"
        ]
    
    @staticmethod
    def _modern_style(themes: Dict) -> List[str]:
        """Modern minimalist style prompt."""
        return [
            "modern minimalist design",
            "bold geometric shapes",
            "contemporary aesthetic",
            "clean lines",
            "vibrant gradient backgrounds",
            "tech startup style",
            "trendy and fresh look",
            "Instagram-worthy composition"
        ]
    
    @staticmethod
    def _abstract_style(themes: Dict) -> List[str]:
        """Abstract artistic style prompt."""
        return [
            "abstract artistic interpretation",
            "flowing organic shapes",
            "conceptual art style",
            "surreal elements",
            "creative composition",
            "artistic expression",
            "metaphorical visualization",
            "thought-provoking imagery"
        ]
    
    @staticmethod
    def _scientific_style(themes: Dict) -> List[str]:
        """Scientific technical style prompt."""
        return [
            "scientific visualization style",
            "technical illustration",
            "research paper aesthetic",
            "data-driven composition",
            "analytical presentation",
            "academic journal style",
            "precise and accurate representation",
            "evidence-based design"
        ]
    
    @staticmethod
    def _futuristic_style(themes: Dict) -> List[str]:
        """Futuristic high-tech style prompt."""
        return [
            "futuristic high-tech aesthetic",
            "sci-fi inspired design",
            "holographic interfaces",
            "neon accents",
            "cyberpunk influences",
            "advanced technology visualization",
            "next-generation innovation",
            "blade runner style lighting"
        ]
    
    @staticmethod
    def _cinematic_style(themes: Dict) -> List[str]:
        """Cinematic movie-poster style prompt."""
        return [
            "cinematic composition",
            "movie poster aesthetic",
            "dramatic lighting",
            "film grain effect",
            "epic scale",
            "Hollywood production quality",
            "theatrical presentation",
            "blockbuster visual style"
        ]
    
    @staticmethod
    def _minimalist_style(themes: Dict) -> List[str]:
        """Ultra-minimalist clean style prompt."""
        return [
            "ultra minimalist design",
            "white space emphasis",
            "simple clean composition",
            "less is more philosophy",
            "zen aesthetic",
            "uncluttered layout",
            "elegant simplicity",
            "refined and sophisticated"
        ]
    
    @staticmethod
    def create_civitai_prompt(
        main_concept: str,
        style_tags: List[str],
        quality_level: str = "high"
    ) -> Dict[str, str]:
        """Create CivitAI-community-style prompt.
        
        Args:
            main_concept: Core subject (e.g., "AI-powered cancer research")
            style_tags: Style descriptors
            quality_level: "high", "ultra", or "maximum"
            
        Returns:
            Prompt dictionary with positive and negative prompts
        """
        # Quality presets
        quality_presets = {
            "high": ["best quality", "high resolution", "detailed"],
            "ultra": ["masterpiece", "best quality", "ultra detailed", "8k uhd", "professional"],
            "maximum": ["masterpiece", "best quality", "ultra detailed", "8k uhd", "professional",
                       "award winning", "perfect composition", "studio lighting"]
        }
        
        quality_tags = quality_presets.get(quality_level, quality_presets["high"])
        
        # Combine all elements
        positive_parts = quality_tags + [main_concept] + style_tags
        
        positive = ", ".join(positive_parts)
        negative = ", ".join(FluxPromptGenerator.NEGATIVE_PROMPTS)
        
        return {
            "positive": positive,
            "negative": negative
        }
    
    @staticmethod
    def generate_sample_prompts() -> List[Dict[str, any]]:
        """Generate sample prompts for testing and examples."""
        samples = [
            {
                "name": "Professional Medical AI",
                "positive": "masterpiece, best quality, ultra detailed, 8k uhd, professional medical photography, "
                           "artificial intelligence in healthcare, modern hospital setting with holographic displays, "
                           "clean clinical environment, futuristic medical technology, neural network visualization, "
                           "color palette: deep blue, cyan, white, professional color grading, high contrast lighting, "
                           "16:9 aspect ratio, centered composition, sharp focus, magazine cover style",
                "negative": "text, words, letters, watermark, signature, blurry, low quality, distorted, cluttered"
            },
            {
                "name": "Futuristic Cancer Research",
                "positive": "masterpiece, best quality, ultra detailed, 8k resolution, futuristic laboratory, "
                           "cancer research visualization, holographic DNA strands, AI-powered microscope, "
                           "neon blue and purple lighting, high-tech medical equipment, floating data displays, "
                           "cinematic composition, dramatic lighting, sci-fi aesthetic, professional photography, "
                           "16:9 aspect ratio, award winning composition",
                "negative": "text, watermark, blurry, low quality, amateur, cluttered, distorted"
            },
            {
                "name": "Abstract Medical Innovation",
                "positive": "masterpiece, best quality, ultra detailed, abstract medical illustration, "
                           "flowing organic shapes representing cells, neural networks, digital art style, "
                           "vibrant blue and purple gradients, conceptual visualization of AI in medicine, "
                           "modern artistic interpretation, clean composition, professional design, "
                           "magazine quality, 16:9 aspect ratio, balanced layout",
                "negative": "text, words, watermark, blurry, low quality, cluttered, realistic faces"
            },
            {
                "name": "Minimalist Tech Medical",
                "positive": "masterpiece, best quality, minimalist design, clean medical technology visualization, "
                           "simple geometric shapes, AI brain icon, white background with blue accents, "
                           "professional corporate style, elegant simplicity, negative space, modern aesthetic, "
                           "high contrast, sharp lines, 16:9 aspect ratio, centered composition",
                "negative": "text, watermark, cluttered, busy, complex, low quality, blurry"
            },
            {
                "name": "Cinematic Scientific Discovery",
                "positive": "masterpiece, best quality, ultra detailed, 8k uhd, cinematic style, "
                           "dramatic scientific breakthrough scene, glowing particles, molecular structures, "
                           "epic scale, movie poster aesthetic, dramatic lighting, blue hour lighting, "
                           "depth of field, professional photography, theatrical presentation, "
                           "16:9 aspect ratio, Hollywood production quality",
                "negative": "text, watermark, blurry, low quality, amateur, overexposed, underexposed"
            }
        ]
        
        return samples


def generate_flux_prompt_for_newsletter(
    executive_summary: str,
    main_topic: str = "AI in Cancer Care",
    topics: List[str] = None,
    style: str = "professional"
) -> Dict[str, str]:
    """Convenience function to generate Flux prompts for newsletter covers.
    
    Args:
        executive_summary: Newsletter executive summary
        main_topic: Main newsletter topic
        topics: List of sub-topics
        style: Visual style (professional, modern, abstract, scientific, 
               futuristic, cinematic, minimalist)
        
    Returns:
        Dictionary with positive and negative prompts
    """
    generator = FluxPromptGenerator()
    
    prompts = generator.generate_newsletter_cover_prompt(
        executive_summary=executive_summary,
        main_topic=main_topic,
        topics=topics or [],
        style=style
    )
    
    logger.info(f"Generated Flux prompt for style: {style}")
    logger.info(f"Themes detected: {prompts.get('themes', {})}")
    
    return prompts


# Example usage
if __name__ == "__main__":
    # Example 1: Generate from newsletter content
    summary = """
    This week, we spotlight the groundbreaking integration of artificial intelligence
    in clinical trial design and patient matching, which is revolutionizing oncology
    research. AI's capacity to analyze vast datasets is enhancing the precision of
    participant selection, thereby accelerating the pace of clinical trials.
    """
    
    topics = ["Cancer Research", "Early Detection", "Treatment Planning"]
    
    print("=" * 80)
    print("FLUX PROMPT GENERATOR - Examples")
    print("=" * 80)
    print()
    
    # Generate prompts for different styles
    styles = ["professional", "futuristic", "cinematic"]
    
    for style in styles:
        print(f"\n{'='*80}")
        print(f"Style: {style.upper()}")
        print(f"{'='*80}")
        
        prompts = generate_flux_prompt_for_newsletter(
            executive_summary=summary,
            main_topic="AI in Cancer Care",
            topics=topics,
            style=style
        )
        
        print(f"\n📝 POSITIVE PROMPT:")
        print(prompts['positive'])
        
        print(f"\n🚫 NEGATIVE PROMPT:")
        print(prompts['negative'])
        
        print()
    
    # Example 2: Sample prompts
    print(f"\n{'='*80}")
    print("SAMPLE PROMPTS (Ready to use)")
    print(f"{'='*80}")
    
    samples = FluxPromptGenerator.generate_sample_prompts()
    
    for i, sample in enumerate(samples[:2], 1):  # Show first 2
        print(f"\n{i}. {sample['name']}")
        print(f"   Positive: {sample['positive'][:100]}...")
        print(f"   Negative: {sample['negative'][:80]}...")

