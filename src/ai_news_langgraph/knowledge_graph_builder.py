"""Knowledge Graph Builder for AI Cancer Research Newsletter.

Builds a knowledge graph from newsletter content, extracts key concepts,
identifies high-centrality terms, and generates glossaries.
"""

import logging
from typing import Dict, List, Set, Tuple, Any, Optional
from collections import defaultdict, Counter
import re
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class KnowledgeGraphBuilder:
    """Build and analyze knowledge graphs from newsletter content."""
    
    # Domain-specific terms for cancer research + AI
    DOMAIN_TERMS = {
        # Cancer terms
        'cancer', 'oncology', 'tumor', 'tumour', 'carcinoma', 'malignancy',
        'metastasis', 'chemotherapy', 'radiotherapy', 'immunotherapy',
        'biopsy', 'diagnosis', 'prognosis', 'biomarker', 'genomics',
        'mutation', 'gene', 'protein', 'cell', 'tissue',
        
        # AI/ML terms
        'artificial intelligence', 'machine learning', 'deep learning',
        'neural network', 'algorithm', 'model', 'prediction', 'classification',
        'regression', 'clustering', 'supervised', 'unsupervised',
        'training', 'validation', 'accuracy', 'precision', 'recall',
        
        # Medical AI terms
        'computer vision', 'natural language processing', 'nlp',
        'image analysis', 'diagnostic', 'screening', 'detection',
        'segmentation', 'annotation', 'feature extraction',
        
        # Research terms
        'clinical trial', 'patient', 'treatment', 'therapy', 'outcome',
        'efficacy', 'safety', 'adverse event', 'cohort', 'study',
        'research', 'data', 'analysis', 'statistical', 'significant'
    }
    
    # Stop words to exclude
    STOP_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
        'these', 'those', 'it', 'its', 'they', 'their', 'them'
    }
    
    def __init__(self):
        """Initialize the knowledge graph builder."""
        self.graph = defaultdict(set)  # {term: set of related terms}
        self.term_frequency = Counter()  # {term: count}
        self.term_contexts = defaultdict(list)  # {term: [contexts]}
        self.relationships = defaultdict(list)  # {(term1, term2): [relationship_type]}
    
    def build_from_newsletter(
        self,
        executive_summary: str,
        topic_summaries: List[Dict[str, Any]],
        articles: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build knowledge graph from newsletter content.
        
        Args:
            executive_summary: Newsletter executive summary
            topic_summaries: List of topic summaries
            articles: Optional list of source articles
            
        Returns:
            Dictionary with graph data and statistics
        """
        logger.info("Building knowledge graph from newsletter content...")
        
        # Extract from executive summary
        self._extract_from_text(executive_summary, "Executive Summary")
        
        # Extract from topic summaries
        for topic in topic_summaries:
            topic_name = topic.get('topic_name', 'Unknown')
            
            if 'overview' in topic:
                self._extract_from_text(topic['overview'], f"Topic: {topic_name}")
            
            if 'key_findings' in topic:
                for finding in topic['key_findings']:
                    self._extract_from_text(finding, f"Finding: {topic_name}")
        
        # Extract from articles if provided
        if articles:
            for article in articles:
                if 'summary' in article:
                    self._extract_from_text(
                        article['summary'],
                        f"Article: {article.get('title', 'Unknown')}"
                    )
        
        # Build relationships between terms
        self._build_relationships()
        
        # Calculate centrality
        centrality = self._calculate_centrality()
        
        # Generate results
        result = {
            'total_terms': len(self.term_frequency),
            'total_relationships': sum(len(v) for v in self.graph.values()),
            'top_keywords': self._extract_keywords(top_n=20),
            'high_centrality_terms': centrality[:15],
            'term_frequency': dict(self.term_frequency.most_common(50)),
            'graph': {k: list(v) for k, v in self.graph.items()},
            'relationships': {f"{k[0]}-{k[1]}": v for k, v in self.relationships.items()}
        }
        
        logger.info(f"Knowledge graph built: {result['total_terms']} terms, "
                   f"{result['total_relationships']} relationships")
        
        return result
    
    def _extract_from_text(self, text: str, context: str):
        """Extract terms and concepts from text.
        
        Args:
            text: Text to analyze
            context: Context label for the text
        """
        if not text:
            return
        
        # Normalize text
        text_lower = text.lower()
        
        # Extract multi-word terms first (2-3 words)
        for term_length in [3, 2]:
            self._extract_ngrams(text_lower, term_length, context)
        
        # Extract single words
        words = re.findall(r'\b[a-z]{3,}\b', text_lower)
        for word in words:
            if word not in self.STOP_WORDS and len(word) >= 3:
                self.term_frequency[word] += 1
                self.term_contexts[word].append(context)
    
    def _extract_ngrams(self, text: str, n: int, context: str):
        """Extract n-grams (multi-word terms).
        
        Args:
            text: Text to analyze
            n: Number of words per term
            context: Context label
        """
        words = re.findall(r'\b[a-z]+\b', text)
        
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            
            # Check if it's a domain term or contains domain terms
            if (ngram in self.DOMAIN_TERMS or 
                any(term in ngram for term in self.DOMAIN_TERMS)):
                self.term_frequency[ngram] += 1
                self.term_contexts[ngram].append(context)
    
    def _build_relationships(self):
        """Build relationships between co-occurring terms."""
        # For each context, connect terms that appear together
        context_terms = defaultdict(set)
        
        for term, contexts in self.term_contexts.items():
            for context in contexts:
                context_terms[context].add(term)
        
        # Build co-occurrence graph
        for context, terms in context_terms.items():
            terms_list = list(terms)
            for i, term1 in enumerate(terms_list):
                for term2 in terms_list[i+1:]:
                    # Add bidirectional edges
                    self.graph[term1].add(term2)
                    self.graph[term2].add(term1)
                    
                    # Record relationship
                    rel_key = tuple(sorted([term1, term2]))
                    self.relationships[rel_key].append(context)
    
    def _calculate_centrality(self) -> List[Tuple[str, float]]:
        """Calculate centrality (degree centrality) for all terms.
        
        Returns:
            List of (term, centrality_score) tuples, sorted by score
        """
        if not self.graph:
            return []
        
        # Degree centrality = number of connections / (total_nodes - 1)
        total_nodes = len(self.graph)
        
        centrality_scores = {}
        for term, connections in self.graph.items():
            # Weighted by frequency
            degree = len(connections)
            frequency_weight = self.term_frequency.get(term, 1)
            
            # Combined score
            score = (degree / max(total_nodes - 1, 1)) * (1 + 0.1 * frequency_weight)
            centrality_scores[term] = score
        
        # Sort by centrality
        sorted_terms = sorted(
            centrality_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_terms
    
    def _extract_keywords(self, top_n: int = 20) -> List[Dict[str, Any]]:
        """Extract top keywords with scores.
        
        Args:
            top_n: Number of keywords to extract
            
        Returns:
            List of keyword dictionaries
        """
        keywords = []
        
        # Get terms by frequency and centrality
        centrality_dict = dict(self._calculate_centrality())
        
        for term, freq in self.term_frequency.most_common(top_n * 2):
            # Skip very short terms
            if len(term) < 3:
                continue
            
            # Calculate combined score
            centrality = centrality_dict.get(term, 0)
            
            # TF-IDF-like score (simplified)
            tf_score = freq / max(self.term_frequency.most_common(1)[0][1], 1)
            
            # Combined score
            score = tf_score * (1 + centrality)
            
            keywords.append({
                'term': term,
                'frequency': freq,
                'centrality': round(centrality, 4),
                'score': round(score, 4),
                'connections': len(self.graph.get(term, []))
            })
        
        # Sort by score and return top N
        keywords.sort(key=lambda x: x['score'], reverse=True)
        return keywords[:top_n]
    
    def generate_glossary(
        self,
        min_centrality: float = 0.1,
        top_n: int = 15
    ) -> List[Dict[str, str]]:
        """Generate glossary for high-centrality terms.
        
        Args:
            min_centrality: Minimum centrality score to include
            top_n: Maximum number of terms to include
            
        Returns:
            List of glossary entries (term + definition stub)
        """
        logger.info(f"Generating glossary for top {top_n} high-centrality terms...")
        
        # Get high centrality terms
        centrality = self._calculate_centrality()
        
        glossary = []
        for term, score in centrality[:top_n]:
            if score >= min_centrality:
                # Get contexts where term appears
                contexts = self.term_contexts.get(term, [])
                
                # Get related terms
                related = list(self.graph.get(term, []))[:5]
                
                glossary.append({
                    'term': term.title(),
                    'term_lower': term,
                    'centrality': round(score, 4),
                    'frequency': self.term_frequency.get(term, 0),
                    'related_terms': [r.title() for r in related],
                    'contexts': list(set(contexts))[:3],
                    'definition_needed': True  # Flag for LLM to generate
                })
        
        return glossary
    
    def export_graph_json(self, filepath: str):
        """Export knowledge graph to JSON file.
        
        Args:
            filepath: Output file path
        """
        export_data = {
            'metadata': {
                'created': datetime.now().isoformat(),
                'total_terms': len(self.term_frequency),
                'total_relationships': sum(len(v) for v in self.graph.values())
            },
            'terms': {
                term: {
                    'frequency': freq,
                    'contexts': self.term_contexts[term],
                    'connections': list(self.graph.get(term, []))
                }
                for term, freq in self.term_frequency.items()
            },
            'relationships': {
                f"{k[0]}-{k[1]}": v 
                for k, v in self.relationships.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Knowledge graph exported to: {filepath}")
    
    def visualize_graph_data(self) -> Dict[str, Any]:
        """Generate data for graph visualization (e.g., D3.js, NetworkX).
        
        Returns:
            Dictionary with nodes and edges for visualization
        """
        # Get centrality for node sizing
        centrality = dict(self._calculate_centrality())
        
        # Create nodes
        nodes = []
        for term, freq in self.term_frequency.items():
            nodes.append({
                'id': term,
                'label': term.title(),
                'frequency': freq,
                'centrality': centrality.get(term, 0),
                'size': min(freq * 5, 50),  # For visualization
                'group': self._categorize_term(term)
            })
        
        # Create edges
        edges = []
        processed = set()
        for term1, connected in self.graph.items():
            for term2 in connected:
                edge_key = tuple(sorted([term1, term2]))
                if edge_key not in processed:
                    edges.append({
                        'source': term1,
                        'target': term2,
                        'weight': len(self.relationships.get(edge_key, []))
                    })
                    processed.add(edge_key)
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def _categorize_term(self, term: str) -> str:
        """Categorize a term into domain categories.
        
        Args:
            term: Term to categorize
            
        Returns:
            Category name
        """
        term_lower = term.lower()
        
        # Cancer-related
        cancer_keywords = {'cancer', 'tumor', 'oncology', 'malignancy', 'carcinoma'}
        if any(kw in term_lower for kw in cancer_keywords):
            return 'cancer'
        
        # AI/ML-related
        ai_keywords = {'ai', 'artificial', 'machine', 'learning', 'neural', 'algorithm', 'model'}
        if any(kw in term_lower for kw in ai_keywords):
            return 'ai_ml'
        
        # Medical procedure
        medical_keywords = {'diagnosis', 'treatment', 'therapy', 'biopsy', 'screening'}
        if any(kw in term_lower for kw in medical_keywords):
            return 'medical'
        
        # Research
        research_keywords = {'research', 'study', 'trial', 'clinical', 'data', 'analysis'}
        if any(kw in term_lower for kw in research_keywords):
            return 'research'
        
        return 'other'


def build_knowledge_graph_from_newsletter(
    executive_summary: str,
    topic_summaries: List[Dict[str, Any]],
    articles: List[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Convenience function to build knowledge graph.
    
    Args:
        executive_summary: Newsletter executive summary
        topic_summaries: List of topic summaries
        articles: Optional list of articles
        
    Returns:
        Knowledge graph data
    """
    builder = KnowledgeGraphBuilder()
    return builder.build_from_newsletter(
        executive_summary,
        topic_summaries,
        articles
    )


# Example usage
if __name__ == "__main__":
    # Example newsletter content
    exec_summary = """
    This week, we spotlight the groundbreaking integration of artificial intelligence
    in clinical trial design and patient matching. Machine learning algorithms are
    revolutionizing oncology research by analyzing genomic data and predicting
    treatment outcomes with unprecedented accuracy.
    """
    
    topic_summaries = [
        {
            'topic_name': 'Cancer Research',
            'overview': 'AI-powered diagnostic tools are improving early cancer detection rates.',
            'key_findings': [
                'Deep learning models achieve 95% accuracy in tumor classification',
                'Computer vision systems detect malignancies in medical imaging'
            ]
        },
        {
            'topic_name': 'Treatment Planning',
            'overview': 'Personalized therapy recommendations using machine learning.',
            'key_findings': [
                'AI systems analyze patient genomics for treatment optimization',
                'Predictive models improve chemotherapy response rates'
            ]
        }
    ]
    
    # Build knowledge graph
    builder = KnowledgeGraphBuilder()
    graph_data = builder.build_from_newsletter(exec_summary, topic_summaries)
    
    print("=" * 80)
    print("KNOWLEDGE GRAPH ANALYSIS")
    print("=" * 80)
    print(f"\nTotal Terms: {graph_data['total_terms']}")
    print(f"Total Relationships: {graph_data['total_relationships']}")
    
    print("\n" + "=" * 80)
    print("TOP KEYWORDS")
    print("=" * 80)
    for i, kw in enumerate(graph_data['top_keywords'][:10], 1):
        print(f"{i}. {kw['term'].title():30} | "
              f"Freq: {kw['frequency']:3} | "
              f"Centrality: {kw['centrality']:.3f} | "
              f"Connections: {kw['connections']}")
    
    print("\n" + "=" * 80)
    print("HIGH CENTRALITY TERMS")
    print("=" * 80)
    for i, (term, score) in enumerate(graph_data['high_centrality_terms'][:10], 1):
        connections = len(builder.graph.get(term, []))
        print(f"{i}. {term.title():30} | Score: {score:.3f} | Connections: {connections}")
    
    print("\n" + "=" * 80)
    print("GLOSSARY")
    print("=" * 80)
    glossary = builder.generate_glossary(top_n=10)
    for i, entry in enumerate(glossary, 1):
        print(f"\n{i}. {entry['term']}")
        print(f"   Centrality: {entry['centrality']:.3f} | Frequency: {entry['frequency']}")
        print(f"   Related: {', '.join(entry['related_terms'][:3])}")
    
    print("\n" + "=" * 80)
    print("Done!")

