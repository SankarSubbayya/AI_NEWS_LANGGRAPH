"""Utility for loading prompts from YAML configuration."""

import os
import yaml
from pathlib import Path
from typing import Dict, Optional
from langchain_core.prompts import ChatPromptTemplate
from functools import lru_cache


class PromptLoader:
    """Loads and manages prompt templates from YAML configuration."""
    
    def __init__(self, prompts_file: Optional[str] = None):
        """Initialize prompt loader.
        
        Args:
            prompts_file: Path to prompts YAML file. If None, uses default location.
        """
        if prompts_file is None:
            # Default to prompts.yaml in config directory
            config_dir = Path(__file__).parent / "config"
            prompts_file = config_dir / "prompts.yaml"
        
        self.prompts_file = Path(prompts_file)
        self._prompts = None
    
    @property
    def prompts(self) -> Dict:
        """Lazy load prompts from YAML file."""
        if self._prompts is None:
            self._prompts = self._load_prompts()
        return self._prompts
    
    def _load_prompts(self) -> Dict:
        """Load prompts from YAML file."""
        if not self.prompts_file.exists():
            raise FileNotFoundError(f"Prompts file not found: {self.prompts_file}")
        
        with open(self.prompts_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_prompt_template(
        self,
        agent_name: str,
        prompt_name: str
    ) -> ChatPromptTemplate:
        """Get a ChatPromptTemplate for a specific agent and prompt.
        
        Args:
            agent_name: Name of the agent (e.g., 'research_agent', 'editor_agent')
            prompt_name: Name of the prompt (e.g., 'analyze_relevance', 'summarize_articles')
        
        Returns:
            ChatPromptTemplate ready to use with LangChain
        
        Raises:
            KeyError: If agent or prompt not found in configuration
        
        Example:
            >>> loader = PromptLoader()
            >>> prompt = loader.get_prompt_template('research_agent', 'analyze_relevance')
            >>> chain = prompt | llm
        """
        try:
            agent_prompts = self.prompts[agent_name]
            prompt_config = agent_prompts[prompt_name]
        except KeyError as e:
            available_agents = list(self.prompts.keys())
            if agent_name not in self.prompts:
                raise KeyError(
                    f"Agent '{agent_name}' not found in prompts configuration. "
                    f"Available agents: {available_agents}"
                ) from e
            
            available_prompts = list(self.prompts[agent_name].keys())
            raise KeyError(
                f"Prompt '{prompt_name}' not found for agent '{agent_name}'. "
                f"Available prompts: {available_prompts}"
            ) from e
        
        # Build messages for ChatPromptTemplate
        messages = []
        
        if "system" in prompt_config:
            messages.append(("system", prompt_config["system"]))
        
        if "human" in prompt_config:
            messages.append(("human", prompt_config["human"]))
        
        return ChatPromptTemplate.from_messages(messages)
    
    def get_prompt_description(self, agent_name: str, prompt_name: str) -> str:
        """Get the description of a specific prompt.
        
        Args:
            agent_name: Name of the agent
            prompt_name: Name of the prompt
        
        Returns:
            Description string
        """
        try:
            prompt_config = self.prompts[agent_name][prompt_name]
            return prompt_config.get("description", "No description available")
        except KeyError:
            return "Prompt not found"
    
    def get_prompt_variables(self, agent_name: str, prompt_name: str) -> list:
        """Get list of variables required by a prompt.
        
        Args:
            agent_name: Name of the agent
            prompt_name: Name of the prompt
        
        Returns:
            List of variable names
        """
        try:
            prompt_config = self.prompts[agent_name][prompt_name]
            return prompt_config.get("variables", [])
        except KeyError:
            return []
    
    def list_agents(self) -> list:
        """List all available agents in prompts configuration.
        
        Returns:
            List of agent names
        """
        return list(self.prompts.keys())
    
    def list_prompts(self, agent_name: str) -> list:
        """List all available prompts for a specific agent.
        
        Args:
            agent_name: Name of the agent
        
        Returns:
            List of prompt names
        """
        if agent_name not in self.prompts:
            return []
        return list(self.prompts[agent_name].keys())
    
    def reload(self):
        """Reload prompts from file."""
        self._prompts = None


# Global singleton instance for easy access
_default_loader: Optional[PromptLoader] = None


def get_prompt_loader(prompts_file: Optional[str] = None) -> PromptLoader:
    """Get the default prompt loader instance.
    
    Args:
        prompts_file: Optional path to prompts file. Only used on first call.
    
    Returns:
        PromptLoader instance
    """
    global _default_loader
    if _default_loader is None:
        _default_loader = PromptLoader(prompts_file)
    return _default_loader


def load_prompt(agent_name: str, prompt_name: str) -> ChatPromptTemplate:
    """Convenience function to load a prompt template.
    
    Args:
        agent_name: Name of the agent
        prompt_name: Name of the prompt
    
    Returns:
        ChatPromptTemplate
    
    Example:
        >>> prompt = load_prompt('research_agent', 'analyze_relevance')
        >>> chain = prompt | llm
    """
    loader = get_prompt_loader()
    return loader.get_prompt_template(agent_name, prompt_name)

