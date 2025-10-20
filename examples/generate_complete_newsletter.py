"""Complete Newsletter Generation with Cover, Keywords, and Glossary.

This example demonstrates the full workflow:
1. Generate cover image (or Flux prompt)
2. Extract cancer research entities and keywords
3. Identify high-centrality terms
4. Generate AI-powered glossary
5. Create complete HTML newsletter with all components
"""

import os
import sys
import base64
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_news_langgraph.cancer_research_knowledge_graph import CancerResearchKnowledgeGraph
from ai_news_langgraph.glossary_generator import GlossaryGenerator
from ai_news_langgraph.flux_prompt_generator import generate_flux_prompt_for_newsletter
from ai_news_langgraph.cover_image_generator import CoverImageGenerator


def generate_complete_newsletter():
    """Generate a complete newsletter with all enhancements."""
    
    print("=" * 80)
    print("🔬 COMPLETE NEWSLETTER GENERATION")
    print("=" * 80)
    print()
    
    # Sample newsletter content
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
            'topic_name': 'AI Diagnostics',
            'overview': 'Computer vision and deep learning transform cancer screening and detection.',
            'key_findings': [
                'Convolutional neural networks achieve 95% accuracy in mammography analysis for breast cancer',
                'Machine learning models detect lung cancer in CT scans 6 months earlier than radiologists',
                'Natural language processing analyzes pathology reports for colorectal cancer with high precision',
                'AI-powered liquid biopsy detects circulating tumor DNA in pancreatic cancer patients'
            ],
            'articles': [
                {
                    'title': 'Deep Learning for Breast Cancer Screening',
                    'source': 'Nature Medicine',
                    'url': 'https://example.com/article1',
                    'relevance_score': 0.95
                },
                {
                    'title': 'AI Detects Lung Cancer Earlier',
                    'source': 'JAMA Oncology',
                    'url': 'https://example.com/article2',
                    'relevance_score': 0.92
                }
            ]
        },
        {
            'topic_name': 'Immunotherapy Advances',
            'overview': 'Checkpoint inhibitors and targeted therapies show breakthrough results.',
            'key_findings': [
                'Pembrolizumab targeting PD-L1 improves survival rates in non-small cell lung cancer',
                'Combination immunotherapy with nivolumab extends progression-free survival in melanoma',
                'CAR-T cell therapy shows promise in treating aggressive lymphoma cases',
                'Biomarker-guided immunotherapy selection improves response rates by 40%'
            ],
            'articles': [
                {
                    'title': 'PD-L1 Inhibitors in Lung Cancer',
                    'source': 'The Lancet',
                    'url': 'https://example.com/article3',
                    'relevance_score': 0.94
                }
            ]
        },
        {
            'topic_name': 'Precision Medicine',
            'overview': 'Genomic profiling and AI enable personalized cancer treatment.',
            'key_findings': [
                'Next-generation sequencing identifies actionable mutations in 67% of patients',
                'Machine learning predicts chemotherapy response from tumor genomics',
                'BRCA1/BRCA2 genetic testing guides treatment decisions in ovarian cancer',
                'Liquid biopsy tracks treatment efficacy through ctDNA monitoring'
            ],
            'articles': [
                {
                    'title': 'Genomic Profiling for Treatment Selection',
                    'source': 'Cell',
                    'url': 'https://example.com/article4',
                    'relevance_score': 0.91
                }
            ]
        }
    ]
    
    main_topic = "AI in Cancer Care"
    
    # -------------------------------------------------------------------------
    # STEP 1: Generate Cover Image Prompt (Flux)
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 1: Generate Cover Image Prompt")
    print("=" * 80)
    print()
    
    cover_prompts = generate_flux_prompt_for_newsletter(
        executive_summary=executive_summary,
        main_topic=main_topic,
        topics=[t['topic_name'] for t in topic_summaries],
        style="professional"
    )
    
    print("✅ Flux Prompt Generated!")
    print(f"\n📝 Use this prompt on CivitAI:")
    print(f"\nPositive: {cover_prompts['positive'][:150]}...")
    print(f"\nNegative: {cover_prompts['negative']}")
    
    # Optional: Generate fallback cover with Pillow
    print("\n💡 Generating fallback cover image...")
    cover_gen = CoverImageGenerator()
    cover_path = cover_gen.generate_fallback_image(main_topic)
    
    # Convert to base64 for HTML
    cover_image = None
    if cover_path:
        with open(cover_path, 'rb') as f:
            cover_b64 = base64.b64encode(f.read()).decode()
            cover_image = f"data:image/png;base64,{cover_b64}"
        print(f"✅ Fallback cover created: {cover_path}")
    
    # -------------------------------------------------------------------------
    # STEP 2: Build Cancer Research Knowledge Graph
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 2: Build Cancer Research Knowledge Graph")
    print("=" * 80)
    print()
    
    kg = CancerResearchKnowledgeGraph()
    graph_data = kg.build_from_newsletter(
        executive_summary=executive_summary,
        topic_summaries=topic_summaries
    )
    
    print(f"✅ Knowledge Graph Built!")
    print(f"   Total Entities: {graph_data['total_entities']}")
    print(f"   Total Relationships: {graph_data['total_relationships']}")
    print()
    
    print("📊 Entities by Type:")
    for entity_type, count in graph_data['entity_counts'].items():
        print(f"   • {entity_type.replace('_', ' ').title()}: {count}")
    
    print("\n🔑 Top 10 Important Entities (High Centrality):")
    for i, (entity, score, entity_type) in enumerate(graph_data['top_entities'][:10], 1):
        print(f"   {i:2}. {entity.title():30} ({entity_type:15}) Score: {score:.2f}")
    
    # -------------------------------------------------------------------------
    # STEP 3: Generate AI-Powered Glossary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 3: Generate AI-Powered Glossary")
    print("=" * 80)
    print()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Using mock glossary.")
        glossary = _create_mock_glossary(graph_data)
    else:
        print("🤖 Generating definitions with GPT-4...")
        print("   (This may take 30-60 seconds)")
        print()
        
        glossary_gen = GlossaryGenerator()
        
        # Create glossary entries from top entities
        glossary = []
        for entity, score, entity_type in graph_data['top_entities'][:15]:
            # Get entity details
            entity_details = kg.get_entity_details(entity)
            
            if entity_details:
                # Get related terms
                related = [r['target'] for r in entity_details['outgoing_relationships'][:3]]
                
                try:
                    # Generate definition
                    definition = glossary_gen._generate_definition(
                        term=entity.title(),
                        related_terms=[r.title() for r in related],
                        context="AI in Cancer Care",
                        frequency=entity_details['frequency']
                    )
                    
                    glossary.append({
                        'term': entity.title(),
                        'definition': definition,
                        'related_terms': [r.title() for r in related],
                        'importance': 'high' if score > 2.0 else 'medium' if score > 1.0 else 'low',
                        'entity_type': entity_type
                    })
                    
                    print(f"   ✓ {entity.title()}")
                    
                except Exception as e:
                    print(f"   ✗ Failed: {entity.title()} ({e})")
    
    print(f"\n✅ Glossary generated with {len(glossary)} terms!")
    
    # -------------------------------------------------------------------------
    # STEP 4: Generate Complete HTML Newsletter
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 4: Generate Complete HTML Newsletter")
    print("=" * 80)
    print()
    
    html_content = _generate_newsletter_html(
        executive_summary=executive_summary,
        topic_summaries=topic_summaries,
        main_topic=main_topic,
        cover_image=cover_image,
        glossary=glossary,
        graph_data=graph_data
    )
    
    # Save newsletter
    output_dir = "outputs/newsletters"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/complete_newsletter_{timestamp}.html"
    
    with open(filename, 'w') as f:
        f.write(html_content)
    
    print(f"✅ Newsletter saved: {filename}")
    
    # -------------------------------------------------------------------------
    # STEP 5: Generate Summary Report
    # -------------------------------------------------------------------------
    print("\n" + "=" * 80)
    print("STEP 5: Summary Report")
    print("=" * 80)
    print()
    
    print("📄 Newsletter Components:")
    print(f"   ✓ Cover Image: {'Yes (fallback)' if cover_image else 'Flux prompt generated'}")
    print(f"   ✓ Executive Summary: Yes")
    print(f"   ✓ Topics: {len(topic_summaries)}")
    print(f"   ✓ Knowledge Graph: {graph_data['total_entities']} entities, {graph_data['total_relationships']} relationships")
    print(f"   ✓ Glossary: {len(glossary)} terms")
    print()
    
    print("🔑 Top Keywords Highlighted:")
    for i, (entity, score, _) in enumerate(graph_data['top_entities'][:5], 1):
        print(f"   {i}. {entity.title()}")
    print()
    
    print("📚 Glossary Terms:")
    for entry in glossary[:5]:
        print(f"   • {entry['term']} ({entry['entity_type']})")
    print(f"   ... and {len(glossary) - 5} more")
    print()
    
    print("=" * 80)
    print("✅ COMPLETE NEWSLETTER GENERATION FINISHED!")
    print("=" * 80)
    print()
    print(f"📂 Output: {filename}")
    print(f"🌐 Open in browser: open {filename}")
    print()


