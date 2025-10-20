"""Generate Knowledge Graph and Glossary from Newsletter Content.

This example demonstrates how to:
1. Build a knowledge graph from newsletter content
2. Extract keywords and high-centrality terms
3. Generate AI-powered glossaries
4. Export and visualize the graph
"""

import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ai_news_langgraph.knowledge_graph_builder import KnowledgeGraphBuilder
from ai_news_langgraph.glossary_generator import GlossaryGenerator, generate_glossary_for_newsletter


def print_separator(title=""):
    """Print a nice separator."""
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)
    print()


def example_1_basic_knowledge_graph():
    """Example 1: Build a basic knowledge graph."""
    print_separator("Example 1: Basic Knowledge Graph")
    
    # Sample newsletter content
    exec_summary = """
    This week, we spotlight the groundbreaking integration of artificial intelligence
    in clinical trial design and patient matching. Machine learning algorithms are
    revolutionizing oncology research by analyzing genomic data and predicting
    treatment outcomes with unprecedented accuracy.
    """
    
    topic_summaries = [
        {
            'topic_name': 'Cancer Research',
            'overview': 'AI-powered diagnostic tools improving early cancer detection rates.',
            'key_findings': [
                'Deep learning models achieve 95% accuracy in tumor classification',
                'Computer vision systems detect malignancies in medical imaging',
                'Natural language processing analyzes pathology reports automatically'
            ]
        },
        {
            'topic_name': 'Treatment Planning',
            'overview': 'Personalized therapy recommendations using machine learning.',
            'key_findings': [
                'AI systems analyze patient genomics for treatment optimization',
                'Predictive models improve chemotherapy response rates by 30%',
                'Automated clinical decision support reduces treatment errors'
            ]
        },
        {
            'topic_name': 'Early Detection',
            'overview': 'Breakthrough in liquid biopsy technology for cancer screening.',
            'key_findings': [
                'Machine learning detects circulating tumor DNA with high sensitivity',
                'AI-powered screening reduces false positives in mammography',
                'Biomarker discovery accelerated through data mining'
            ]
        }
    ]
    
    print("📰 Building knowledge graph from newsletter content...")
    print()
    
    # Build knowledge graph
    builder = KnowledgeGraphBuilder()
    graph_data = builder.build_from_newsletter(exec_summary, topic_summaries)
    
    print(f"✅ Knowledge Graph Built!")
    print(f"   Total Terms: {graph_data['total_terms']}")
    print(f"   Total Relationships: {graph_data['total_relationships']}")
    print()
    
    print("🔑 Top 10 Keywords:")
    for i, kw in enumerate(graph_data['top_keywords'][:10], 1):
        print(f"   {i:2}. {kw['term'].title():35} | "
              f"Score: {kw['score']:.3f} | "
              f"Connections: {kw['connections']:2}")
    
    print()
    print("📊 High Centrality Terms (Most Connected):")
    for i, (term, score) in enumerate(graph_data['high_centrality_terms'][:10], 1):
        connections = len(builder.graph.get(term, []))
        print(f"   {i:2}. {term.title():35} | "
              f"Centrality: {score:.3f} | "
              f"Connections: {connections:2}")


def example_2_generate_glossary():
    """Example 2: Generate AI-powered glossary."""
    print_separator("Example 2: AI-Powered Glossary Generation")
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY not set. Skipping glossary generation.")
        print("   Set your API key to enable AI-powered definitions.")
        return
    
    # Sample content
    exec_summary = """
    Breakthrough advances in liquid biopsy technology are enabling earlier cancer
    detection through AI-powered analysis of circulating tumor DNA. These innovations
    promise to transform screening protocols and significantly improve patient outcomes.
    """
    
    topic_summaries = [
        {
            'topic_name': 'Liquid Biopsy',
            'overview': 'Non-invasive blood tests detect cancer biomarkers.',
            'key_findings': [
                'ctDNA analysis achieves 90% sensitivity for early-stage cancers',
                'Machine learning identifies genomic signatures in blood samples'
            ]
        },
        {
            'topic_name': 'AI Analysis',
            'overview': 'Deep learning models process complex genomic data.',
            'key_findings': [
                'Neural networks classify cancer types from biomarker patterns',
                'Automated pipelines reduce analysis time from weeks to hours'
            ]
        }
    ]
    
    print("📚 Generating glossary with AI-powered definitions...")
    print("   (This may take 10-30 seconds)")
    print()
    
    try:
        result = generate_glossary_for_newsletter(
            exec_summary,
            topic_summaries,
            top_n=8,
            output_format="markdown"
        )
        
        print(f"✅ Glossary generated with {result['total_terms']} terms!")
        print()
        print(result['markdown'])
        
    except Exception as e:
        print(f"❌ Error generating glossary: {e}")


