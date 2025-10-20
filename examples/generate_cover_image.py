"""Example: Generate Cover Image for Newsletter.

This example demonstrates how to use the Cover Image Generator
to create professional cover images for your newsletters.
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_news_langgraph.cover_image_generator import (
    generate_newsletter_cover,
    CoverImageGenerator
)


def example_1_basic():
    """Example 1: Basic cover image generation."""
    print("=" * 60)
    print("Example 1: Basic Cover Image Generation")
    print("=" * 60)
    
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
    
    image_path = generate_newsletter_cover(
        executive_summary=executive_summary,
        main_topic="AI in Cancer Care",
        topics=topics,
        style="professional"
    )
    
    if image_path:
        print(f"✅ Cover image generated: {image_path}")
    else:
        print("❌ Failed to generate cover image")
    
    print()


def example_2_different_styles():
    """Example 2: Generate covers with different styles."""
    print("=" * 60)
    print("Example 2: Different Style Options")
    print("=" * 60)
    
    summary = "AI advances in precision oncology and personalized treatment."
    topics = ["Genomics", "Immunotherapy", "Diagnostics"]
    
    styles = ["professional", "modern", "abstract", "scientific", "futuristic"]
    
    for style in styles:
        print(f"\nGenerating {style} style cover...")
        image_path = generate_newsletter_cover(
            executive_summary=summary,
            main_topic="Precision Oncology",
            topics=topics,
            style=style
        )
        
        if image_path:
            print(f"✅ {style.capitalize()}: {image_path}")
    
    print()


def example_3_fallback():
    """Example 3: Using fallback image (no AI)."""
    print("=" * 60)
    print("Example 3: Fallback Image Generation")
    print("=" * 60)
    
    image_path = generate_newsletter_cover(
        executive_summary="Weekly newsletter content",
        main_topic="Cancer Research Weekly",
        topics=[],
        use_fallback=True
    )
    
    if image_path:
        print(f"✅ Fallback image created: {image_path}")
    
    print()


def example_4_advanced():
    """Example 4: Advanced usage with custom settings."""
    print("=" * 60)
    print("Example 4: Advanced Usage")
    print("=" * 60)
    
    # Initialize generator
    generator = CoverImageGenerator()
    
    # Custom settings
    summary = """
    Breakthrough discoveries in multi-omics data integration are enabling
    unprecedented insights into cancer biology. Machine learning models are
    identifying novel therapeutic targets with remarkable accuracy.
    """
    
    topics = [
        "Multi-Omics Integration",
        "Machine Learning Models",
        "Drug Discovery"
    ]
    
    # Generate with custom output directory
    image_path = generator.generate_cover_image(
        executive_summary=summary,
        main_topic="AI-Driven Drug Discovery",
        topics=topics,
        output_dir="custom_output/images",
        style="futuristic"
    )
    
    if image_path:
        print(f"✅ Custom cover generated: {image_path}")
        
        # Get base64 for HTML embedding
        base64_image = generator.embed_image_in_html(image_path)
        print(f"✅ Base64 encoded (length: {len(base64_image)} chars)")
        
        # Show how to use in HTML
        print("\nHTML Usage:")
        print(f'<img src="{base64_image[:50]}..." alt="Newsletter Cover">')
    
    print()


def example_5_error_handling():
    """Example 5: Proper error handling."""
    print("=" * 60)
    print("Example 5: Error Handling")
    print("=" * 60)
    
    try:
        # Attempt AI generation
        image_path = generate_newsletter_cover(
            executive_summary="Test newsletter",
            main_topic="Test Topic",
            topics=["Topic 1", "Topic 2"],
            style="professional"
        )
        
        if image_path:
            print(f"✅ AI generation successful: {image_path}")
        else:
            print("⚠️  AI generation failed, fallback was used")
            
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("   Using fallback as recovery...")
        
        # Use fallback as recovery
        image_path = generate_newsletter_cover(
            executive_summary="Test newsletter",
            main_topic="Test Topic",
            topics=[],
            use_fallback=True
        )
        
        if image_path:
            print(f"✅ Fallback recovery successful: {image_path}")
    
    print()


def main():
    """Run all examples."""
    print("\n")
    print("🎨" * 30)
    print("Cover Image Generator - Examples")
    print("🎨" * 30)
    print("\n")
    
    # Check for API key
    if os.getenv("OPENAI_API_KEY"):
        print("✅ OpenAI API key found")
    else:
        print("⚠️  No OpenAI API key - will use fallback images")
        print("   Set OPENAI_API_KEY environment variable for AI generation")
    
    print("\n")
    
    # Run examples
    example_1_basic()
    
    # Uncomment to run other examples:
    # example_2_different_styles()
    # example_3_fallback()
    # example_4_advanced()
    # example_5_error_handling()
    
    print("=" * 60)
    print("Examples Complete!")
    print("=" * 60)
    print("\nGenerated images are saved in: outputs/images/")
    print("\nFor more information, see: docs/COVER_IMAGE_GENERATOR.md")
    print()


if __name__ == "__main__":
    main()


