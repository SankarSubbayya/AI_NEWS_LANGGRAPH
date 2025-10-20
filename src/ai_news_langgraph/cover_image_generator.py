"""Cover Image Generator for AI News Newsletter.

Automatically creates contextually relevant cover images based on editorial content.
"""

import os
import base64
from typing import Optional, Dict, Any
from pathlib import Path
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CoverImageGenerator:
    """Generate cover images for newsletters using AI image generation."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the cover image generator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("No OpenAI API key provided. Cover image generation will be disabled.")
    
    def generate_cover_image(
        self,
        executive_summary: str,
        main_topic: str = "AI in Cancer Care",
        topics: list = None,
        output_dir: str = "outputs/images",
        style: str = "professional"
    ) -> Optional[str]:
        """Generate a cover image based on newsletter content.
        
        Args:
            executive_summary: The executive summary text
            main_topic: Main topic of the newsletter
            topics: List of topic names covered
            output_dir: Directory to save the generated image
            style: Image style (professional, modern, abstract, scientific)
            
        Returns:
            Path to the generated image, or None if generation failed
        """
        if not self.api_key:
            logger.warning("Skipping cover image generation: No API key")
            return None
        
        try:
            # Create the image prompt
            prompt = self._create_image_prompt(
                executive_summary=executive_summary,
                main_topic=main_topic,
                topics=topics or [],
                style=style
            )

            logger.info(f"Generating cover image with style: {style}")
            logger.info(f"Topics being visualized: {', '.join(topics[:5]) if topics else 'cancer research'}")
            logger.info(f"Number of topics received: {len(topics)}")
            if not topics:
                logger.warning("⚠️ No specific topics provided - using default cancer research theme")
            logger.debug(f"Full DALL-E prompt: {prompt[:300]}...")
            
            # Generate image using OpenAI DALL-E
            image_path = self._generate_with_dalle(
                prompt=prompt,
                output_dir=output_dir
            )
            
            if image_path:
                logger.info(f"Cover image generated successfully: {image_path}")
            
            return image_path
            
        except Exception as e:
            logger.error(f"Failed to generate cover image: {e}")
            return None
    
    def _create_image_prompt(
        self,
        executive_summary: str,
        main_topic: str,
        topics: list,
        style: str
    ) -> str:
        """Create a detailed prompt for image generation.

        Args:
            executive_summary: Newsletter summary text
            main_topic: Main topic
            topics: List of topics
            style: Desired image style

        Returns:
            Formatted prompt for image generation
        """
        # Extract key concepts from executive summary
        import re

        # Extract meaningful phrases and keywords
        keywords = []

        # Look for specific medical/tech terms in summary
        medical_terms = ['immunotherapy', 'genomics', 'imaging', 'diagnosis', 'treatment',
                        'biomarker', 'screening', 'precision', 'clinical trials', 'detection',
                        'deep learning', 'neural network', 'AI model', 'machine learning',
                        'prediction', 'accuracy', 'algorithm', 'data analysis']

        summary_lower = executive_summary.lower()
        found_terms = [term for term in medical_terms if term in summary_lower]

        # Build detailed topic string with all topics
        if topics and any(topics):  # Check if topics exist and are not empty strings
            # Filter out empty strings
            valid_topics = [t for t in topics if t and t.strip()]
            if valid_topics:
                topics_detail = ", ".join(valid_topics[:5])  # Use up to 5 topics for more detail
            else:
                # Default topics if none provided
                topics_detail = "Cancer Research, Early Detection, Treatment Planning, Clinical Trials, Prevention"
                logger.warning("Using default topics for cover image")
        else:
            # Default topics if none provided
            topics_detail = "Cancer Research, Early Detection, Treatment Planning, Clinical Trials, Prevention"
            logger.warning("No topics provided, using defaults")

        # Extract percentage/numbers if present (shows concrete results)
        numbers = re.findall(r'\d+%|\d+\.?\d*\s*(?:percent|accuracy|improvement)', executive_summary)
        results_mention = f" with {numbers[0]}" if numbers else ""

        # Get the main theme from first sentence of summary
        first_sentence = executive_summary.split('.')[0] if '.' in executive_summary else executive_summary[:150]

        # Style definitions with more specific medical/AI elements
        style_prompts = {
            "professional": "professional medical publication style, clean corporate design, medical journal aesthetic",
            "modern": "modern healthcare design, contemporary medical illustration, sleek and minimal",
            "abstract": "abstract medical visualization, artistic interpretation of cancer research data",
            "scientific": "scientific research visualization, technical medical illustration, data-driven imagery",
            "futuristic": "futuristic medical technology, cutting-edge healthcare AI, advanced digital medicine"
        }

        style_desc = style_prompts.get(style, style_prompts["professional"])

        # Build context-aware visual elements based on topics
        visual_elements = []
        # Use valid_topics if available, otherwise use executive summary keywords
        topics_to_check = valid_topics if 'valid_topics' in locals() and valid_topics else ['research', 'detection', 'treatment', 'prevention', 'trials']

        if any('detection' in t.lower() or 'diagnosis' in t.lower() for t in topics_to_check if t):
            visual_elements.append("medical imaging scans, diagnostic visualization")
        if any('treatment' in t.lower() or 'therapy' in t.lower() for t in topics_to_check if t):
            visual_elements.append("treatment planning, therapeutic approaches")
        if any('research' in t.lower() for t in topics_to_check if t):
            visual_elements.append("laboratory research, scientific discovery")
        if any('prevention' in t.lower() for t in topics_to_check if t):
            visual_elements.append("preventive healthcare, risk assessment")
        if any('trial' in t.lower() for t in topics_to_check if t):
            visual_elements.append("clinical trial data, patient outcomes")

        visual_desc = ", ".join(visual_elements[:3]) if visual_elements else "cancer research elements"

        # Create highly detailed, context-specific prompt
        prompt = f"""Professional cover image for an AI in Cancer Care newsletter.