def _create_mock_glossary(graph_data):
    """Create mock glossary when no API key available."""
    mock_glossary = []
    
    mock_definitions = {
        'breast cancer': 'A malignant tumor that develops in breast tissue, one of the most common cancers affecting women and increasingly diagnosed using AI-powered imaging analysis.',
        'machine learning': 'A subset of artificial intelligence that enables computers to learn from data and improve their performance without explicit programming, widely used in cancer diagnostics.',
        'immunotherapy': 'A type of cancer treatment that harnesses the immune system to fight cancer cells, including checkpoint inhibitors and CAR-T cell therapy.',
        'pd-l1': 'Programmed Death-Ligand 1, a protein biomarker used to predict response to immunotherapy in various cancers including lung cancer and melanoma.',
        'mammography': 'An X-ray imaging technique used to screen for and diagnose breast cancer, increasingly enhanced by AI algorithms for improved accuracy.',
        'deep learning': 'An advanced form of machine learning using neural networks with multiple layers, particularly effective in medical image analysis.',
        'lung cancer': 'Cancer that begins in the lungs, often detected using CT scans and increasingly diagnosed earlier with AI-powered screening tools.',
        'genomics': 'The study of an organism\'s complete set of DNA, used in cancer care to identify genetic mutations and guide personalized treatment decisions.',
        'biomarker': 'A measurable biological indicator used to detect disease presence, predict treatment response, or monitor disease progression in cancer patients.',
        'precision medicine': 'An approach to patient care that uses genetic, environmental, and lifestyle factors to customize prevention and treatment strategies.'
    }
    
    for entity, score, entity_type in graph_data['top_entities'][:15]:
        definition = mock_definitions.get(entity, f"A key term in cancer research related to {entity_type.replace('_', ' ')}.")
        
        mock_glossary.append({
            'term': entity.title(),
            'definition': definition,
            'related_terms': [],
            'importance': 'high' if score > 2.0 else 'medium' if score > 1.0 else 'low',
            'entity_type': entity_type
        })
    
    return mock_glossary