def example_3_export_graph():
    """Example 3: Export knowledge graph to JSON."""
    print_separator("Example 3: Export Knowledge Graph")
    
    # Build graph
    exec_summary = "AI transforms cancer care through machine learning and deep learning."
    topic_summaries = [
        {
            'topic_name': 'AI in Oncology',
            'overview': 'Machine learning revolutionizes cancer diagnosis and treatment.',
            'key_findings': ['Deep learning improves diagnostic accuracy']
        }
    ]
    
    builder = KnowledgeGraphBuilder()
    builder.build_from_newsletter(exec_summary, topic_summaries)
    
    # Create output directory
    output_dir = "outputs/knowledge_graphs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Export to JSON
    json_file = f"{output_dir}/knowledge_graph_example.json"
    builder.export_graph_json(json_file)
    
    print(f"✅ Knowledge graph exported to: {json_file}")
    print()
    
    # Show visualization data
    viz_data = builder.visualize_graph_data()
    print(f"📊 Visualization Data:")
    print(f"   Nodes: {len(viz_data['nodes'])}")
    print(f"   Edges: {len(viz_data['edges'])}")
    print()
    print(f"   Sample nodes (first 5):")
    for node in viz_data['nodes'][:5]:
        print(f"      • {node['label']:30} (group: {node['group']}, "
              f"freq: {node['frequency']})")


def example_4_comprehensive():
    """Example 4: Comprehensive analysis."""
    print_separator("Example 4: Comprehensive Knowledge Graph Analysis")
    
    # Rich newsletter content
    exec_summary = """
    This week's newsletter covers groundbreaking developments in AI-powered cancer care.
    From machine learning algorithms that predict treatment outcomes to computer vision
    systems that detect malignancies in medical imaging, artificial intelligence is
    revolutionizing oncology. Deep learning models are analyzing genomic data, identifying
    biomarkers, and enabling personalized medicine at an unprecedented scale.
    """
    
    topic_summaries = [
        {
            'topic_name': 'Diagnostic AI',
            'overview': 'Computer vision and deep learning enhance cancer detection.',
            'key_findings': [
                'Convolutional neural networks classify histopathology slides',
                'AI systems detect subtle patterns invisible to human experts',
                'Automated screening reduces radiologist workload by 40%'
            ]
        },
        {
            'topic_name': 'Precision Medicine',
            'overview': 'Genomic analysis guides personalized treatment selection.',
            'key_findings': [
                'Machine learning predicts drug response from tumor genomics',
                'AI identifies optimal chemotherapy combinations',
                'Patient stratification improves clinical trial efficiency'
            ]
        },
        {
            'topic_name': 'Clinical Trials',
            'overview': 'AI transforms patient recruitment and trial design.',
            'key_findings': [
                'NLP extracts eligibility criteria from medical records',
                'Predictive models match patients to appropriate trials',
                'Adaptive trial designs optimize treatment protocols'
            ]
        }
    ]
    
    print("📊 Building comprehensive knowledge graph...")
    print()
    
    # Build graph
    builder = KnowledgeGraphBuilder()
    graph_data = builder.build_from_newsletter(exec_summary, topic_summaries)
    
    # Statistics
    print(f"📈 Knowledge Graph Statistics:")
    print(f"   Terms Extracted: {graph_data['total_terms']}")
    print(f"   Relationships: {graph_data['total_relationships']}")
    print(f"   Avg Connections per Term: "
          f"{graph_data['total_relationships'] / max(graph_data['total_terms'], 1):.1f}")
    print()
    
    # Top keywords with detailed scores
    print("🔑 Top 15 Keywords (Ranked by Importance):")
    for i, kw in enumerate(graph_data['top_keywords'][:15], 1):
        bar_length = int(kw['score'] * 20)
        bar = "█" * bar_length
        print(f"   {i:2}. {kw['term'].title():30} {bar:20} {kw['score']:.3f}")
    print()
    
    # High centrality terms
    print("🎯 High Centrality Terms (Most Influential):")
    for i, (term, score) in enumerate(graph_data['high_centrality_terms'][:12], 1):
        connections = len(builder.graph.get(term, []))
        bar_length = int(score * 20)
        bar = "●" * bar_length
        print(f"   {i:2}. {term.title():30} {bar:20} "
              f"Centrality: {score:.3f} ({connections} connections)")
    print()
    
    # Term categories
    viz_data = builder.visualize_graph_data()
    categories = {}
    for node in viz_data['nodes']:
        group = node['group']
        categories[group] = categories.get(group, 0) + 1
    
    print("📂 Term Categories:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {category.replace('_', ' ').title():20} {count:3} terms")


def main():
    """Run all examples."""
    print("\n")
    print("🧠" * 40)
    print("\n  KNOWLEDGE GRAPH & GLOSSARY GENERATOR - Examples\n")
    print("🧠" * 40)
    print("\n")
    
    try:
        # Example 1
        example_1_basic_knowledge_graph()
        input("\n\nPress Enter for Example 2 (AI Glossary)...")
        
        # Example 2
        example_2_generate_glossary()
        input("\n\nPress Enter for Example 3 (Export Graph)...")
        
        # Example 3
        example_3_export_graph()
        input("\n\nPress Enter for Example 4 (Comprehensive Analysis)...")
        
        # Example 4
        example_4_comprehensive()
        
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
        return
    
    # Completion
    print_separator("✅ All Examples Complete!")
    
    print("🎯 What You Can Do Now:")
    print()
    print("1. Extract Keywords")
    print("   → Identify the most important terms in your newsletter")
    print()
    print("2. Build Knowledge Graphs")
    print("   → Visualize relationships between concepts")
    print()
    print("3. Generate Glossaries")
    print("   → Create AI-powered definitions for key terms")
    print()
    print("4. Analyze Term Centrality")
    print("   → Find the most influential concepts")
    print()
    print("5. Export & Visualize")
    print("   → Create interactive visualizations")
    print()
    print("📚 For more info, see: docs/KNOWLEDGE_GRAPH_GUIDE.md")
    print()


if __name__ == "__main__":
    main()

