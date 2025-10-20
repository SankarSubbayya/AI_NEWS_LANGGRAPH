"""Flux Image Generator using Replicate API.

Generates actual Flux images using Black Forest Labs' Flux model via Replicate.
This module creates high-quality, photorealistic images for newsletter covers.
"""

import os
import logging
import requests
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class FluxImageGenerator:
    """Generate actual Flux images using Replicate API."""

    def __init__(self, api_token: Optional[str] = None):
        """Initialize Flux image generator.

        Args:
            api_token: Replicate API token (defaults to REPLICATE_API_TOKEN env var)
        """
        self.api_token = api_token or os.getenv("REPLICATE_API_TOKEN")

        if not self.api_token:
            logger.warning(
                "REPLICATE_API_TOKEN not found. Flux image generation will be skipped. "
                "Get your token at https://replicate.com/account/api-tokens"
            )
            self.enabled = False
        else:
            self.enabled = True
            logger.info("✅ Flux image generator initialized with Replicate API")

    def generate_cover_image(
        self,
        executive_summary: str,
        main_topic: str,
        topics: List[str],
        style: str = "professional",
        output_dir: str = "outputs/images"
    ) -> Optional[str]:
        """Generate Flux cover image using Replicate API.

        Args:
            executive_summary: Newsletter summary text
            main_topic: Main topic (e.g., "AI in Cancer Care")
            topics: List of sub-topics
            style: Visual style preference
            output_dir: Directory to save generated images

        Returns:
            Path to generated image file, or None if generation failed
        """
        if not self.enabled:
            logger.warning("Flux image generation disabled (missing API token)")
            return None

        try:
            # Import here to avoid dependency issues if replicate not installed
            import replicate

            # Generate optimized prompt using FluxPromptGenerator
            from .flux_prompt_generator import FluxPromptGenerator

            prompt_data = FluxPromptGenerator.generate_newsletter_cover_prompt(
                executive_summary=executive_summary,
                main_topic=main_topic,
                topics=topics,
                style=style
            )

            positive_prompt = prompt_data["positive"]

            logger.info("🎨 Generating Flux image via Replicate API...")
            logger.info(f"📝 Prompt: {positive_prompt[:100]}...")

            # Use Flux Schnell (fastest) or Flux Dev (higher quality)
            # Flux Schnell is faster and cheaper, Flux Dev is higher quality
            model = "black-forest-labs/flux-schnell"  # Change to flux-dev for better quality

            # Generate image using Replicate
            output = replicate.run(
                model,
                input={
                    "prompt": positive_prompt,
                    "num_outputs": 1,
                    "aspect_ratio": "16:9",  # Landscape for newsletter cover
                    "output_format": "png",
                    "output_quality": 90,
                }
            )

            # Download the generated image
            if output and len(output) > 0:
                image_url = output[0]

                # Create output directory
                os.makedirs(output_dir, exist_ok=True)

                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"flux_cover_{timestamp}.png"
                filepath = os.path.join(output_dir, filename)

                # Download image
                logger.info(f"⬇️  Downloading Flux image from {image_url}...")
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()

                with open(filepath, "wb") as f:
                    f.write(response.content)

                logger.info(f"✅ Flux image saved: {filepath}")
                return filepath
            else:
                logger.error("❌ Replicate returned no image output")
                return None

        except ImportError:
            logger.error(
                "❌ Replicate library not installed. Run: pip install replicate"
            )
            return None
        except Exception as e:
            logger.error(f"❌ Failed to generate Flux image: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

    def generate_with_custom_prompt(
        self,
        positive_prompt: str,
        negative_prompt: Optional[str] = None,
        output_dir: str = "outputs/images",
        aspect_ratio: str = "16:9",
        model: str = "black-forest-labs/flux-schnell"
    ) -> Optional[str]:
        """Generate Flux image with custom prompts.

        Args:
            positive_prompt: The main prompt describing what to generate
            negative_prompt: What to avoid (not used by Flux models currently)
            output_dir: Directory to save generated images
            aspect_ratio: Image aspect ratio (1:1, 16:9, 21:9, 2:3, 3:2, 4:5, 5:4, 9:16, 9:21)
            model: Replicate model to use (flux-schnell or flux-dev)

        Returns:
            Path to generated image file, or None if generation failed
        """
        if not self.enabled:
            logger.warning("Flux image generation disabled (missing API token)")
            return None

        try:
            import replicate

            logger.info(f"🎨 Generating Flux image with custom prompt via {model}...")

            # Generate image
            output = replicate.run(
                model,
                input={
                    "prompt": positive_prompt,
                    "num_outputs": 1,
                    "aspect_ratio": aspect_ratio,
                    "output_format": "png",
                    "output_quality": 90,
                }
            )

            # Download the generated image
            if output and len(output) > 0:
                image_url = output[0]

                # Create output directory
                os.makedirs(output_dir, exist_ok=True)

                # Generate filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"flux_custom_{timestamp}.png"
                filepath = os.path.join(output_dir, filename)

                # Download image
                response = requests.get(image_url, timeout=30)
                response.raise_for_status()

                with open(filepath, "wb") as f:
                    f.write(response.content)

                logger.info(f"✅ Flux image saved: {filepath}")
                return filepath
            else:
                logger.error("❌ Replicate returned no image output")
                return None

        except Exception as e:
            logger.error(f"❌ Failed to generate Flux image: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


def test_flux_generation():
    """Test Flux image generation."""
    generator = FluxImageGenerator()

    if not generator.enabled:
        print("❌ Flux generation not enabled (missing REPLICATE_API_TOKEN)")
        print("Get your token at: https://replicate.com/account/api-tokens")
        print("Then set it in your .env file: REPLICATE_API_TOKEN=your_token_here")
        return

    # Test with sample newsletter data
    test_summary = """
    Recent advances in AI-powered cancer detection have shown promising results.
    New deep learning models achieve 95% accuracy in early-stage diagnosis.
    Treatment planning algorithms optimize personalized therapy selection.
    """

    test_topic = "AI in Cancer Care"
    test_topics = [
        "Cancer Research",
        "Early Detection",
        "Treatment Planning"
    ]

    print("🧪 Testing Flux image generation...")
    print(f"Topic: {test_topic}")
    print(f"Sub-topics: {', '.join(test_topics)}")

    filepath = generator.generate_cover_image(
        executive_summary=test_summary,
        main_topic=test_topic,
        topics=test_topics,
        style="professional"
    )

    if filepath:
        print(f"✅ Test successful! Image saved to: {filepath}")
    else:
        print("❌ Test failed - no image generated")


if __name__ == "__main__":
    # Set up logging for testing
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    test_flux_generation()
