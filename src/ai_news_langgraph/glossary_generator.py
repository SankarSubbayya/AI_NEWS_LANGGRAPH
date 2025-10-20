"""AI-Powered Glossary Generator for Newsletter Terms.

Automatically generates definitions for high-centrality terms using LLM.
"""

import logging
import os
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from .knowledge_graph_builder import KnowledgeGraphBuilder

logger = logging.getLogger(__name__)


class GlossaryGenerator:
    """Generate glossaries with AI-powered definitions."""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.3):
        """Initialize the glossary generator.
        
        Args:
            model: OpenAI model to use
            temperature: Creativity level (0-1)
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def generate_from_knowledge_graph(
        self,
        kg_builder: KnowledgeGraphBuilder,
        min_centrality: float = 0.1,
        top_n: int = 15,
        context: str = "AI in Cancer Care"
    ) -> List[Dict[str, Any]]:
        """Generate glossary from knowledge graph.
        
        Args:
            kg_builder: Knowledge graph builder instance
            min_centrality: Minimum centrality score
            top_n: Maximum number of terms
            context: Domain context for definitions
            
        Returns:
            List of glossary entries with definitions
        """
        logger.info(f"Generating glossary for top {top_n} terms...")
        
        # Get high-centrality terms
        glossary_stubs = kg_builder.generate_glossary(min_centrality, top_n)
        
        # Generate definitions
        glossary = []
        for stub in glossary_stubs:
            try:
                definition = self._generate_definition(
                    term=stub['term'],
                    related_terms=stub['related_terms'],
                    context=context,
                    frequency=stub['frequency']
                )
                
                glossary.append({
                    'term': stub['term'],
                    'definition': definition,
                    'related_terms': stub['related_terms'],
                    'centrality': stub['centrality'],
                    'frequency': stub['frequency'],
                    'importance': self._calculate_importance(stub)
                })
                
            except Exception as e:
                logger.error(f"Failed to generate definition for '{stub['term']}': {e}")
                glossary.append({
                    'term': stub['term'],
                    'definition': f"[Definition pending for: {stub['term']}]",
                    'related_terms': stub['related_terms'],
                    'centrality': stub['centrality'],
                    'frequency': stub['frequency'],
                    'importance': 'medium'
                })
        
        logger.info(f"Glossary generated with {len(glossary)} terms")
        return glossary
    
    def _generate_definition(
        self,
        term: str,
        related_terms: List[str],
        context: str,
        frequency: int
    ) -> str:
        """Generate definition for a term using LLM.
        
        Args:
            term: Term to define
            related_terms: Related terms from knowledge graph
            context: Domain context
            frequency: Term frequency in content
            
        Returns:
            Generated definition
        """
        system_message = f"""You are a medical and AI terminology expert creating a glossary 
for a newsletter about {context}. 