Main Focus: {main_topic}{results_mention}

Specific Topics Covered:
{topics_detail}

Content Theme: {first_sentence}

Visual Style: {style_desc}

Key Visual Elements to Include:
- {visual_desc}
- AI/machine learning visualization (neural networks, data patterns, algorithms)
- Medical technology (microscopy, genomic sequences, diagnostic tools)
- Healthcare innovation (digital health, precision medicine)
{'- Highlighted concepts: ' + ', '.join(found_terms[:5]) if found_terms else ''}

Color Palette:
- Primary: Deep blues and teals (medical/tech)
- Secondary: Purple/violet (AI/innovation)
- Accents: White, light blue (clarity, precision)
- Avoid: Red, harsh colors

Technical Requirements:
- NO text, words, or letters in the image
- Professional medical journal quality
- High resolution, sharp focus
- Balanced composition, not cluttered
- Landscape orientation (16:9)
- Suitable for newsletter header
- Photorealistic yet abstract enough to be universally representative

Mood: Innovative, hopeful, scientific, trustworthy, cutting-edge"""

        return prompt
    
    def _generate_with_dalle(
        self,
        prompt: str,
        output_dir: str,
        model: str = "dall-e-3"
    ) -> Optional[str]:
        """Generate image using OpenAI DALL-E API.
        
        Args:
            prompt: Image generation prompt
            output_dir: Output directory for saving image
            model: DALL-E model to use (dall-e-2 or dall-e-3)
            
        Returns:
            Path to saved image or None
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.api_key)
            
            # Generate image
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size="1792x1024",  # 16:9 ratio for dall-e-3
                quality="standard",  # or "hd" for higher quality
                n=1
            )
            
            # Get image URL
            image_url = response.data[0].url
            
            # Download and save image
            import requests
            image_response = requests.get(image_url)
            
            if image_response.status_code == 200:
                # Create output directory
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                
                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"cover_image_{timestamp}.png"
                filepath = os.path.join(output_dir, filename)
                
                # Save image
                with open(filepath, 'wb') as f:
                    f.write(image_response.content)
                
                logger.info(f"Image saved to: {filepath}")
                return filepath
            else:
                logger.error(f"Failed to download image: {image_response.status_code}")
                return None
                
        except ImportError:
            logger.error("OpenAI package not installed. Run: pip install openai")
            return None
        except Exception as e:
            logger.error(f"DALL-E generation failed: {e}")
            return None
    
    def generate_fallback_image(
        self,
        main_topic: str,
        output_dir: str = "outputs/images"
    ) -> Optional[str]:
        """Generate a simple fallback cover image using Pillow.
        
        Args:
            main_topic: Main topic for the cover
            output_dir: Output directory
            
        Returns:
            Path to generated image or None
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            width, height = 1792, 1024
            img = Image.new('RGB', (width, height), color='#667eea')
            draw = ImageDraw.Draw(img)
            
            # Add gradient effect
            for i in range(height):
                alpha = i / height
                r = int(102 + (118 - 102) * alpha)
                g = int(126 + (75 - 126) * alpha)
                b = int(234 + (162 - 234) * alpha)
                draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
            
            # Add text
            try:
                font_large = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 120)
                font_small = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 60)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Draw title
            title_text = main_topic
            title_bbox = draw.textbbox((0, 0), title_text, font=font_large)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, height // 2 - 100), title_text, fill='white', font=font_large)
            
            # Draw subtitle
            subtitle = "AI-Powered Research Newsletter"
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            draw.text((subtitle_x, height // 2 + 50), subtitle, fill='white', font=font_small)
            
            # Save image
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cover_fallback_{timestamp}.png"
            filepath = os.path.join(output_dir, filename)
            
            img.save(filepath)
            logger.info(f"Fallback cover image created: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to create fallback image: {e}")
            return None
    
    def embed_image_in_html(self, image_path: str) -> str:
        """Convert image to base64 for HTML embedding.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Base64 encoded image string
        """
        try:
            with open(image_path, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode()
                return f"data:image/png;base64,{img_data}"
        except Exception as e:
            logger.error(f"Failed to embed image: {e}")
            return ""


def generate_newsletter_cover(
    executive_summary: str,
    main_topic: str = "AI in Cancer Care",
    topics: list = None,
    style: str = "professional",
    use_fallback: bool = False
) -> Optional[str]:
    """Convenience function to generate a newsletter cover image.
    
    Args:
        executive_summary: Newsletter executive summary
        main_topic: Main topic of newsletter
        topics: List of topics covered
        style: Image style (professional, modern, abstract, scientific, futuristic)
        use_fallback: If True, use simple fallback instead of AI generation
        
    Returns:
        Path to generated image or None
    """
    generator = CoverImageGenerator()
    
    if use_fallback:
        return generator.generate_fallback_image(main_topic)
    
    image_path = generator.generate_cover_image(
        executive_summary=executive_summary,
        main_topic=main_topic,
        topics=topics,
        style=style
    )
    
    # If AI generation fails, use fallback
    if not image_path:
        logger.warning("AI generation failed, using fallback image")
        image_path = generator.generate_fallback_image(main_topic)
    
    return image_path


# Example usage
if __name__ == "__main__":
    # Test the cover image generator
    sample_summary = """
    This week, we spotlight the groundbreaking integration of artificial intelligence 
    in clinical trial design and patient matching, which is revolutionizing oncology research.
    """
    
    sample_topics = [
        "Cancer Research",
        "Early Detection", 
        "Treatment Planning"
    ]
    
    image_path = generate_newsletter_cover(
        executive_summary=sample_summary,
        main_topic="AI in Cancer Care",
        topics=sample_topics,
        style="professional"
    )
    
    if image_path:
        print(f"✅ Cover image generated: {image_path}")
    else:
        print("❌ Failed to generate cover image")


