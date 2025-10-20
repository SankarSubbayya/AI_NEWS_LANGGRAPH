#!/usr/bin/env python3
"""
Test script for new features:
1. Cancer-specific news sources
2. Agent constructor YAML files
3. Enhanced CO-STAR prompts with few-shot examples
4. Alternative news APIs
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import yaml
from typing import Dict, Any


def test_cancer_news_sources():
    """Test cancer-specific news sources integration."""
    print("\n" + "="*80)
    print("TEST 1: Cancer-Specific News Sources")
    print("="*80)

    try:
        from src.ai_news_langgraph.tools_cancer_news import CancerNewsAPI

        api = CancerNewsAPI()
        print(f"✅ CancerNewsAPI initialized with {len(api.sources)} sources")

        # List sources
        print("\nAvailable sources:")
        for source_id, source_info in api.sources.items():
            print(f"  - {source_info['name']} ({source_info['type']})")

        # Test search (limited results for testing)
        print("\n🔍 Testing search functionality...")
        try:
            results = api.search_all_sources(
                query="AI artificial intelligence cancer",
                max_results_per_source=2,
                days_back=30
            )
            print(f"✅ Search completed: {len(results)} articles found")

            if results:
                print("\nSample article:")
                article = results[0]
                print(f"  Title: {article['title'][:80]}...")
                print(f"  Source: {article['source']}")
                print(f"  URL: {article['url'][:60]}...")
                print(f"  Score: {article['score']}")

        except Exception as e:
            print(f"⚠️  Search test skipped (requires internet): {e}")

        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_configs():
    """Test agent constructor YAML files."""
    print("\n" + "="*80)
    print("TEST 2: Agent Constructor YAML Files")
    print("="*80)

    agents = [
        'research_assistant',
        'editor_assistant',
        'chief_editor',
        'self_reviewer'
    ]

    all_passed = True

    for agent_id in agents:
        try:
            config_path = Path(f"src/ai_news_langgraph/config/agents/{agent_id}.yaml")

            if not config_path.exists():
                print(f"❌ {agent_id}: Config file not found at {config_path}")
                all_passed = False
                continue

            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)

            # Validate required fields
            required_fields = ['agent_id', 'role', 'goal', 'backstory', 'model', 'temperature']
            missing = [field for field in required_fields if field not in config]

            if missing:
                print(f"❌ {agent_id}: Missing fields: {missing}")
                all_passed = False
                continue

            print(f"\n✅ {agent_id}")
            print(f"   Role: {config['role'][:70]}...")
            print(f"   Model: {config['model']}, Temp: {config['temperature']}")

            if 'tools' in config:
                print(f"   Tools: {', '.join(config['tools'][:3])}")

            # Check for detailed configuration sections
            special_sections = {
                'research_assistant': ['search_config', 'output_format'],
                'editor_assistant': ['analysis_config', 'quality_criteria'],
                'chief_editor': ['design_config', 'newsletter_structure'],
                'self_reviewer': ['review_criteria', 'quality_metrics']
            }

            if agent_id in special_sections:
                for section in special_sections[agent_id]:
                    if section in config:
                        print(f"   ✓ Has {section}")
                    else:
                        print(f"   ⚠️  Missing {section}")

        except Exception as e:
            print(f"❌ {agent_id}: {e}")
            all_passed = False

    return all_passed


def test_enhanced_prompts():
    """Test enhanced CO-STAR prompts with few-shot examples."""
    print("\n" + "="*80)
    print("TEST 3: Enhanced CO-STAR Prompts")
    print("="*80)

    try:
        from src.ai_news_langgraph.prompts_enhanced import (
            enhanced_prompt_registry,
            get_enhanced_prompt
        )

        # Check prompts loaded
        all_prompts = enhanced_prompt_registry.list_prompts()
        print(f"✅ Loaded {len(all_prompts)} prompts")

        # List prompts by agent
        agents = ["research_agent", "editor_agent", "chief_editor", "self_reviewer"]
        for agent in agents:
            agent_prompts = enhanced_prompt_registry.list_prompts(agent)
            print(f"\n{agent}: {len(agent_prompts)} prompts")
            for prompt_name in agent_prompts:
                print(f"  - {prompt_name}")

        # Test prompt rendering
        print("\n🔍 Testing prompt rendering...")

        test_prompt = get_enhanced_prompt(
            agent_name="research_agent",
            prompt_name="analyze_relevance",
            topic_name="Early Detection and Diagnosis",
            topic_description="AI in medical imaging for cancer detection",
            title="Test Article Title",
            content="Test article content about AI in cancer detection...",
            source="Test Source",
            published_date="2024-01-15",
            compact=False
        )

        print(f"✅ Full prompt rendered ({len(test_prompt)} chars)")

        # Check for key components
        components = ["# CONTEXT", "# OBJECTIVE", "# STYLE", "# TONE", "# AUDIENCE", "# RESPONSE FORMAT"]
        for component in components:
            if component in test_prompt:
                print(f"   ✓ Contains {component}")
            else:
                print(f"   ⚠️  Missing {component}")

        # Check for few-shot examples
        if "Example" in test_prompt or "EXAMPLE" in test_prompt:
            print(f"   ✓ Contains few-shot examples")
        else:
            print(f"   ⚠️  Missing few-shot examples")

        # Test compact rendering
        compact_prompt = get_enhanced_prompt(
            agent_name="research_agent",
            prompt_name="analyze_relevance",
            topic_name="Test Topic",
            topic_description="Test description",
            title="Test title",
            content="Test content",
            source="Test source",
            published_date="2024-01-15",
            compact=True
        )

        print(f"✅ Compact prompt rendered ({len(compact_prompt)} chars)")
        print(f"   Reduction: {100 * (1 - len(compact_prompt)/len(test_prompt)):.1f}%")

        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tools_integration():
    """Test integration of cancer sources into main tools."""
    print("\n" + "="*80)
    print("TEST 4: Tools Integration")
    print("="*80)

    try:
        from src.ai_news_langgraph.tools import NewsSearchTool

        tool = NewsSearchTool()
        print("✅ NewsSearchTool initialized")

        # Check cancer news integration
        if hasattr(tool, 'cancer_news') and tool.cancer_news:
            print("✅ Cancer news sources integrated")
        else:
            print("⚠️  Cancer news sources not available")

        # Check configuration
        if hasattr(tool, 'use_cancer_sources'):
            print(f"   use_cancer_sources: {tool.use_cancer_sources}")

        if hasattr(tool, 'tavily_client'):
            has_tavily = tool.tavily_client is not None
            print(f"   Tavily API: {'available' if has_tavily else 'not configured'}")

        if hasattr(tool, 'serper_api_key'):
            has_serper = tool.serper_api_key is not None
            print(f"   Serper API: {'available' if has_serper else 'not configured'}")

        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_yaml_validity():
    """Test YAML files for syntax errors."""
    print("\n" + "="*80)
    print("TEST 5: YAML File Validation")
    print("="*80)

    yaml_files = [
        "src/ai_news_langgraph/config/prompts_costar_enhanced.yaml",
        "src/ai_news_langgraph/config/agents/research_assistant.yaml",
        "src/ai_news_langgraph/config/agents/editor_assistant.yaml",
        "src/ai_news_langgraph/config/agents/chief_editor.yaml",
        "src/ai_news_langgraph/config/agents/self_reviewer.yaml",
    ]

    all_valid = True

    for yaml_file in yaml_files:
        path = Path(yaml_file)
        try:
            if not path.exists():
                print(f"⚠️  {path.name}: File not found")
                continue

            with open(path, 'r') as f:
                data = yaml.safe_load(f)

            print(f"✅ {path.name}: Valid YAML ({len(str(data))} chars)")

        except Exception as e:
            print(f"❌ {path.name}: {e}")
            all_valid = False

    return all_valid


def test_complete_workflow():
    """Test that all components work together."""
    print("\n" + "="*80)
    print("TEST 6: Complete Workflow Integration")
    print("="*80)

    try:
        # Import main components
        from src.ai_news_langgraph.tools_cancer_news import CancerNewsAPI
        from src.ai_news_langgraph.prompts_enhanced import get_enhanced_prompt

        # Initialize cancer news
        api = CancerNewsAPI()
        print("✅ Cancer news API initialized")

        # Get enhanced prompt
        prompt = get_enhanced_prompt(
            agent_name="research_agent",
            prompt_name="analyze_relevance",
            topic_name="Test Topic",
            topic_description="Test description",
            title="Test",
            content="Test",
            source="Test",
            published_date="2024-01-15",
            compact=True
        )
        print("✅ Enhanced prompt generated")

        # Load agent config
        with open("src/ai_news_langgraph/config/agents/research_assistant.yaml") as f:
            config = yaml.safe_load(f)
        print("✅ Agent config loaded")

        print("\n✅ All components integrate successfully!")
        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "🧪 " + "="*76)
    print("TESTING NEW FEATURES: Cancer Sources, Agent Configs, Enhanced Prompts")
    print("="*80)

    tests = [
        ("YAML Validation", test_yaml_validity),
        ("Agent Configs", test_agent_configs),
        ("Enhanced Prompts", test_enhanced_prompts),
        ("Tools Integration", test_tools_integration),
        ("Cancer News Sources", test_cancer_news_sources),
        ("Complete Workflow", test_complete_workflow),
    ]

    results = {}

    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    passed = sum(1 for result in results.values() if result)
    total = len(results)

    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")

    print("\n" + "="*80)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*80)

    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
