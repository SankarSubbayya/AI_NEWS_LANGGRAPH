"""Regenerate newsletter with enhanced cover image."""

import os
import sys
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_news_langgraph.enhanced_cover_generator import generate_enhanced_cover_base64
from ai_news_langgraph.cancer_research_knowledge_graph import CancerResearchKnowledgeGraph
from ai_news_langgraph.glossary_generator import generate_glossary_for_newsletter
from ai_news_langgraph.html_generator import HTMLNewsletterGenerator

# Sample newsletter data
executive_summary = """
This week, we spotlight groundbreaking advances in AI-powered cancer diagnostics 
and treatment. Deep learning models are revolutionizing breast cancer detection 
in mammography images, achieving 95% accuracy rates. Meanwhile, immunotherapy 
targeting PD-L1 biomarkers shows remarkable promise in clinical trials for lung 
cancer patients. Machine learning algorithms are also transforming precision 
medicine by analyzing genomic data to predict treatment responses for melanoma 
and colorectal cancer. These innovations represent a paradigm shift in oncology,
combining artificial intelligence with personalized medicine to improve patient outcomes.
"""

topic_summaries = [
    {
        "topic": "AI Diagnostics",
        "overview": "Computer vision and deep learning transform cancer screening and detection.",
        "key_findings": [
            "Convolutional neural networks achieve 95% accuracy in mammography analysis for breast cancer",
            "Machine learning models detect lung cancer in CT scans 6 months earlier than radiologists",
            "Natural language processing analyzes pathology reports for colorectal cancer with high precision",
            "AI-powered liquid biopsy detects circulating tumor DNA in pancreatic cancer patients"
        ]
    },
    {
        "topic": "Immunotherapy Advances",
        "overview": "Checkpoint inhibitors and targeted therapies show breakthrough results.",
        "key_findings": [
            "Pembrolizumab targeting PD-L1 improves survival rates in non-small cell lung cancer",
            "Combination immunotherapy with nivolumab extends progression-free survival in melanoma",
            "CAR-T cell therapy shows promise in treating aggressive lymphoma cases",
            "Biomarker-guided immunotherapy selection improves response rates by 40%"
        ]
    },
    {
        "topic": "Precision Medicine",
        "overview": "Genomic profiling and AI enable personalized cancer treatment.",
        "key_findings": [
            "Next-generation sequencing identifies actionable mutations in 67% of patients",
            "Machine learning predicts chemotherapy response from tumor genomics",
            "BRCA1/BRCA2 genetic testing guides treatment decisions in ovarian cancer",
            "Liquid biopsy tracks treatment efficacy through ctDNA monitoring"
        ]
    }
]

