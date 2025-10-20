"""Generate Flux Prompts for Newsletter Covers.

This script demonstrates how to create CivitAI-quality prompts for Flux AI
to generate stunning newsletter cover images.
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_news_langgraph.flux_prompt_generator import (
    generate_flux_prompt_for_newsletter,
    FluxPromptGenerator
)


def print_separator(title=""):
    """Print a nice separator."""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)
    print()


def example_1_basic():
    """Example 1: Generate basic newsletter cover prompt."""
    print_separator("Example 1: Basic Newsletter Cover Prompt")
    
    executive_summary = """
    This week, we spotlight the groundbreaking integration of artificial intelligence
    in clinical trial design and patient matching, which is revolutionizing oncology
    research. AI's capacity to analyze vast datasets is enhancing the precision of
    participant selection, thereby accelerating the pace of clinical trials.
    """
    
    topics = ["Cancer Research", "Early Detection", "Treatment Planning"]
    
    print("📰 Newsletter Content:")
    print(f"   Topic: AI in Cancer Care")
    print(f"   Sub-topics: {', '.join(topics)}")
    print(f"   Summary: {executive_summary.strip()[:100]}...")
    print()
    
    # Generate prompt
    prompts = generate_flux_prompt_for_newsletter(
        executive_summary=executive_summary,
        main_topic="AI in Cancer Care",
        topics=topics,
        style="professional"
    )
    
    print("✅ Generated Flux Prompts:")
    print()
    print("📝 POSITIVE PROMPT (Copy to CivitAI):")
    print("-" * 80)
    print(prompts['positive'])
    print()
    print("🚫 NEGATIVE PROMPT (Copy to CivitAI):")
    print("-" * 80)
    print(prompts['negative'])
    print()
    print("💡 Detected Themes:")
    themes = prompts.get('themes', {})
    print(f"   - Medical: {'Yes' if themes.get('is_medical') else 'No'}")
    print(f"   - AI-Focused: {'Yes' if themes.get('is_ai_focused') else 'No'}")
    print(f"   - Research: {'Yes' if themes.get('is_research') else 'No'}")
    print(f"   - Data Analysis: {'Yes' if themes.get('is_data') else 'No'}")


def example_2_multiple_styles():
    """Example 2: Generate prompts for multiple styles."""
    print_separator("Example 2: Multiple Style Variations")
    
    summary = "Breakthrough in AI-powered genomic analysis enables personalized cancer treatment."
    topics = ["Genomics", "Immunotherapy", "Precision Medicine"]
    
    print("📰 Newsletter Content:")
    print(f"   Topic: Precision Oncology")
    print(f"   Sub-topics: {', '.join(topics)}")
    print()
    
    styles = ["professional", "futuristic", "cinematic", "minimalist"]
    
    print(f"🎨 Generating {len(styles)} style variations...")
    print()
    
    for i, style in enumerate(styles, 1):
        print(f"\n{'─' * 80}")
        print(f"Style {i}/{len(styles)}: {style.upper()}")
        print(f"{'─' * 80}")
        
        prompts = generate_flux_prompt_for_newsletter(
            executive_summary=summary,
            main_topic="Precision Oncology",
            topics=topics,
            style=style
        )
        
        # Show first 150 characters of positive prompt
        positive_preview = prompts['positive'][:150] + "..."
        print(f"\n📝 Positive (preview): {positive_preview}")
        
        print(f"\n💾 Save to file: flux_prompt_{style}.txt")


def example_3_sample_prompts():
    """Example 3: Show pre-made sample prompts."""
    print_separator("Example 3: Pre-Made Sample Prompts")
    
    print("🎨 Here are 5 ready-to-use CivitAI prompts:")
    print()
    
    generator = FluxPromptGenerator()
    samples = generator.generate_sample_prompts()
    
    for i, sample in enumerate(samples, 1):
        print(f"\n{'─' * 80}")
        print(f"{i}. {sample['name']}")
        print(f"{'─' * 80}")
        print()
        print("📝 POSITIVE:")
        # Wrap text at 80 characters
        positive = sample['positive']
        words = positive.split(', ')
        line = ""
        for word in words:
            if len(line) + len(word) + 2 > 78:
                print(f"   {line},")
                line = word
            else:
                if line:
                    line += ", " + word
                else:
                    line = word
        if line:
            print(f"   {line}")
        
        print()
        print(f"🚫 NEGATIVE: {sample['negative']}")


def example_4_custom_civitai():
    """Example 4: Create custom CivitAI-style prompt."""
    print_separator("Example 4: Custom CivitAI-Style Prompt")
    
    generator = FluxPromptGenerator()
    
    print("🎯 Creating custom prompt for specific concept...")
    print()
    
    # Custom concept
    main_concept = "futuristic AI-powered cancer research laboratory with holographic displays"
    style_tags = [
        "neon blue and purple lighting",
        "cinematic composition",
        "dramatic atmosphere",
        "high-tech medical equipment",
        "glowing data visualizations"
    ]
    
    print("📋 Input:")
    print(f"   Main Concept: {main_concept}")
    print(f"   Style Tags: {', '.join(style_tags)}")
    print()
    
    # Generate for different quality levels
    for quality in ["high", "ultra", "maximum"]:
        print(f"\n{'─' * 80}")
        print(f"Quality Level: {quality.upper()}")
        print(f"{'─' * 80}")
        
        prompts = generator.create_civitai_prompt(
            main_concept=main_concept,
            style_tags=style_tags,
            quality_level=quality
        )
        
        positive_preview = prompts['positive'][:120] + "..."
        print(f"\n📝 Positive (preview): {positive_preview}")


def example_5_save_prompts():
    """Example 5: Save prompts to files for CivitAI."""
    print_separator("Example 5: Save Prompts to Files")
    
    summary = "Weekly AI cancer research roundup featuring breakthroughs in early detection."
    topics = ["Early Detection", "Biomarkers", "Imaging"]
    
    # Create output directory
    output_dir = "outputs/flux_prompts"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📁 Saving prompts to: {output_dir}/")
    print()
    
    styles = ["professional", "modern", "futuristic", "cinematic", "minimalist"]
    
    for style in styles:
        prompts = generate_flux_prompt_for_newsletter(
            executive_summary=summary,
            main_topic="AI Cancer Research Weekly",
            topics=topics,
            style=style
        )
        
        # Save to JSON
        filename = f"{output_dir}/prompt_{style}.json"
        with open(filename, 'w') as f:
            json.dump(prompts, f, indent=2)
        
        # Save to text (easy to copy)
        txt_filename = f"{output_dir}/prompt_{style}.txt"
        with open(txt_filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write(f"FLUX PROMPT - {style.upper()} STYLE\n")
            f.write("="*80 + "\n\n")
            f.write("POSITIVE PROMPT:\n")
            f.write("-"*80 + "\n")
            f.write(prompts['positive'] + "\n\n")
            f.write("NEGATIVE PROMPT:\n")
            f.write("-"*80 + "\n")
            f.write(prompts['negative'] + "\n\n")
            f.write("="*80 + "\n")
            f.write("HOW TO USE ON CIVITAI:\n")
            f.write("="*80 + "\n")
            f.write("1. Go to https://civitai.com/\n")
            f.write("2. Select Flux.1 Dev or Flux.1 Pro model\n")
            f.write("3. Copy the POSITIVE PROMPT above\n")
            f.write("4. Copy the NEGATIVE PROMPT above\n")
            f.write("5. Set aspect ratio to 16:9\n")
            f.write("6. Set steps to 20-30\n")
            f.write("7. Generate!\n")
        
        print(f"✅ Saved: {style}.json and {style}.txt")
    
    print()
    print(f"📂 All prompts saved to: {output_dir}/")
    print("💡 Open the .txt files to easily copy-paste to CivitAI!")


def example_6_newsletter_workflow():
    """Example 6: Complete newsletter-to-CivitAI workflow."""
    print_separator("Example 6: Complete Newsletter Workflow")
    
    print("📋 Workflow: Newsletter Content → Flux Prompt → CivitAI → Cover Image")
    print()
    
    # Step 1
    print("Step 1️⃣: Prepare Newsletter Content")
    print("-" * 80)
    summary = """
    Revolutionary advances in liquid biopsy technology are enabling earlier cancer
    detection through AI-powered analysis of circulating tumor DNA. These breakthroughs
    promise to transform screening protocols and significantly improve patient outcomes.
    """
    topics = ["Liquid Biopsy", "Early Detection", "ctDNA Analysis"]
    
    print(f"✅ Topic: AI in Early Cancer Detection")
    print(f"✅ Sub-topics: {', '.join(topics)}")
    print()
    
    # Step 2
    print("Step 2️⃣: Generate Flux Prompt")
    print("-" * 80)
    prompts = generate_flux_prompt_for_newsletter(
        executive_summary=summary,
        main_topic="AI in Early Cancer Detection",
        topics=topics,
        style="professional"
    )
    print(f"✅ Prompt generated ({len(prompts['positive'])} chars)")
    print()
    
    # Step 3
    print("Step 3️⃣: Use on CivitAI")
    print("-" * 80)
    print("✅ Go to: https://civitai.com/")
    print("✅ Select: Flux.1 Dev or Flux.1 Pro")
    print("✅ Settings:")
    print("   - Aspect Ratio: 16:9 (1792×1024)")
    print("   - Steps: 25")
    print("   - CFG Scale: 7.5")
    print("   - Sampler: DPM++ 2M Karras")
    print()
    
    # Step 4
    print("Step 4️⃣: Copy These Prompts to CivitAI")
    print("-" * 80)
    print()
    print("📝 POSITIVE PROMPT:")
    print(prompts['positive'])
    print()
    print("🚫 NEGATIVE PROMPT:")
    print(prompts['negative'])
    print()
    
    # Step 5
    print("Step 5️⃣: Generate and Download")
    print("-" * 80)
    print("✅ Click 'Generate' on CivitAI")
    print("✅ Wait 10-30 seconds")
    print("✅ Download the generated image")
    print("✅ Save to: outputs/images/newsletter_cover.png")
    print()
    
    # Step 6
    print("Step 6️⃣: Use in Newsletter")
    print("-" * 80)
    print("✅ Use html_generator.py to add cover to newsletter")
    print("✅ Share your beautiful newsletter!")


def main():
    """Run examples."""
    print()
    print("🎨" * 40)
    print()
    print("  FLUX PROMPT GENERATOR FOR NEWSLETTER COVERS")
    print("  Optimized for CivitAI Quality Standards")
    print()
    print("🎨" * 40)
    
    print()
    print("This tool generates professional Flux prompts for creating stunning")
    print("newsletter cover images on CivitAI (https://civitai.com/)")
    print()
    
    # Run examples
    try:
        example_1_basic()
        input("\n\nPress Enter to see Example 2 (Multiple Styles)...")
        
        example_2_multiple_styles()
        input("\n\nPress Enter to see Example 3 (Sample Prompts)...")
        
        example_3_sample_prompts()
        input("\n\nPress Enter to see Example 4 (Custom CivitAI)...")
        
        example_4_custom_civitai()
        input("\n\nPress Enter to see Example 5 (Save to Files)...")
        
        example_5_save_prompts()
        input("\n\nPress Enter to see Example 6 (Complete Workflow)...")
        
        example_6_newsletter_workflow()
        
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        return
    
    # Completion
    print_separator("✅ Examples Complete!")
    
    print("🎯 Next Steps:")
    print()
    print("1. Choose a prompt from above")
    print("2. Go to https://civitai.com/")
    print("3. Select Flux.1 Dev (free) or Flux.1 Pro")
    print("4. Paste the prompt")
    print("5. Set aspect ratio to 16:9")
    print("6. Generate your cover image!")
    print()
    print("📚 For more info, see: docs/FLUX_PROMPTS_GUIDE.md")
    print()
    print("🎨 Happy creating!")
    print()


if __name__ == "__main__":
    main()

