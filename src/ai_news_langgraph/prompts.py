"""
Centralized prompt management following metamorphosis pattern.

This module provides structured prompt templates and management
for all agents in the workflow, implementing direct access patterns.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
import yaml
from pathlib import Path


@dataclass
class PromptConfig:
    """Configuration for a prompt template."""
    name: str
    description: str
    system_template: str
    human_template: str
    variables: List[str]
    output_format: Optional[str] = None
    examples: Optional[List[Dict[str, Any]]] = None


class PromptRegistry:
    """
    Centralized registry for all prompt templates.
    Implements the metamorphosis pattern for prompt management.
    """

    def __init__(self):
        """Initialize the prompt registry."""
        self._prompts: Dict[str, Dict[str, PromptConfig]] = {}
        self._compiled_prompts: Dict[str, ChatPromptTemplate] = {}

        # Load default prompts
        self._load_default_prompts()

    def _load_default_prompts(self) -> None:
        """Load and register default prompt templates."""

        # Research Agent Prompts
        self.register_prompt(
            "research_agent",
            "analyze_relevance",
            PromptConfig(
                name="analyze_relevance",
                description="Analyze article relevance to topic",
                system_template="""You are an AI Research Analyst specializing in cancer care and medical AI applications.
Your role is to assess the relevance and quality of articles for inclusion in a specialized newsletter.
You have deep expertise in oncology, AI/ML applications in healthcare, and research methodology.""",
                human_template="""Analyze the relevance of this article to the specified topic.

Topic: {topic_name}
Topic Description: {topic_description}

Article Title: {title}
Article Content: {content}

Scoring Criteria:
1. Direct relevance to the topic (0-0.4 points)
2. Scientific credibility and source quality (0-0.2 points)
3. Recency and timeliness (0-0.2 points)
4. Innovation and impact potential (0-0.2 points)

Provide a relevance score between 0.0 and 1.0.
Output only the numerical score, nothing else.""",
                variables=["topic_name", "topic_description", "title", "content"],
                output_format="float"
            )
        )

        self.register_prompt(
            "research_agent",
            "extract_key_facts",
            PromptConfig(
                name="extract_key_facts",
                description="Extract key facts from article",
                system_template="""You are an expert at analyzing medical and AI research content.
Your task is to extract the most important facts and findings from articles.""",
                human_template="""Extract the key facts from this article:

Title: {title}
Content: {content}

Provide:
1. Main finding or development (1 sentence)
2. Key statistics or metrics (if available)
3. Organizations/researchers involved
4. Potential clinical impact
5. Timeline or next steps

Format as a structured list.""",
                variables=["title", "content"],
                output_format="structured_list"
            )
        )

        # Editor Agent Prompts
        self.register_prompt(
            "editor_agent",
            "summarize_topic",
            PromptConfig(
                name="summarize_topic",
                description="Create comprehensive topic summary",
                system_template="""You are a Senior Medical Editor with expertise in AI applications in oncology.
Your writing is clear, engaging, and accessible to healthcare professionals while maintaining scientific accuracy.
You excel at synthesizing complex information into coherent narratives.""",
                human_template="""Create a comprehensive summary for the following topic and articles.

Topic: {topic_name}
Description: {topic_description}

Articles to summarize:
{articles_json}

Create a summary that includes:

## Overview
Write a 200-250 word overview that captures the main developments and themes across all articles.

## Key Findings
List 3-5 most significant findings or developments as bullet points.

## Notable Trends
Identify 2-3 emerging trends or patterns.

## Clinical Implications
Briefly describe the potential impact on cancer care.

## Recommended Reading
Select the top 3 most important articles with brief explanations why.

Ensure the content is professional, informative, and engaging.""",
                variables=["topic_name", "topic_description", "articles_json"],
                output_format="markdown"
            )
        )

        self.register_prompt(
            "editor_agent",
            "create_executive_summary",
            PromptConfig(
                name="create_executive_summary",
                description="Create newsletter executive summary",
                system_template="""You are the Executive Editor of a premier AI in Cancer Care newsletter.
