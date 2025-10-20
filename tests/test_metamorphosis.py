"""
Test script for the refactored LangGraph implementation following metamorphosis pattern.
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

from src.ai_news_langgraph.graph_v2 import AINewsWorkflow
from src.ai_news_langgraph.tools_direct import DirectToolRegistry, DirectToolExecutor


def test_direct_tools():
    """Test direct tool access functionality."""
    print("\n" + "="*60)
    print("Testing Direct Tool Access")
    print("="*60)

    # Initialize registry
    registry = DirectToolRegistry()

    # List available tools
    print("\nAvailable Tools:")
    for category in ["research", "processing", "file_management", "langgraph"]:
        tools = registry.list_tools(category)
        print(f"  {category}: {tools}")

    # Test search tool
    print("\n1. Testing news search tool...")
    result = registry.execute_tool(
        "search_news",
        query="AI cancer diagnosis",
        max_results=3
    )
    print(f"   Success: {result.success}")
    print(f"   Execution time: {result.execution_time:.2f}s")

    # Test achievement extraction
    print("\n2. Testing achievement extraction...")
    sample_text = """
    We successfully achieved a 95% accuracy in cancer detection.
    The team completed the integration of the new AI model.
    Research succeeded in identifying key biomarkers.
    """
    result = registry.execute_tool("extract_achievements", content=sample_text)
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Found {result.output['total_count']} achievements")

    # Test quality evaluation
    print("\n3. Testing review text evaluation...")
    review_text = """
    ## Summary
    This research presents significant findings in AI-powered cancer detection.

    ## Key Findings
    - Improved accuracy by 15%
    - Reduced false positives
    - Faster processing time
    """
    result = registry.execute_tool("evaluate_review_text", text=review_text)
    print(f"   Success: {result.success}")
    if result.success:
        print(f"   Quality score: {result.output['quality_score']:.2f}")
        print(f"   Meets criteria: {result.output['meets_criteria']}")


async def test_workflow_async():
    """Test the async workflow execution."""
    print("\n" + "="*60)
    print("Testing Async Workflow Execution")
    print("="*60)

    # Initialize workflow
    workflow = AINewsWorkflow(
        use_parallel=False,
        checkpoint_type="memory",
        enable_streaming=False
    )

    # Create test topics configuration
    test_config = {
        "main_topic": "AI in Cancer Research - Test",
        "topics": [
            {
                "name": "AI Diagnostics",
                "description": "AI applications in cancer diagnostics",
                "query": "AI cancer diagnosis imaging pathology"
            },
            {
                "name": "Treatment Planning",
                "description": "AI for treatment optimization",
                "query": "AI cancer treatment planning precision medicine"
            }
        ]
    }

    # Save test config
    config_path = "test_config.json"
    with open(config_path, "w") as f:
        json.dump(test_config, f, indent=2)

    print(f"\nRunning workflow with {len(test_config['topics'])} topics...")

    # Run workflow
    result = await workflow.run_async(
        main_topic=test_config["main_topic"],
        topics_path=config_path
    )

    # Display results
    print("\nWorkflow Results:")
    print(f"  Status: {result['status']}")
    print(f"  Thread ID: {result.get('thread_id', 'N/A')}")

    if 'metrics' in result:
        metrics = result['metrics']
        print("\nMetrics:")
        print(f"  Topics processed: {metrics.get('topics_processed', 0)}")
        print(f"  Articles fetched: {metrics.get('total_articles', 0)}")
        print(f"  Success rate: {metrics.get('success_rate', 0):.2%}")
        print(f"  Duration: {metrics.get('duration_seconds', 0):.2f}s")

    if 'outputs' in result:
        print(f"\nOutputs generated:")
        for key, path in result['outputs'].items():
            print(f"  {key}: {path}")

    if 'errors' in result and result['errors']:
        print(f"\nErrors encountered: {len(result['errors'])}")
        for error in result['errors'][:3]:
            print(f"  - {error}")

    # Clean up
    Path(config_path).unlink(missing_ok=True)

    return result


async def test_parallel_workflow():
    """Test parallel topic processing."""
    print("\n" + "="*60)
    print("Testing Parallel Workflow Execution")
    print("="*60)

    # Initialize parallel workflow
    workflow = AINewsWorkflow(
        use_parallel=True,
        checkpoint_type="memory",
        enable_streaming=False
    )

    print("\nTesting parallel execution with 3 topics...")

    # Create config with multiple topics
    test_config = {
        "main_topic": "AI in Oncology - Parallel Test",
        "topics": [
            {
                "name": f"Topic {i}",
                "description": f"Test topic {i}",
                "query": f"AI cancer research topic{i}"
            }
            for i in range(1, 4)
        ]
    }

    config_path = "test_parallel_config.json"
    with open(config_path, "w") as f:
        json.dump(test_config, f, indent=2)

    # Run with timing
    import time
    start_time = time.time()

    result = await workflow.run_async(
        main_topic=test_config["main_topic"],
        topics_path=config_path
    )

    elapsed_time = time.time() - start_time

    print(f"\nParallel execution completed in {elapsed_time:.2f}s")
    print(f"Status: {result['status']}")

    # Clean up
    Path(config_path).unlink(missing_ok=True)


def test_workflow_status():
    """Test workflow status and thread management."""
    print("\n" + "="*60)
    print("Testing Workflow Status & Thread Management")
    print("="*60)

    workflow = AINewsWorkflow()

    # Test with a specific thread ID
    test_thread_id = f"test_thread_{datetime.now().timestamp()}"

    print(f"\nChecking status for thread: {test_thread_id}")
    status = workflow.get_status(test_thread_id)
    print(f"  Status: {status}")

    # List workflows
    print("\nListing all workflows:")
    workflows = workflow.list_workflows()
    print(f"  Found {len(workflows)} workflows")


async def test_tool_executor():
    """Test the DirectToolExecutor with advanced features."""
    print("\n" + "="*60)
    print("Testing DirectToolExecutor")
    print("="*60)

    registry = DirectToolRegistry()
    executor = DirectToolExecutor(registry)

    # Test retry logic
    print("\n1. Testing retry logic...")
    result = await executor.execute_with_retry(
        "search_news",
        max_retries=2,
        query="test query",
        max_results=5
    )
    print(f"   Success: {result.success}")

    # Test parallel execution
    print("\n2. Testing parallel tool execution...")
    tool_calls = [
        {"tool_name": "extract_achievements", "content": "Test achieved success."},
        {"tool_name": "evaluate_review_text", "text": "Test review text."}
    ]

    results = await executor.execute_parallel(tool_calls)
    print(f"   Executed {len(results)} tools in parallel")
    for i, result in enumerate(results):
        print(f"   Tool {i+1}: Success={result.success}")

    # Test caching
    print("\n3. Testing tool caching...")

    # First call (not cached)
    result1 = executor.execute_with_cache(
        "extract_achievements",
        content="Cached test content",
        cache_ttl=60
    )

    # Second call (should be cached)
    result2 = executor.execute_with_cache(
        "extract_achievements",
        content="Cached test content",
        cache_ttl=60
    )

    print(f"   First call time: {result1.execution_time:.4f}s")
    print(f"   Second call time: {result2.execution_time:.4f}s (cached)")


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("METAMORPHOSIS PATTERN IMPLEMENTATION TEST SUITE")
    print("="*60)

    # Test direct tools
    test_direct_tools()

    # Test workflow status
    test_workflow_status()

    # Run async tests
    print("\nRunning async tests...")
    asyncio.run(test_async_suite())


async def test_async_suite():
    """Run all async tests."""
    # Test tool executor
    await test_tool_executor()

    # Test basic workflow
    await test_workflow_async()

    # Test parallel workflow
    await test_parallel_workflow()

    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60)


if __name__ == "__main__":
    main()