Generate clear, concise definitions that:
1. Explain the term in the context of cancer research and AI
2. Are 1-2 sentences long
3. Are accessible to healthcare professionals and researchers
4. Focus on practical applications and relevance
5. Don't repeat the term in the definition"""

        related_str = ", ".join(related_terms[:3]) if related_terms else "none"
        
        human_message = f"""Define the term: "{term}"

Related terms in this newsletter: {related_str}
Context: {context}
Term frequency in content: {frequency}

Provide a clear, concise definition (1-2 sentences):"""

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
        ]
        
        response = self.llm.invoke(messages)
        definition = response.content.strip()
        
        return definition
    
    def _calculate_importance(self, stub: Dict[str, Any]) -> str:
        """Calculate importance level based on centrality and frequency.
        
        Args:
            stub: Glossary stub with metrics
            
        Returns:
            Importance level (high, medium, low)
        """
        centrality = stub['centrality']
        frequency = stub['frequency']
        
        # Combined score
        score = centrality * 0.7 + (frequency / 100) * 0.3
        
        if score > 0.5:
            return 'high'
        elif score > 0.2:
            return 'medium'
        else:
            return 'low'
    
    def format_glossary_html(self, glossary: List[Dict[str, Any]]) -> str:
        """Format glossary as HTML for newsletter.
        
        Args:
            glossary: List of glossary entries
            
        Returns:
            HTML formatted glossary
        """
        # Sort by importance and term
        glossary_sorted = sorted(
            glossary,
            key=lambda x: (
                {'high': 0, 'medium': 1, 'low': 2}.get(x['importance'], 3),
                x['term']
            )
        )
        
        html = """
        <div class="glossary-section" style="
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 30px;
            border-radius: 10px;
            margin: 30px 0;
        ">
            <h2 style="
                color: #2d3748;
                font-size: 28px;
                margin-bottom: 20px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            ">
                📚 Key Terms Glossary
            </h2>
            <p style="
                color: #4a5568;
                font-size: 14px;
                margin-bottom: 25px;
                font-style: italic;
            ">
                Important terms from this newsletter, ranked by relevance and usage
            </p>
            <div class="glossary-entries">
        """
        
        for entry in glossary_sorted:
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
            related_str = ", ".join(entry['related_terms'][:3])
            
            html += f"""
            <div class="glossary-entry" style="
                background: white;
                padding: 20px;
                margin-bottom: 15px;
                border-radius: 8px;
                border-left: 4px solid {color};
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <h3 style="
                        color: #2d3748;
                        font-size: 20px;
                        margin: 0 0 10px 0;
                        font-weight: 600;
                    ">
                        {entry['term']}
                    </h3>
                    <span style="
                        background: {color};
                        color: white;
                        padding: 4px 12px;
                        border-radius: 12px;
                        font-size: 11px;
                        font-weight: 600;
                        text-transform: uppercase;
                        white-space: nowrap;
                    ">
                        {label}
                    </span>
                </div>
                <p style="
                    color: #4a5568;
                    font-size: 15px;
                    line-height: 1.6;
                    margin: 10px 0;
                ">
                    {entry['definition']}
                </p>
            """
            
            if related_str:
                html += f"""
                <div style="
                    margin-top: 12px;
                    padding-top: 12px;
                    border-top: 1px solid #e2e8f0;
                ">
                    <span style="
                        color: #718096;
                        font-size: 13px;
                        font-weight: 600;
                    ">
                        Related: 
                    </span>
                    <span style="
                        color: #4a5568;
                        font-size: 13px;
                    ">
                        {related_str}
                    </span>
                </div>
                """
            
            html += """
            </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def format_glossary_markdown(self, glossary: List[Dict[str, Any]]) -> str:
        """Format glossary as Markdown.
        
        Args:
            glossary: List of glossary entries
            
        Returns:
            Markdown formatted glossary
        """
        # Sort by importance
        glossary_sorted = sorted(
            glossary,
            key=lambda x: (
                {'high': 0, 'medium': 1, 'low': 2}.get(x['importance'], 3),
                x['term']
            )
        )
        
        md = "# 📚 Key Terms Glossary\n\n"
        md += "_Important terms from this newsletter, ranked by relevance and usage_\n\n"
        md += "---\n\n"
        
        current_importance = None
        for entry in glossary_sorted:
            # Add section header when importance changes
            if entry['importance'] != current_importance:
                current_importance = entry['importance']
                section_titles = {
                    'high': '## ⭐ High Priority Terms',
                    'medium': '## ✓ Important Terms',
                    'low': '## 📖 Reference Terms'
                }
                md += f"\n{section_titles.get(current_importance, '## Terms')}\n\n"
            
            # Add term entry
            md += f"### {entry['term']}\n\n"
            md += f"{entry['definition']}\n\n"
            
            if entry['related_terms']:
                related_str = ", ".join(entry['related_terms'][:3])
                md += f"**Related terms**: {related_str}\n\n"
            
            md += "---\n\n"
        
        return md


def generate_glossary_for_newsletter(
    executive_summary: str,
    topic_summaries: List[Dict[str, Any]],
    articles: List[Dict[str, Any]] = None,
    top_n: int = 15,
    output_format: str = "both"
) -> Dict[str, Any]:
    """Generate glossary for newsletter (convenience function).
    
    Args:
        executive_summary: Newsletter summary
        topic_summaries: List of topic summaries
        articles: Optional article list
        top_n: Number of terms to include
        output_format: "html", "markdown", or "both"
        
    Returns:
        Dictionary with glossary data and formatted output
    """
    # Build knowledge graph
    kg_builder = KnowledgeGraphBuilder()
    kg_builder.build_from_newsletter(
        executive_summary,
        topic_summaries,
        articles
    )
    
    # Generate glossary
    glossary_gen = GlossaryGenerator()
    glossary = glossary_gen.generate_from_knowledge_graph(
        kg_builder,
        top_n=top_n
    )
    
    # Format output
    result = {
        'glossary': glossary,
        'total_terms': len(glossary)
    }
    
    if output_format in ["html", "both"]:
        result['html'] = glossary_gen.format_glossary_html(glossary)
    
    if output_format in ["markdown", "both"]:
        result['markdown'] = glossary_gen.format_glossary_markdown(glossary)
    
    return result


def generate_glossary_from_cancer_kg(
    cancer_kg_data: Dict[str, Any],
    executive_summary: str = "",
    topic_summaries: List[Dict[str, Any]] = None,
    top_n: int = 15,
    output_format: str = "both"
) -> Dict[str, Any]:
    """Generate glossary using pre-built Cancer Research Knowledge Graph data.
    
    Args:
        cancer_kg_data: Output from CancerResearchKnowledgeGraph.build_from_newsletter()
        executive_summary: Newsletter summary (for context)
        topic_summaries: Topic summaries (for context)
        top_n: Number of terms to include
        output_format: "html", "markdown", or "both"
        
    Returns:
        Dictionary with glossary data and formatted output
    """
    from langchain_openai import ChatOpenAI
    
    # Extract top entities from cancer research KG
    # top_entities is a list of tuples: (entity, score, entity_type)
    top_entities = cancer_kg_data.get('top_entities', [])[:top_n]
    
    # Check if API key is available
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.warning("No OpenAI API key found. Returning empty glossary.")
        return {
            'glossary': [],
            'total_terms': 0,
            'html': '<p>⚠️ Glossary generation requires OPENAI_API_KEY</p>',
            'markdown': '⚠️ Glossary generation requires OPENAI_API_KEY'
        }
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    # Generate definitions for each entity
    glossary = []
    for entity, score, entity_type in top_entities:
        try:
            # Create context-aware prompt
            prompt = f"""Define the following medical/AI term in the context of cancer research:

