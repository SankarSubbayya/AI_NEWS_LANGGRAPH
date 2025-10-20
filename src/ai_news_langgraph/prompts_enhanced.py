"""
Enhanced CO-STAR prompts with few-shot examples, detailed audience specs,
and comprehensive style guidelines.

This module provides improved prompts that include:
- Detailed agent personas and backgrounds
- Specific audience expertise levels and reading contexts
- Comprehensive style and tone guidelines
- 2-3 few-shot examples per prompt demonstrating desired outputs
- Clear response format specifications
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import yaml
from pathlib import Path


@dataclass
class FewShotExample:
    """A few-shot learning example for a prompt."""
    example_number: int
    input: Dict[str, str]
    output: str
    reasoning: Optional[str] = None


@dataclass
class EnhancedCostarPromptConfig:
    """
    Enhanced CO-STAR prompt configuration with few-shot learning.

    Attributes:
        name: Prompt identifier
        description: Brief description of prompt purpose
        context: Detailed agent persona, background, and expertise
        objective: Specific task with clear success criteria
        style: Writing style, format, and structural requirements
        tone: Emotional quality and professional voice
        audience: Target readers with expertise level and reading context
        response_format: Expected output format with specifications
        few_shot_examples: List of example inputs and outputs
        variables: Template variables to be filled
    """
    name: str
    description: str
    context: str
    objective: str
    style: str
    tone: str
    audience: str
    response_format: str
    variables: List[str]
    few_shot_examples: List[FewShotExample] = field(default_factory=list)

    def render(self, **kwargs) -> str:
        """
        Render the complete prompt with variables filled in.

        Args:
            **kwargs: Variable values to fill into the template

        Returns:
            Fully rendered prompt string
        """
        prompt_parts = []

        # Add context
        prompt_parts.append("# CONTEXT")
        prompt_parts.append(self.context.strip())
        prompt_parts.append("")

        # Add objective with filled variables
        prompt_parts.append("# OBJECTIVE")
        objective_filled = self.objective
        for var, value in kwargs.items():
            objective_filled = objective_filled.replace(f"{{{var}}}", str(value))
        prompt_parts.append(objective_filled.strip())
        prompt_parts.append("")

        # Add few-shot examples if available
        if self.few_shot_examples:
            prompt_parts.append("# EXAMPLES")
            prompt_parts.append("Here are examples of the expected input and output format:")
            prompt_parts.append("")

            for example in self.few_shot_examples:
                prompt_parts.append(f"## Example {example.example_number}")
                prompt_parts.append("**Input:**")
                for key, value in example.input.items():
                    prompt_parts.append(f"  {key}: {value}")
                prompt_parts.append("")
                prompt_parts.append("**Expected Output:**")
                prompt_parts.append(example.output.strip())

                if example.reasoning:
                    prompt_parts.append("")
                    prompt_parts.append("**Reasoning:**")
                    prompt_parts.append(example.reasoning.strip())

                prompt_parts.append("")
                prompt_parts.append("---")
                prompt_parts.append("")

        # Add style guidelines
        prompt_parts.append("# STYLE")
        prompt_parts.append(self.style.strip())
        prompt_parts.append("")

        # Add tone
        prompt_parts.append("# TONE")
        prompt_parts.append(self.tone.strip())
        prompt_parts.append("")

        # Add audience
        prompt_parts.append("# AUDIENCE")
        prompt_parts.append(self.audience.strip())
        prompt_parts.append("")

        # Add response format
        prompt_parts.append("# RESPONSE FORMAT")
        prompt_parts.append(self.response_format.strip())

        return "\n".join(prompt_parts)

    def render_compact(self, **kwargs) -> str:
        """
        Render a more compact version suitable for API calls with token limits.

        Args:
            **kwargs: Variable values to fill into the template

        Returns:
            Compact prompt string
        """
        # Fill objective
        objective_filled = self.objective
        for var, value in kwargs.items():
            objective_filled = objective_filled.replace(f"{{{var}}}", str(value))

        prompt = f"{self.context.strip()}\n\n{objective_filled.strip()}\n\n"

        # Add one example if available
        if self.few_shot_examples:
            example = self.few_shot_examples[0]
            prompt += "Example:\n"
            prompt += f"Input: {example.input}\n"
            prompt += f"Output: {example.output}\n\n"

        prompt += f"{self.response_format.strip()}"

        return prompt


class EnhancedCostarPromptRegistry:
    """Registry for enhanced CO-STAR prompts with few-shot learning."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize the enhanced prompt registry.

        Args:
            config_path: Path to YAML config file (optional)
        """
        self.prompts: Dict[str, EnhancedCostarPromptConfig] = {}

        if config_path and config_path.exists():
            self.load_from_yaml(config_path)
        else:
            self._load_default_prompts()

    def _load_default_prompts(self) -> None:
        """Load enhanced prompts from the default YAML file."""
        default_config = Path(__file__).parent / "config" / "prompts_costar_enhanced.yaml"
        if default_config.exists():
            self.load_from_yaml(default_config)

    def load_from_yaml(self, config_path: Path) -> None:
        """
        Load prompts from a YAML configuration file.

        Args:
            config_path: Path to YAML config file
        """
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Parse each agent's prompts
        for agent_name, agent_prompts in config.items():
            if agent_name == "metadata":  # Skip metadata section
                continue

            for prompt_name, prompt_config in agent_prompts.items():
                if not isinstance(prompt_config, dict):
                    continue

                full_name = f"{agent_name}.{prompt_name}"

                # Parse few-shot examples
                examples = []
                if "few_shot_examples" in prompt_config:
                    for ex_data in prompt_config["few_shot_examples"]:
                        example = FewShotExample(
                            example_number=ex_data.get("example", 1),
                            input=ex_data.get("input", {}),
                            output=ex_data.get("output", ""),
                            reasoning=ex_data.get("reasoning")
                        )
                        examples.append(example)

                # Create enhanced prompt config
                prompt = EnhancedCostarPromptConfig(
                    name=full_name,
                    description=prompt_config.get("description", ""),
                    context=prompt_config.get("context", ""),
                    objective=prompt_config.get("objective", ""),
                    style=prompt_config.get("style", ""),
                    tone=prompt_config.get("tone", ""),
                    audience=prompt_config.get("audience", ""),
                    response_format=prompt_config.get("response_format", ""),
                    variables=prompt_config.get("variables", []),
                    few_shot_examples=examples
                )

                self.prompts[full_name] = prompt

    def get_prompt(
        self,
        agent_name: str,
        prompt_name: str,
        compact: bool = False
    ) -> Optional[EnhancedCostarPromptConfig]:
        """
        Get a prompt by agent and prompt name.

        Args:
            agent_name: Name of the agent (e.g., "research_agent")
            prompt_name: Name of the prompt (e.g., "analyze_relevance")
            compact: Whether to use compact format

        Returns:
            Prompt configuration or None if not found
        """
        full_name = f"{agent_name}.{prompt_name}"
        return self.prompts.get(full_name)

    def render_prompt(
        self,
        agent_name: str,
        prompt_name: str,
        compact: bool = False,
        **kwargs
    ) -> str:
        """
        Render a prompt with variables filled in.

        Args:
            agent_name: Name of the agent
            prompt_name: Name of the prompt
            compact: Whether to use compact format
            **kwargs: Variable values

        Returns:
            Rendered prompt string
        """
        prompt = self.get_prompt(agent_name, prompt_name)
        if not prompt:
            raise ValueError(f"Prompt not found: {agent_name}.{prompt_name}")

        if compact:
            return prompt.render_compact(**kwargs)
        else:
            return prompt.render(**kwargs)

    def list_prompts(self, agent_name: Optional[str] = None) -> List[str]:
        """
        List available prompts, optionally filtered by agent.

        Args:
            agent_name: Optional agent name to filter by

        Returns:
            List of prompt names
        """
        if agent_name:
            prefix = f"{agent_name}."
            return [name for name in self.prompts.keys() if name.startswith(prefix)]
        return list(self.prompts.keys())


# Global registry instance
enhanced_prompt_registry = EnhancedCostarPromptRegistry()


def get_enhanced_prompt(
    agent_name: str,
    prompt_name: str,
    compact: bool = False,
    **kwargs
) -> str:
    """
    Convenience function to get and render a prompt.

    Args:
        agent_name: Name of the agent
        prompt_name: Name of the prompt
        compact: Whether to use compact format
        **kwargs: Variable values

    Returns:
        Rendered prompt string
    """
    return enhanced_prompt_registry.render_prompt(
        agent_name,
        prompt_name,
        compact=compact,
        **kwargs
    )


# Example usage
if __name__ == "__main__":
    # List all prompts
    print("Available prompts:")
    for prompt_name in enhanced_prompt_registry.list_prompts():
        print(f"  - {prompt_name}")

    print("\n" + "="*80 + "\n")

    # Example: Render a research agent prompt
    prompt = get_enhanced_prompt(
        agent_name="research_agent",
        prompt_name="analyze_relevance",
        topic_name="Early Detection and Diagnosis",
        topic_description="AI in medical imaging for cancer detection",
        title="Deep Learning Detects Lung Cancer with 94% Accuracy",
        content="Study of 1,200 patients...",
        source="Nature Medicine",
        published_date="2024-01-15",
        compact=False
    )

    print("Full prompt with few-shot examples:")
    print(prompt)

    print("\n" + "="*80 + "\n")

    # Example: Compact version
    compact_prompt = get_enhanced_prompt(
        agent_name="research_agent",
        prompt_name="analyze_relevance",
        topic_name="Early Detection and Diagnosis",
        topic_description="AI in medical imaging for cancer detection",
        title="Deep Learning Detects Lung Cancer with 94% Accuracy",
        content="Study of 1,200 patients...",
        source="Nature Medicine",
        published_date="2024-01-15",
        compact=True
    )

    print("Compact prompt:")
    print(compact_prompt)
