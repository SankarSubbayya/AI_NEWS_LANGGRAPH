#!/usr/bin/env python3
"""
Test script for CO-STAR prompts
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Now import from the correct path
from src.ai_news_langgraph.prompts_costar import (
    get_costar_prompt,
    costar_prompt_registry,
    CostarPromptConfig
)


def test_costar_prompts():
    """Test the CO-STAR prompts implementation."""

    print("=" * 60)
    print("CO-STAR PROMPTS TEST")
    print("=" * 60)

    # 1. List all available prompts
    print("\n📋 Available CO-STAR Prompts:")
    prompts = costar_prompt_registry.list_prompts()
    for agent, prompt_list in prompts.items():
        print(f"\n  {agent}:")
        for prompt in prompt_list:
            print(f"    - {prompt}")

    # 2. Get a specific prompt configuration
    print("\n" + "=" * 60)
    print("📝 Example: Research Agent - Analyze Relevance")
    print("=" * 60)

    config = costar_prompt_registry.get_prompt_config("research_agent", "analyze_relevance")

    print(f"\n📌 CONTEXT (first 200 chars):")
    print(f"{config.context[:200]}...")

    print(f"\n🎯 OBJECTIVE (first 150 chars):")
    print(f"{config.objective[:150]}...")

    print(f"\n✍️ STYLE:")
    print(f"{config.style}")

    print(f"\n🎭 TONE:")
    print(f"{config.tone}")

    print(f"\n👥 AUDIENCE:")
    print(f"{config.audience}")

    print(f"\n📊 RESPONSE FORMAT (first 200 chars):")
    print(f"{config.response_format[:200]}...")

    print(f"\n🔧 Variables required: {', '.join(config.variables)}")

    # 3. Get compiled prompt
    print("\n" + "=" * 60)
    print("🔨 Compiled Prompt Template")
    print("=" * 60)

    prompt = get_costar_prompt("research_agent", "analyze_relevance")
    print(f"\nPrompt type: {type(prompt)}")
    print(f"Input variables: {prompt.input_variables}")

    # 4. Example usage
    print("\n" + "=" * 60)
    print("💡 Example Usage")
    print("=" * 60)

    print("""
# In your code:
from src.ai_news_langgraph.prompts_costar import get_costar_prompt

# Get the prompt
prompt = get_costar_prompt("research_agent", "analyze_relevance")

# Use with LangChain
chain = prompt | llm | output_parser

# Invoke with variables
result = await chain.ainvoke({
    "topic_name": "AI Diagnostics",
    "topic_description": "AI applications in cancer diagnostics",
    "title": "New AI Model Detects Cancer Earlier",
    "content": "Researchers developed an AI system..."
})
""")

    # 5. Show all agents and their prompts
    print("\n" + "=" * 60)
    print("📚 All CO-STAR Prompts by Agent")
    print("=" * 60)

    agents_info = {
        "research_agent": "AI Research Analyst - evaluates articles",
        "editor_agent": "Senior Medical Editor - creates summaries",
        "chief_editor": "Chief Editor - refines content",
        "self_reviewer": "Quality Assurance - evaluates quality"
    }

    for agent, description in agents_info.items():
        print(f"\n🤖 {agent}")
        print(f"   {description}")
        if agent in prompts:
            for prompt in prompts[agent]:
                config = costar_prompt_registry.get_prompt_config(agent, prompt)
                print(f"   • {prompt}: {config.description}")


def compare_prompts():
    """Compare original vs CO-STAR prompts."""

    print("\n" + "=" * 60)
    print("📊 COMPARISON: Original vs CO-STAR")
    print("=" * 60)

    print("\n❌ ORIGINAL PROMPT (simple):")
    print("-" * 40)
    print("""
Score this article's relevance to the topic (0-1):
Topic: {topic_name} - {topic_desc}
Article: {title}
Summary: {content}

Return only a number between 0 and 1.
""")

    print("\n✅ CO-STAR PROMPT (structured):")
    print("-" * 40)

    config = costar_prompt_registry.get_prompt_config("research_agent", "analyze_relevance")

    print(f"""
CONTEXT:
{config.context[:150]}...

OBJECTIVE:
{config.objective[:150]}...

STYLE: {config.style[:50]}...

TONE: {config.tone}

AUDIENCE: {config.audience}

RESPONSE FORMAT:
{config.response_format[:150]}...
""")

    print("\n💡 Key Improvements:")
    print("  ✓ Clear role and expertise established")
    print("  ✓ Specific scoring criteria with weights")
    print("  ✓ Defined audience and purpose")
    print("  ✓ Consistent structure across all prompts")
    print("  ✓ Better context for more accurate responses")


def main():
    """Run all tests."""
    test_costar_prompts()
    compare_prompts()

    print("\n" + "=" * 60)
    print("✅ CO-STAR Prompts Test Complete!")
    print("=" * 60)
    print("\nTo use in your project:")
    print("1. Import: from src.ai_news_langgraph.prompts_costar import get_costar_prompt")
    print("2. Get prompt: prompt = get_costar_prompt('agent_name', 'prompt_name')")
    print("3. Use with LLM: chain = prompt | llm | parser")


if __name__ == "__main__":
    main()