Term: {entity}
Category: {entity_type.replace('_', ' ').title()}

Provide a clear, concise definition (2-3 sentences) suitable for a medical newsletter.
Focus on its relevance to cancer research, diagnosis, or treatment.

Definition:"""
            
            response = llm.invoke(prompt)
            definition = response.content.strip()
            
            glossary.append({
                'term': entity.title(),
                'definition': definition,
                'category': entity_type.replace('_', ' ').title(),
                'importance': score,
                'priority': 'high' if score > 4 else 'medium'
            })
            
            logger.info(f"Generated definition for: {entity}")
            
        except Exception as e:
            logger.error(f"Error generating definition for {entity}: {e}")
            glossary.append({
                'term': entity.title(),
                'definition': f"A {entity_type.replace('_', ' ')} relevant to cancer research.",
                'category': entity_type.replace('_', ' ').title(),
                'importance': score,
                'priority': 'high' if score > 4 else 'medium'
            })
    
    # Format output
    result = {
        'glossary': glossary,
        'total_terms': len(glossary)
    }
    
    if output_format in ["html", "both"]:
        result['html'] = _format_cancer_glossary_html(glossary)
    
    if output_format in ["markdown", "both"]:
        result['markdown'] = _format_cancer_glossary_markdown(glossary)
    
    return result


def _format_cancer_glossary_html(glossary: List[Dict[str, Any]]) -> str:
    """Format cancer research glossary as HTML."""
    html = """
    <!-- Medical Glossary -->
    <div class="section" style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 30px; border-radius: 10px; margin-top: 30px;">
        <h2 style="color: #2d3748; font-size: 28px; margin-bottom: 15px; font-weight: 700;">📖 Medical Glossary</h2>
        <p style="color: #4a5568; font-size: 14px; margin-bottom: 25px; font-style: italic;">
            Key medical and AI terms from this cancer research newsletter
        </p>
"""
    
    for term_data in glossary:
        priority = term_data.get('priority', 'medium')
        color = "#e53e3e" if priority == 'high' else "#ed8936"
        category = term_data.get('category', 'General')
        
        html += f"""
        <div style="background: white; padding: 20px; margin-bottom: 15px; border-radius: 8px; border-left: 4px solid {color};">
            <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">
                <h3 style="color: #2d3748; font-size: 20px; margin: 0; font-weight: 600;">
                    {term_data['term']}
                </h3>
                <span style="background: {color}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">
                    {category}
                </span>
            </div>
            <p style="color: #4a5568; font-size: 15px; line-height: 1.6; margin: 0;">
                {term_data['definition']}
            </p>
        </div>
"""
    
    html += """
    </div>
"""
    return html


def _format_cancer_glossary_markdown(glossary: List[Dict[str, Any]]) -> str:
    """Format cancer research glossary as Markdown."""
    md = "# 📖 Medical Glossary\n\n"
    md += "*Key medical and AI terms from this cancer research newsletter*\n\n"
    md += "---\n\n"
    
    for term_data in glossary:
        category = term_data.get('category', 'General')
        priority = term_data.get('priority', 'medium')
        priority_badge = "⭐ HIGH PRIORITY" if priority == 'high' else "📌 IMPORTANT"
        
        md += f"### {term_data['term']}\n\n"
        md += f"**Category:** {category} | {priority_badge}\n\n"
        md += f"{term_data['definition']}\n\n"
        md += "---\n\n"
    
    return md


# Example usage
if __name__ == "__main__":
    # Example content
    exec_summary = """
    This week, we spotlight the groundbreaking integration of artificial intelligence
    in clinical trial design and patient matching. Machine learning algorithms are
    revolutionizing oncology research by analyzing genomic data and predicting
    treatment outcomes with unprecedented accuracy.
    """
    
    topic_summaries = [
        {
            'topic_name': 'Cancer Research',
            'overview': 'AI-powered diagnostic tools improving early cancer detection.',
            'key_findings': [
                'Deep learning models achieve 95% accuracy in tumor classification',
                'Computer vision systems detect malignancies in medical imaging'
            ]
        }
    ]
    
    print("Generating glossary...")
    result = generate_glossary_for_newsletter(
        executive_summary,
        topic_summaries,
        top_n=10,
        output_format="markdown"
    )
    
    print(f"\n✅ Generated glossary with {result['total_terms']} terms\n")
    print(result['markdown'])