You have the ability to identify the most impactful developments and communicate them effectively
to an audience of oncologists, researchers, and healthcare executives.""",
                human_template="""Create an executive summary for this week's AI in Cancer Care newsletter.

Topics covered this week:
{topics_summaries}

Write a compelling 250-300 word executive summary that:
1. Opens with the most significant development
2. Highlights cross-cutting themes
3. Emphasizes clinical and research implications
4. Concludes with a forward-looking statement

The tone should be professional yet engaging, suitable for senior healthcare professionals.""",
                variables=["topics_summaries"],
                output_format="text"
            )
        )

        # Chief Editor Agent Prompts
        self.register_prompt(
            "chief_editor",
            "generate_newsletter_html",
            PromptConfig(
                name="generate_newsletter_html",
                description="Generate HTML newsletter",
                system_template="""You are a Digital Content Specialist who creates professional,
mobile-responsive HTML newsletters for medical audiences. You understand both content
presentation and technical implementation.""",
                human_template="""Generate a professional HTML newsletter with the following content:

Executive Summary:
{executive_summary}

Topics and Articles:
{topics_content}

Newsletter Requirements:
- Mobile-responsive design
- Professional medical/scientific aesthetic
- Clear hierarchy and navigation
- Proper citations for all sources
- Include social sharing buttons
- Footer with unsubscribe link

Output clean, valid HTML with inline CSS for email compatibility.""",
                variables=["executive_summary", "topics_content"],
                output_format="html"
            )
        )

        # Self-Reviewer Agent Prompts (Metamorphosis Pattern)
        self.register_prompt(
            "self_reviewer",
            "evaluate_quality",
            PromptConfig(
                name="evaluate_quality",
                description="Evaluate content quality",
                system_template="""You are a Quality Assurance Specialist for medical publications.
Your role is to ensure all content meets the highest standards of accuracy, clarity, and professionalism.
You have expertise in medical writing, fact-checking, and editorial standards.""",
                human_template="""Evaluate the quality of this content:

{content}

Assessment Criteria:
1. Scientific Accuracy (0-25 points)
   - Are claims supported by evidence?
   - Are sources credible and recent?

2. Clarity and Readability (0-25 points)
   - Is the content clear and well-organized?
   - Is technical language appropriately explained?

3. Completeness (0-25 points)
   - Are all key points covered?
   - Is context adequately provided?

4. Professional Presentation (0-25 points)
   - Grammar and style
   - Formatting and structure

Provide:
1. Overall quality score (0-100)
2. Specific feedback for each criterion
3. Recommendations for improvement
4. Red flags or concerns (if any)""",
                variables=["content"],
                output_format="structured_assessment"
            )
        )

        self.register_prompt(
            "self_reviewer",
            "check_consistency",
            PromptConfig(
                name="check_consistency",
                description="Check content consistency",
                system_template="""You are an Editorial Consistency Checker ensuring uniformity across all content.""",
                human_template="""Check this content for consistency issues:

{content}

Review for:
1. Terminology consistency (same terms used throughout)
2. Style consistency (tone, voice, formatting)
3. Data consistency (numbers, dates, statistics match)
4. Reference consistency (proper citations)