def main():
    print("=" * 80)
    print("🎨 REGENERATING NEWSLETTER WITH ENHANCED COVER")
    print("=" * 80)
    print()
    
    # Step 1: Generate enhanced cover
    print("📸 Step 1: Generating enhanced cover image...")
    styles = ["professional", "modern", "abstract", "scientific"]
    
    print("\nAvailable styles:")
    for i, style in enumerate(styles, 1):
        print(f"  {i}. {style.title()}")
    
    try:
        choice = input("\nChoose a style (1-4) [default: 1]: ").strip()
        style_idx = int(choice) - 1 if choice else 0
        selected_style = styles[style_idx] if 0 <= style_idx < len(styles) else styles[0]
    except (ValueError, IndexError):
        selected_style = "professional"
    
    print(f"   ✓ Using '{selected_style}' style")
    cover_image = generate_enhanced_cover_base64(
        main_topic="AI in Cancer Care",
        style=selected_style
    )
    print(f"   ✓ Cover generated ({len(cover_image)} characters)")
    
    # Step 2: Build knowledge graph
    print("\n🧠 Step 2: Building cancer research knowledge graph...")
    kg = CancerResearchKnowledgeGraph()
    graph_data = kg.build_from_newsletter(executive_summary, topic_summaries)
    
    print(f"   ✓ Extracted {graph_data['total_entities']} medical entities")
    print(f"   ✓ Found {graph_data['total_relationships']} medical relationships")
    
    # Step 3: Extract top terms
    print("\n🔑 Step 3: Extracting high-centrality medical terms...")
    top_entities_data = graph_data['top_entities'][:15]
    high_centrality_terms = [entity[0] for entity in top_entities_data]  # entity[0] is the name
    print(f"   ✓ Top 15 terms: {', '.join(high_centrality_terms[:5])}...")
    
    # Step 4: Generate glossary
    print("\n📚 Step 4: Generating AI-powered glossary...")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("   ⚠️  No OPENAI_API_KEY found, using mock glossary")
        glossary_html = _create_mock_glossary(top_entities_data)
    else:
        glossary_result = generate_glossary_for_newsletter(
            executive_summary=executive_summary,
            topic_summaries=topic_summaries,
            top_n=15,
            high_centrality_terms=high_centrality_terms
        )
        glossary_html = glossary_result['html']
        print(f"   ✓ Generated glossary with {len(high_centrality_terms)} terms")
    
    # Step 5: Generate HTML
    print("\n📄 Step 5: Generating complete HTML newsletter...")
    
    # Build knowledge graph summary section
    kg_section = _build_kg_section(graph_data)
    
    # Append KG section and glossary to topics before generating HTML
    modified_summary = executive_summary + kg_section
    
    html_content = HTMLNewsletterGenerator.generate_newsletter_html(
        executive_summary=modified_summary,
        topic_summaries=topic_summaries,
        main_topic="AI in Cancer Care",
        metrics=None,
        chart_images=None,
        cover_image=cover_image
    )
    
    # Insert glossary before closing tags
    html_content = html_content.replace(
        '</div>\n</body>',
        f'{glossary_html}</div>\n</body>'
    )
    
    # Save file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = "outputs/newsletters"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"enhanced_newsletter_{timestamp}.html")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"   ✓ Saved to: {output_file}")
    
    # Step 6: Summary
    print("\n" + "=" * 80)
    print("✅ NEWSLETTER GENERATION COMPLETE!")
    print("=" * 80)
    print(f"\n📁 File: {output_file}")
    print(f"🎨 Style: {selected_style.title()}")
    print(f"📊 Knowledge Graph: {graph_data['total_entities']} entities, {graph_data['total_relationships']} relationships")
    print(f"📚 Glossary: {len(high_centrality_terms)} medical terms")
    print(f"\n🌐 Open in browser:")
    print(f"   file://{os.path.abspath(output_file)}")
    print()

def _build_kg_section(graph_data):
    """Build knowledge graph insights section."""
    return ""  # KG stats will be added to the full HTML in the generator


def _create_mock_glossary(top_entities_data):
    """Create a simple mock glossary.
    
    Args:
        top_entities_data: List of tuples (entity_name, score, entity_type)
    """
    glossary_html = """
    <!-- Glossary -->
    <div class="section" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 30px; border-radius: 10px; margin-top: 30px;">
        <h2 class="section-title">📚 Key Terms Glossary</h2>
        <p style="color: #4a5568; font-size: 14px; margin-bottom: 25px; font-style: italic;">
            Important medical and AI terms from this newsletter
        </p>
"""
    
    for entity_name, score, entity_type in top_entities_data[:10]:
        priority = "⭐ High Priority" if score > 4 else "Important"
        color = "#e53e3e" if score > 4 else "#ed8936"
        glossary_html += f"""
        <div style="background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                <h3 style="color: #2d3748; font-size: 20px; margin: 0; font-weight: 600;">
                    {entity_name.title()}
                </h3>
                <span style="background: {color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600; white-space: nowrap;">
                    {priority}
                </span>
            </div>
            <p style="color: #4a5568; font-size: 15px; line-height: 1.6; margin: 10px 0;">
                A key medical term in cancer research (Type: {entity_type.replace('_', ' ').title()}, Score: {score:.2f})
            </p>
        </div>
"""
    
    glossary_html += """
    </div>
"""
    return glossary_html

if __name__ == "__main__":
    main()