def _generate_newsletter_html(
    executive_summary,
    topic_summaries,
    main_topic,
    cover_image,
    glossary,
    graph_data
):
    """Generate complete HTML newsletter."""
    date_str = datetime.now().strftime("%B %d, %Y")
    
    # Format glossary HTML
    glossary_html = _format_glossary_html(glossary)
    
    # Format knowledge graph summary
    kg_summary_html = _format_kg_summary_html(graph_data)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{main_topic} Newsletter - {date_str}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #2d3748;
            background: #f7fafc;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .cover {{
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 60px 40px;
            text-align: center;
            color: white;
        }}
        
        .cover img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .cover h1 {{
            font-size: 42px;
            margin-bottom: 10px;
            font-weight: 700;
        }}
        
        .cover .date {{
            font-size: 18px;
            opacity: 0.9;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section-title {{
            font-size: 28px;
            color: #1a202c;
            margin-bottom: 20px;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .executive-summary {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 8px;
            border-left: 5px solid #667eea;
            margin-bottom: 40px;
        }}
        
        .topic {{
            background: #f7fafc;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 25px;
            border-left: 4px solid #48bb78;
        }}
        
        .topic-title {{
            font-size: 22px;
            color: #2d3748;
            margin-bottom: 15px;
            font-weight: 600;
        }}
        
        .findings {{
            list-style: none;
            padding-left: 0;
        }}
        
        .findings li {{
            padding: 10px 0;
            padding-left: 25px;
            position: relative;
        }}
        
        .findings li:before {{
            content: "✓";
            position: absolute;
            left: 0;
            color: #48bb78;
            font-weight: bold;
        }}
        
        .keyword {{
            background: #fef3c7;
            padding: 2px 6px;
            border-radius: 3px;
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Cover Page -->
        <div class="cover">
            {f'<img src="{cover_image}" alt="Newsletter Cover">' if cover_image else ''}
            <h1>🔬 {main_topic}</h1>
            <p class="date">Newsletter • {date_str}</p>
        </div>
        
        <!-- Content -->
        <div class="content">
            <!-- Executive Summary -->
            <div class="executive-summary">
                <h2 class="section-title">Executive Summary</h2>
                <p>{_highlight_keywords(executive_summary, graph_data)}</p>
            </div>
            
            <!-- Topics -->
            <div class="section">
                <h2 class="section-title">Featured Topics</h2>
"""
    
    # Add topics
    for topic in topic_summaries:
        html += f"""
                <div class="topic">
                    <h3 class="topic-title">{topic['topic_name']}</h3>
                    <p style="margin-bottom: 15px;">{_highlight_keywords(topic['overview'], graph_data)}</p>
                    <h4 style="color: #4a5568; margin-bottom: 10px;">Key Findings:</h4>
                    <ul class="findings">
"""
        for finding in topic['key_findings']:
            html += f"                        <li>{_highlight_keywords(finding, graph_data)}</li>\n"
        
        html += """                    </ul>
                </div>
"""
    
    # Add Knowledge Graph Summary
    html += kg_summary_html
    
    # Add Glossary
    html += glossary_html
    
    # Close HTML
    html += """
        </div>
    </div>
</body>
</html>
"""
    
    return html


def _highlight_keywords(text, graph_data):
    """Highlight top keywords in text."""
    highlighted = text
    
    # Get top 10 entities
    top_entities = [entity.lower() for entity, _, _ in graph_data['top_entities'][:10]]
    
    for entity in top_entities:
        # Case-insensitive replacement
        import re
        pattern = re.compile(re.escape(entity), re.IGNORECASE)
        
        def replacer(match):
            return f'<span class="keyword">{match.group(0)}</span>'
        
        highlighted = pattern.sub(replacer, highlighted)
    
    return highlighted


def _format_glossary_html(glossary):
    """Format glossary as HTML."""
    if not glossary:
        return ""
    
    html = """
            <!-- Glossary -->
            <div class="section" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 30px; border-radius: 10px;">
                <h2 class="section-title">📚 Key Terms Glossary</h2>
                <p style="color: #4a5568; font-size: 14px; margin-bottom: 25px; font-style: italic;">
                    Important medical and AI terms from this newsletter
                </p>
"""
    
    for entry in glossary:
        importance_colors = {
            'high': '#e53e3e',
            'medium': '#ed8936',
            'low': '#48bb78'
        }
        importance_labels = {
            'high': '⭐ High Priority',
            'medium': '✓ Important',
            'low': 'Reference'
        }
        
        color = importance_colors.get(entry['importance'], '#718096')
        label = importance_labels.get(entry['importance'], 'Reference')
        
        html += f"""
                <div style="background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                        <h3 style="color: #2d3748; font-size: 20px; margin: 0; font-weight: 600;">
                            {entry['term']}
                        </h3>
                        <span style="background: {color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 600; white-space: nowrap;">
                            {label}
                        </span>
                    </div>
                    <p style="color: #4a5568; font-size: 15px; line-height: 1.6; margin: 10px 0;">
                        {entry['definition']}
                    </p>
"""
        
        if entry.get('related_terms'):
            related_str = ", ".join(entry['related_terms'][:3])
            html += f"""
                    <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #e2e8f0;">
                        <span style="color: #718096; font-size: 13px; font-weight: 600;">Related: </span>
                        <span style="color: #4a5568; font-size: 13px;">{related_str}</span>
                    </div>
"""
        
        html += """
                </div>
"""
    
    html += """
            </div>
"""
    
    return html


def _format_kg_summary_html(graph_data):
    """Format knowledge graph summary."""
    html = """
            <!-- Knowledge Graph Summary -->
            <div class="section" style="background: #edf2f7; padding: 30px; border-radius: 10px;">
                <h2 class="section-title">🧠 Newsletter Insights</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
"""
    
    for entity_type, count in list(graph_data['entity_counts'].items())[:4]:
        html += f"""
                    <div style="background: white; padding: 20px; border-radius: 8px; text-align: center;">
                        <div style="font-size: 32px; font-weight: 700; color: #667eea;">{count}</div>
                        <div style="color: #4a5568; font-size: 14px; text-transform: capitalize;">
                            {entity_type.replace('_', ' ')}
                        </div>
                    </div>
"""
    
    html += """
                </div>
            </div>
"""
    
    return html


if __name__ == "__main__":
    generate_complete_newsletter()