Report any inconsistencies found.""",
                variables=["content"],
                output_format="list"
            )
        )

    def register_prompt(
        self,
        agent_name: str,
        prompt_name: str,
        config: PromptConfig
    ) -> None:
        """
        Register a new prompt template.

        Args:
            agent_name: Name of the agent
            prompt_name: Name of the prompt
            config: Prompt configuration
        """
        if agent_name not in self._prompts:
            self._prompts[agent_name] = {}

        self._prompts[agent_name][prompt_name] = config

        # Compile the prompt
        cache_key = f"{agent_name}.{prompt_name}"
        self._compiled_prompts[cache_key] = self._compile_prompt(config)

    def _compile_prompt(self, config: PromptConfig) -> ChatPromptTemplate:
        """Compile a prompt configuration into a ChatPromptTemplate."""
        messages = []

        # Add system message
        if config.system_template:
            messages.append(SystemMessagePromptTemplate.from_template(config.system_template))

        # Add human message
        messages.append(HumanMessagePromptTemplate.from_template(config.human_template))

        return ChatPromptTemplate.from_messages(messages)

    def get_prompt(self, agent_name: str, prompt_name: str) -> ChatPromptTemplate:
        """
        Get a compiled prompt template.

        Args:
            agent_name: Name of the agent
            prompt_name: Name of the prompt

        Returns:
            Compiled ChatPromptTemplate
        """
        cache_key = f"{agent_name}.{prompt_name}"

        if cache_key not in self._compiled_prompts:
            raise ValueError(f"Prompt {cache_key} not found in registry")

        return self._compiled_prompts[cache_key]

    def get_prompt_config(self, agent_name: str, prompt_name: str) -> PromptConfig:
        """
        Get the configuration for a prompt.

        Args:
            agent_name: Name of the agent
            prompt_name: Name of the prompt

        Returns:
            PromptConfig object
        """
        if agent_name not in self._prompts or prompt_name not in self._prompts[agent_name]:
            raise ValueError(f"Prompt config {agent_name}.{prompt_name} not found")

        return self._prompts[agent_name][prompt_name]

    def list_prompts(self, agent_name: Optional[str] = None) -> Dict[str, List[str]]:
        """
        List available prompts.

        Args:
            agent_name: Optional filter by agent name

        Returns:
            Dictionary of agent names to prompt lists
        """
        if agent_name:
            return {agent_name: list(self._prompts.get(agent_name, {}).keys())}

        return {
            agent: list(prompts.keys())
            for agent, prompts in self._prompts.items()
        }

    def load_from_yaml(self, yaml_path: str) -> None:
        """
        Load prompts from a YAML file.

        Args:
            yaml_path: Path to YAML file
        """
        path = Path(yaml_path)
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {yaml_path}")

        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        for agent_name, prompts in data.items():
            if agent_name.startswith('#'):  # Skip comments
                continue

            for prompt_name, prompt_data in prompts.items():
                config = PromptConfig(
                    name=prompt_name,
                    description=prompt_data.get('description', ''),
                    system_template=prompt_data.get('system', ''),
                    human_template=prompt_data.get('human', ''),
                    variables=prompt_data.get('variables', []),
                    output_format=prompt_data.get('output_format'),
                    examples=prompt_data.get('examples')
                )
                self.register_prompt(agent_name, prompt_name, config)


class PromptOptimizer:
    """
    Optimizer for prompt templates following metamorphosis pattern.
    Provides prompt enhancement and testing capabilities.
    """

    def __init__(self, registry: PromptRegistry):
        """
        Initialize the prompt optimizer.

        Args:
            registry: Prompt registry to optimize
        """
        self.registry = registry

    def optimize_prompt(
        self,
        agent_name: str,
        prompt_name: str,
        test_cases: List[Dict[str, Any]]
    ) -> PromptConfig:
        """
        Optimize a prompt based on test cases.

        Args:
            agent_name: Agent name
            prompt_name: Prompt name
            test_cases: Test cases with expected outputs

        Returns:
            Optimized PromptConfig
        """
        config = self.registry.get_prompt_config(agent_name, prompt_name)

        # In a real implementation, this would:
        # 1. Test the prompt with various inputs
        # 2. Measure quality metrics
        # 3. Iteratively improve the prompt
        # 4. Return optimized version

        return config

    def add_few_shot_examples(
        self,
        agent_name: str,
        prompt_name: str,
        examples: List[Dict[str, Any]]
    ) -> None:
        """
        Add few-shot examples to a prompt.

        Args:
            agent_name: Agent name
            prompt_name: Prompt name
            examples: List of example inputs and outputs
        """
        config = self.registry.get_prompt_config(agent_name, prompt_name)
        config.examples = examples

        # Re-register with examples
        self.registry.register_prompt(agent_name, prompt_name, config)


# Global registry instance
prompt_registry = PromptRegistry()

# Convenience function for backward compatibility
def get_prompt(agent_name: str, prompt_name: str) -> ChatPromptTemplate:
    """Get a prompt from the global registry."""
    return prompt_registry.get_prompt(agent_name, prompt_name)