"""COSTAR Prompt Framework Integration.

CO-STAR Framework Components:
- Context: Background information and expertise
- Objective: Specific task to accomplish
- Style: Writing style and format
- Tone: Emotional quality and professionalism
- Audience: Target readers and expertise level
- Response: Expected output format
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from langchain_core.prompts import ChatPromptTemplate
import logging

logger = logging.getLogger(__name__)


class COSTARPromptLoader:
    """Load and manage COSTAR-framework prompts."""
    
    def __init__(self, prompts_file: str = "prompts_costar.yaml"):
        """Initialize COSTAR prompt loader.
        
        Args:
            prompts_file: Path to COSTAR prompts YAML file (relative to config directory)
        """
        config_dir = Path(__file__).parent / "config"
        self.prompts_file = config_dir / prompts_file
        self._prompts = None
        
    @property
    def prompts(self) -> Dict:
        """Lazy load prompts from YAML file."""
        if self._prompts is None:
            self._prompts = self._load_prompts()
        return self._prompts
    
    def _load_prompts(self) -> Dict:
        """Load COSTAR prompts from YAML file."""
        if not self.prompts_file.exists():
            logger.warning(f"COSTAR prompts file not found: {self.prompts_file}")
            logger.warning("Falling back to standard prompts")
            # Fall back to standard prompts
            standard_file = self.prompts_file.parent / "prompts.yaml"
            if standard_file.exists():
                with open(standard_file, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            return {}
        
        with open(self.prompts_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_prompt(self, agent_name: str, prompt_name: str) -> ChatPromptTemplate:
        """Get a COSTAR-formatted ChatPromptTemplate.
        
        Args:
            agent_name: Name of the agent
            prompt_name: Name of the prompt
            
        Returns:
            ChatPromptTemplate with COSTAR structure
        """
        try:
            agent_prompts = self.prompts[agent_name]
            prompt_config = agent_prompts[prompt_name]
        except KeyError as e:
            logger.error(f"Prompt not found: {agent_name}.{prompt_name}")
            raise KeyError(f"Prompt '{agent_name}.{prompt_name}' not found in COSTAR configuration") from e
        
        # Build COSTAR-structured prompt
        system_message = self._build_costar_system_message(prompt_config)
        human_message = prompt_config.get('objective', '{input}')
        
        return ChatPromptTemplate.from_messages([
            ("system", system_message),
            ("human", human_message)
        ])
    
    def _build_costar_system_message(self, config: Dict[str, Any]) -> str:
        """Build a comprehensive system message using COSTAR framework.
        
        Args:
            config: Prompt configuration dict with COSTAR components
            
        Returns:
            Formatted system message string
        """
        parts = []
        
        # Context
        if 'context' in config:
            parts.append(f"CONTEXT:\n{config['context'].strip()}")
        
        # Objective (included as reference in system message)
        if 'objective' in config and '{' not in config['objective']:
            # Only include if it's not templated
            parts.append(f"OBJECTIVE:\n{config['objective'].strip()}")
        
        # Style
        if 'style' in config:
            parts.append(f"STYLE:\n{config['style'].strip()}")
        
        # Tone
        if 'tone' in config:
            parts.append(f"TONE:\n{config['tone']}")
        
        # Audience
        if 'audience' in config:
            parts.append(f"AUDIENCE:\n{config['audience']}")
        
        # Response format
        if 'response' in config:
            parts.append(f"EXPECTED RESPONSE FORMAT:\n{config['response'].strip()}")
        
        return "\n\n".join(parts)
    
    def get_all_prompts_for_agent(self, agent_name: str) -> Dict[str, ChatPromptTemplate]:
        """Get all prompts for a specific agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Dictionary of prompt names to ChatPromptTemplates
        """
        try:
            agent_prompts = self.prompts[agent_name]
        except KeyError:
            logger.error(f"Agent '{agent_name}' not found in COSTAR prompts")
            return {}
        
        return {
            prompt_name: self.get_prompt(agent_name, prompt_name)
            for prompt_name in agent_prompts.keys()
        }


class EnhancedPromptRegistry:
    """Registry that can use either standard or COSTAR prompts."""
    
    def __init__(self, use_costar: bool = True):
        """Initialize enhanced prompt registry.
        
        Args:
            use_costar: Whether to use COSTAR prompts (default: True)
        """
        self.use_costar = use_costar
        
        if use_costar:
            try:
                self.loader = COSTARPromptLoader()
                logger.info("Using COSTAR prompt framework")
            except Exception as e:
                logger.warning(f"Failed to load COSTAR prompts: {e}")
                logger.info("Falling back to standard prompts")
                from .prompt_loader import PromptLoader
                self.loader = PromptLoader()
                self.use_costar = False
        else:
            from .prompt_loader import PromptLoader
            self.loader = PromptLoader()
            logger.info("Using standard prompts")
    
    def get_prompt(self, agent_name: str, prompt_name: str) -> ChatPromptTemplate:
        """Get prompt from the active loader.
        
        Args:
            agent_name: Name of the agent
            prompt_name: Name of the prompt
            
        Returns:
            ChatPromptTemplate
        """
        if self.use_costar and hasattr(self.loader, 'get_prompt'):
            return self.loader.get_prompt(agent_name, prompt_name)
        else:
            # Standard prompt loader uses get_prompt_template
            return self.loader.get_prompt_template(agent_name, prompt_name)


# Global instance for easy import
prompt_registry = EnhancedPromptRegistry(use_costar=True)


def get_prompt(agent_name: str, prompt_name: str, use_costar: bool = True) -> ChatPromptTemplate:
    """Convenience function to get prompts.
    
    Args:
        agent_name: Name of the agent
        prompt_name: Name of the prompt
        use_costar: Whether to use COSTAR framework
        
    Returns:
        ChatPromptTemplate
    """
    registry = EnhancedPromptRegistry(use_costar=use_costar)
    return registry.get_prompt(agent_name, prompt_name)



