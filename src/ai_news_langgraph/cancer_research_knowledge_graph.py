"""Cancer Research Domain-Specific Knowledge Graph.

Builds a proper medical/cancer research knowledge graph with:
- Cancer-specific entities (diseases, treatments, biomarkers, genes)
- Medical relationships (treats, diagnoses, causes, prevents)
- Ontology-based structure
- Domain expertise integration
"""

import logging
import re
from typing import Dict, List, Set, Tuple, Any, Optional
from collections import defaultdict
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class CancerResearchKnowledgeGraph:
    """Build domain-specific knowledge graph for cancer research."""
    
    # Cancer Research Ontology
    CANCER_TYPES = {
        'breast cancer', 'lung cancer', 'prostate cancer', 'colorectal cancer',
        'melanoma', 'leukemia', 'lymphoma', 'pancreatic cancer',
        'ovarian cancer', 'brain cancer', 'liver cancer', 'kidney cancer',
        'bladder cancer', 'thyroid cancer', 'gastric cancer', 'esophageal cancer',
        'cervical cancer', 'endometrial cancer', 'glioblastoma', 'neuroblastoma',
        'osteosarcoma', 'sarcoma', 'mesothelioma', 'carcinoma', 'adenocarcinoma',
        'squamous cell carcinoma', 'basal cell carcinoma', 'renal cell carcinoma'
    }
    
    TREATMENTS = {
        'chemotherapy', 'radiotherapy', 'immunotherapy', 'targeted therapy',
        'hormone therapy', 'surgery', 'radiation', 'ablation',
        'stem cell transplant', 'bone marrow transplant', 'car-t therapy',
        'checkpoint inhibitors', 'monoclonal antibodies', 'vaccine therapy',
        'gene therapy', 'photodynamic therapy', 'cryotherapy',
        'pembrolizumab', 'nivolumab', 'atezolizumab', 'durvalumab',
        'trastuzumab', 'bevacizumab', 'cetuximab', 'rituximab',
        'cisplatin', 'carboplatin', 'paclitaxel', 'doxorubicin', 'docetaxel'
    }
    
    BIOMARKERS = {
        'pd-l1', 'her2', 'egfr', 'kras', 'braf', 'brca1', 'brca2',
        'tp53', 'pten', 'alk', 'ros1', 'met', 'ret', 'ntrk',
        'microsatellite instability', 'msi', 'tumor mutational burden', 'tmb',
        'ctdna', 'circulating tumor dna', 'tumor marker', 'cea', 'ca-125',
        'psa', 'afp', 'biomarker', 'genetic marker', 'protein marker'
    }
    
    DIAGNOSTIC_METHODS = {
        'mri', 'ct scan', 'pet scan', 'biopsy', 'liquid biopsy',
        'mammography', 'ultrasound', 'endoscopy', 'colonoscopy',
        'histopathology', 'cytology', 'molecular diagnostics',
        'next generation sequencing', 'ngs', 'whole genome sequencing',
        'rna sequencing', 'gene expression profiling', 'immunohistochemistry',
        'flow cytometry', 'pcr', 'fish', 'imaging', 'screening'
    }
    
    AI_TECHNOLOGIES = {
        'machine learning', 'deep learning', 'artificial intelligence',
        'neural network', 'convolutional neural network', 'cnn',
        'recurrent neural network', 'rnn', 'transformer',
        'computer vision', 'natural language processing', 'nlp',
        'image analysis', 'radiomics', 'pathomics', 'genomics analysis',
        'predictive modeling', 'classification', 'segmentation',
        'object detection', 'feature extraction', 'pattern recognition',
        'decision support system', 'clinical decision support'
    }
    
    RESEARCH_CONCEPTS = {
        'clinical trial', 'phase 1', 'phase 2', 'phase 3', 'phase 4',
        'randomized controlled trial', 'rct', 'cohort study',
        'case control study', 'observational study', 'meta-analysis',
        'systematic review', 'precision medicine', 'personalized medicine',
        'genomics', 'proteomics', 'metabolomics', 'transcriptomics',
        'tumor microenvironment', 'metastasis', 'angiogenesis',
        'apoptosis', 'cell cycle', 'dna repair', 'immune response',
        'tumor suppressor', 'oncogene', 'mutation', 'somatic mutation',
        'germline mutation', 'genetic predisposition', 'risk factor'
    }
    
    # Medical Relationship Types
    RELATIONSHIP_TYPES = {
        'treats': 'treatment_of',
        'diagnoses': 'diagnostic_for',
        'prevents': 'prevention_of',
        'causes': 'causal_factor',
        'increases_risk': 'risk_factor_for',
        'biomarker_for': 'biomarker_of',
        'analyzes': 'analytical_method_for',
        'detects': 'detection_of',
        'predicts': 'predictive_of',
        'monitors': 'monitoring_of',
        'targets': 'therapeutic_target',
        'subtype_of': 'is_subtype_of',
        'stage_of': 'disease_stage',
        'combination_with': 'combined_therapy'
    }
    
    def __init__(self):
        """Initialize cancer research knowledge graph."""
        # Entity storage
        self.entities = defaultdict(set)  # {entity_type: set of entities}
        self.relationships = []  # [(entity1, relation, entity2, context)]
        self.entity_contexts = defaultdict(list)  # {entity: [contexts]}
        
        # Graph structure
        self.graph = defaultdict(lambda: defaultdict(list))  # {entity: {relation: [entities]}}
        
    def build_from_newsletter(
        self,
        executive_summary: str,
        topic_summaries: List[Dict[str, Any]],
        articles: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Build cancer research knowledge graph from newsletter.
        
        Args:
            executive_summary: Newsletter summary
            topic_summaries: Topic summaries
            articles: Optional articles
            
        Returns:
            Knowledge graph data
        """
        logger.info("Building cancer research knowledge graph...")
        
        # Extract entities from all content
        self._extract_entities_from_text(executive_summary, "Executive Summary")
        
        for topic in topic_summaries:
            topic_name = topic.get('topic_name', 'Unknown')
            
            if 'overview' in topic:
                self._extract_entities_from_text(topic['overview'], f"Topic: {topic_name}")
            
            if 'key_findings' in topic:
                for finding in topic['key_findings']:
                    self._extract_entities_from_text(finding, f"Finding: {topic_name}")
        
        if articles:
            for article in articles:
                if 'summary' in article:
                    self._extract_entities_from_text(
                        article['summary'],
                        f"Article: {article.get('title', 'Unknown')}"
                    )
        
        # Build relationships between entities
        self._infer_relationships()
        
        # Calculate entity importance
        importance_scores = self._calculate_entity_importance()
        
        # Generate results
        result = {
            'total_entities': sum(len(entities) for entities in self.entities.values()),
            'total_relationships': len(self.relationships),
            'entities_by_type': {k: list(v) for k, v in self.entities.items()},
            'entity_counts': {k: len(v) for k, v in self.entities.items()},
            'relationships': self._format_relationships(),
            'top_entities': importance_scores[:20],
            'graph_summary': self._generate_summary()
        }
        
        logger.info(f"Knowledge graph built: {result['total_entities']} entities, "
                   f"{result['total_relationships']} relationships")
        
        return result
    
    def _extract_entities_from_text(self, text: str, context: str):
        """Extract cancer research entities from text.
        
        Args:
            text: Text to analyze
            context: Context label
        """
        if not text:
            return
        
        text_lower = text.lower()
        
        # Extract cancer types
        for cancer in self.CANCER_TYPES:
            if cancer in text_lower:
                self.entities['cancer_type'].add(cancer)
                self.entity_contexts[cancer].append(context)
        
        # Extract treatments
        for treatment in self.TREATMENTS:
            if treatment in text_lower:
                self.entities['treatment'].add(treatment)
                self.entity_contexts[treatment].append(context)
        
        # Extract biomarkers
        for biomarker in self.BIOMARKERS:
            if biomarker in text_lower:
                self.entities['biomarker'].add(biomarker)
                self.entity_contexts[biomarker].append(context)
        
        # Extract diagnostic methods
        for diagnostic in self.DIAGNOSTIC_METHODS:
            if diagnostic in text_lower:
                self.entities['diagnostic'].add(diagnostic)
                self.entity_contexts[diagnostic].append(context)
        
        # Extract AI technologies
        for ai_tech in self.AI_TECHNOLOGIES:
            if ai_tech in text_lower:
                self.entities['ai_technology'].add(ai_tech)
                self.entity_contexts[ai_tech].append(context)
        
        # Extract research concepts
        for concept in self.RESEARCH_CONCEPTS:
            if concept in text_lower:
                self.entities['research_concept'].add(concept)
                self.entity_contexts[concept].append(context)
    
    def _infer_relationships(self):
        """Infer medical relationships between entities."""
        # Treatment -> Cancer relationships
        for treatment in self.entities['treatment']:
            for cancer in self.entities['cancer_type']:
                # Check if they co-occur in any context
                treatment_contexts = set(self.entity_contexts[treatment])
                cancer_contexts = set(self.entity_contexts[cancer])
                
                common_contexts = treatment_contexts & cancer_contexts
                if common_contexts:
                    self._add_relationship(
                        treatment, 'treats', cancer,
                        list(common_contexts)[0]
                    )
        
        # Diagnostic -> Cancer relationships
        for diagnostic in self.entities['diagnostic']:
            for cancer in self.entities['cancer_type']:
                diagnostic_contexts = set(self.entity_contexts[diagnostic])
                cancer_contexts = set(self.entity_contexts[cancer])
                
                common_contexts = diagnostic_contexts & cancer_contexts
                if common_contexts:
                    self._add_relationship(
                        diagnostic, 'diagnoses', cancer,
                        list(common_contexts)[0]
                    )
        
        # Biomarker -> Cancer relationships
        for biomarker in self.entities['biomarker']:
            for cancer in self.entities['cancer_type']:
                biomarker_contexts = set(self.entity_contexts[biomarker])
                cancer_contexts = set(self.entity_contexts[cancer])
                
                common_contexts = biomarker_contexts & cancer_contexts
                if common_contexts:
                    self._add_relationship(
                        biomarker, 'biomarker_for', cancer,
                        list(common_contexts)[0]
                    )
        
        # AI Technology -> Diagnostic/Treatment relationships
        for ai_tech in self.entities['ai_technology']:
            for diagnostic in self.entities['diagnostic']:
                ai_contexts = set(self.entity_contexts[ai_tech])
                diag_contexts = set(self.entity_contexts[diagnostic])
                
                common_contexts = ai_contexts & diag_contexts
                if common_contexts:
                    self._add_relationship(
                        ai_tech, 'analyzes', diagnostic,
                        list(common_contexts)[0]
                    )
            
            for cancer in self.entities['cancer_type']:
                ai_contexts = set(self.entity_contexts[ai_tech])
                cancer_contexts = set(self.entity_contexts[cancer])
                
                common_contexts = ai_contexts & cancer_contexts
                if common_contexts:
                    self._add_relationship(
                        ai_tech, 'detects', cancer,
                        list(common_contexts)[0]
                    )
    
    def _add_relationship(
        self,
        entity1: str,
        relation: str,
        entity2: str,
        context: str
    ):
        """Add a relationship to the knowledge graph.
        
        Args:
            entity1: Source entity
            relation: Relationship type
            entity2: Target entity
            context: Context where relationship was found
        """
        self.relationships.append((entity1, relation, entity2, context))
        self.graph[entity1][relation].append(entity2)
    
    def _calculate_entity_importance(self) -> List[Tuple[str, float, str]]:
        """Calculate importance scores for entities.
        
        Returns:
            List of (entity, score, type) tuples sorted by importance
        """
        importance = []
        
        for entity_type, entities in self.entities.items():
            for entity in entities:
                # Base score from frequency
                frequency = len(self.entity_contexts[entity])
                
                # Relationship score
                outgoing = sum(len(v) for v in self.graph[entity].values())
                incoming = sum(
                    1 for e in self.graph.values()
                    for rel_targets in e.values()
                    for target in rel_targets
                    if target == entity
                )
                
                # Combined score
                score = frequency * 0.4 + outgoing * 0.3 + incoming * 0.3
                
                importance.append((entity, score, entity_type))
        
        # Sort by score
        importance.sort(key=lambda x: x[1], reverse=True)
        
        return importance
    
    def _format_relationships(self) -> List[Dict[str, str]]:
        """Format relationships for output.
        
        Returns:
            List of relationship dictionaries
        """
        formatted = []
        
        for entity1, relation, entity2, context in self.relationships:
            formatted.append({
                'source': entity1,
                'relation': relation,
                'target': entity2,
                'context': context,
                'readable': f"{entity1.title()} {relation.replace('_', ' ')} {entity2.title()}"
            })
        
        return formatted
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate a summary of the knowledge graph.
        
        Returns:
            Summary statistics
        """
        return {
            'cancer_types_found': len(self.entities['cancer_type']),
            'treatments_found': len(self.entities['treatment']),
            'biomarkers_found': len(self.entities['biomarker']),
            'diagnostics_found': len(self.entities['diagnostic']),
            'ai_technologies_found': len(self.entities['ai_technology']),
            'research_concepts_found': len(self.entities['research_concept']),
            'relationship_types': len(set(r[1] for r in self.relationships))
        }
    
    def export_to_json(self, filepath: str):
        """Export knowledge graph to JSON.
        
        Args:
            filepath: Output file path
        """
        export_data = {
            'metadata': {
                'created': datetime.now().isoformat(),
                'graph_type': 'cancer_research_knowledge_graph',
                'total_entities': sum(len(entities) for entities in self.entities.values()),
                'total_relationships': len(self.relationships)
            },
            'entities': {k: list(v) for k, v in self.entities.items()},
            'relationships': self._format_relationships(),
            'graph_structure': {
                entity: {
                    relation: targets
                    for relation, targets in relations.items()
                }
                for entity, relations in self.graph.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Knowledge graph exported to: {filepath}")
    
    def visualize_graph_data(self) -> Dict[str, Any]:
        """Generate data for graph visualization.
        
        Returns:
            Nodes and edges for visualization
        """
        # Create nodes
        nodes = []
        for entity_type, entities in self.entities.items():
            for entity in entities:
                frequency = len(self.entity_contexts[entity])
                
                nodes.append({
                    'id': entity,
                    'label': entity.title(),
                    'type': entity_type,
                    'frequency': frequency,
                    'size': min(frequency * 10 + 20, 100)
                })
        
        # Create edges
        edges = []
        for entity1, relation, entity2, context in self.relationships:
            edges.append({
                'source': entity1,
                'target': entity2,
                'relation': relation,
                'label': relation.replace('_', ' '),
                'context': context
            })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def get_entity_details(self, entity: str) -> Dict[str, Any]:
        """Get detailed information about an entity.
        
        Args:
            entity: Entity name
            
        Returns:
            Entity details
        """
        # Find entity type
        entity_type = None
        for etype, entities in self.entities.items():
            if entity in entities:
                entity_type = etype
                break
        
        if not entity_type:
            return None
        
        # Get relationships
        outgoing = []
        for relation, targets in self.graph[entity].items():
            for target in targets:
                outgoing.append({
                    'relation': relation,
                    'target': target
                })
        
        incoming = []
        for source, relations in self.graph.items():
            for relation, targets in relations.items():
                if entity in targets:
                    incoming.append({
                        'source': source,
                        'relation': relation
                    })
        
        return {
            'entity': entity,
            'type': entity_type,
            'frequency': len(self.entity_contexts[entity]),
            'contexts': self.entity_contexts[entity],
            'outgoing_relationships': outgoing,
            'incoming_relationships': incoming,
            'total_connections': len(outgoing) + len(incoming)
        }


# Example usage
if __name__ == "__main__":
    # Example newsletter content
    exec_summary = """
    This week, we spotlight the groundbreaking integration of machine learning
    in breast cancer diagnosis. Deep learning models are analyzing mammography images
    to detect tumors earlier than traditional methods. New immunotherapy treatments
    targeting PD-L1 biomarkers show promising results in clinical trials.
    """
    
    topic_summaries = [
        {
            'topic_name': 'AI Diagnostics',
            'overview': 'Computer vision systems detect lung cancer in CT scans with high accuracy.',
            'key_findings': [
                'CNN models identify melanoma from dermoscopy images',
                'Natural language processing analyzes pathology reports for colorectal cancer'
            ]
        },
        {
            'topic_name': 'Precision Medicine',
            'overview': 'BRCA1 and BRCA2 genetic testing guides treatment for ovarian cancer.',
            'key_findings': [
                'Liquid biopsy detects circulating tumor DNA in pancreatic cancer',
                'Targeted therapy with trastuzumab improves HER2-positive breast cancer outcomes'
            ]
        }
    ]
    
    # Build knowledge graph
    kg = CancerResearchKnowledgeGraph()
    graph_data = kg.build_from_newsletter(exec_summary, topic_summaries)
    
    print("=" * 80)
    print("CANCER RESEARCH KNOWLEDGE GRAPH")
    print("=" * 80)
    print(f"\nTotal Entities: {graph_data['total_entities']}")
    print(f"Total Relationships: {graph_data['total_relationships']}")
    
    print("\n" + "=" * 80)
    print("ENTITIES BY TYPE")
    print("=" * 80)
    for entity_type, count in graph_data['entity_counts'].items():
        print(f"\n{entity_type.replace('_', ' ').title()}: {count}")
        entities = graph_data['entities_by_type'][entity_type][:5]
        for entity in entities:
            print(f"  • {entity.title()}")
    
    print("\n" + "=" * 80)
    print("TOP 15 MOST IMPORTANT ENTITIES")
    print("=" * 80)
    for i, (entity, score, entity_type) in enumerate(graph_data['top_entities'][:15], 1):
        print(f"{i:2}. {entity.title():35} ({entity_type:20}) Score: {score:.2f}")
    
    print("\n" + "=" * 80)
    print("MEDICAL RELATIONSHIPS (Sample)")
    print("=" * 80)
    for i, rel in enumerate(graph_data['relationships'][:10], 1):
        print(f"{i:2}. {rel['readable']}")
        print(f"    Context: {rel['context']}")
    
    print("\n" + "=" * 80)
    print("Done!")

