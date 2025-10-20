"""Main entry point for AI News LangGraph system."""

from __future__ import annotations

import os
import json
import argparse
from typing import Optional
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from .graph_v2 import build_multi_agent_graph

# Load environment variables from .env file
# Try multiple locations for the .env file
def load_env_file():
    """Load .env file from various possible locations."""
    # Current working directory
    if Path(".env").exists():
        load_dotenv(".env")
        print("✅ Loaded .env from current directory")
        return

    # AI_NEWS_LANGGRAPH project root
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded .env from {env_path}")
        return

    # Original ai_news directory (sibling directory)
    ai_news_env = project_root.parent / "ai_news" / ".env"
    if ai_news_env.exists():
        load_dotenv(ai_news_env)
        print(f"✅ Loaded .env from ai_news directory: {ai_news_env}")
        return

    # Look for .env.example as fallback
    env_example = project_root / ".env.example"
    if env_example.exists():
        load_dotenv(env_example)
        print(f"⚠️ Loaded .env.example (please create a .env file)")
        return

    print("⚠️ No .env file found. Using environment variables.")

# Load environment variables on import
load_env_file()


def run_multi_agent():
    """Run the new multi-agent workflow."""
    print("🚀 Starting AI News Multi-Agent Research System...")
    print("=" * 60)

    # Get configuration
    topic = os.getenv("AI_NEWS_TOPIC", "AI in Cancer Care")
    topics_path = os.getenv(
        "AI_NEWS_TOPICS_CONFIG",
        os.path.join(os.path.dirname(__file__), "config/tasks.yaml")
    )
    # Legacy support for AI_NEWS_TOPICS_JSON environment variable
    if not os.path.exists(topics_path):
        topics_path = os.getenv(
            "AI_NEWS_TOPICS_JSON",
            os.path.join(os.path.dirname(__file__), "config/topics_cancer.json")
        )

    print(f"📋 Main Topic: {topic}")
    print(f"📁 Topics Config: {topics_path}")
    print("=" * 60)

    # Build and run the graph
    graph_run = build_multi_agent_graph()
    result = graph_run(topic=topic, topics_json_path=topics_path)

    # Display results
    print("\n✅ Workflow Completed!")
    print("=" * 60)

    if result.get("status") == "completed":
        print("📊 Status: Success")
    else:
        print(f"⚠️ Status: {result.get('status')}")

    # Show outputs
    if result.get("outputs"):
        print("\n📁 Generated Files:")
        for file_type, path in result["outputs"].items():
            print(f"  - {file_type}: {path}")

    # Show agent results
    if result.get("agent_results"):
        print("\n🤖 Agent Performance:")
        for agent_result in result["agent_results"]:
            print(f"  - {agent_result.get('agent_name', 'Unknown')}: {agent_result.get('task_name', 'Unknown')} "
                  f"({agent_result.get('execution_time', 0):.2f}s)")

    # Show errors if any
    if result.get("errors"):
        print("\n❌ Errors Encountered:")
        for error in result["errors"]:
            print(f"  - {error}")

    # Save full results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_path = f"outputs/run_results_{timestamp}.json"
    os.makedirs("outputs", exist_ok=True)

    with open(results_path, "w") as f:
        json.dump(result, f, indent=2, default=str)

    print(f"\n💾 Full results saved to: {results_path}")


def run_simple():
    """Run the original simple workflow (backward compatibility)."""
    print("⚠️  Simple mode is not currently available.")
    print("The 'build_graph' function has not been implemented yet.")
    print("Please use the default multi-agent mode instead:")
    print("  python -m ai_news_langgraph.main --mode multi-agent")
    print("\nOr simply run without any arguments:")
    print("  python -m ai_news_langgraph.main")
    return


def main():
    """Main entry point with CLI arguments."""
    parser = argparse.ArgumentParser(description="AI News LangGraph System")
    parser.add_argument(
        "--mode",
        choices=["multi-agent", "simple"],
        default="multi-agent",
        help="Workflow mode to run (default: multi-agent)"
    )
    parser.add_argument(
        "--topic",
        default=None,
        help="Main research topic (overrides environment variable)"
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to topics configuration JSON file"
    )

    args = parser.parse_args()

    # Override environment variables if CLI args provided
    if args.topic:
        os.environ["AI_NEWS_TOPIC"] = args.topic
    if args.config:
        os.environ["AI_NEWS_TOPICS_JSON"] = args.config

    # Run appropriate mode
    if args.mode == "multi-agent":
        run_multi_agent()
    else:
        run_simple()


def run():
    """Default run function for backward compatibility."""
    run_multi_agent()


if __name__ == "__main__":
    main()


