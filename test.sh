#!/bin/bash

# Simple test runner script for AI News LangGraph

echo "🧪 AI News LangGraph Test Runner"
echo "================================"

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Warning: Not in virtual environment"
    echo "   Consider running: source .venv/bin/activate"
    echo ""
fi

# Default to all tests
TEST_TARGET=${1:-"tests/"}

# Check if specific test category requested
case "$1" in
    state)
        echo "Running state model tests..."
        python3 -m pytest tests/test_state.py -v
        ;;
    prompts)
        echo "Running prompt tests..."
        python3 -m pytest tests/test_prompts.py -v
        ;;
    nodes)
        echo "Running node tests..."
        python3 -m pytest tests/test_nodes_v2.py -v
        ;;
    unit)
        echo "Running unit tests..."
        python3 -m pytest -m unit -v
        ;;
    integration)
        echo "Running integration tests..."
        python3 -m pytest -m integration -v
        ;;
    all)
        echo "Running all tests..."
        python3 -m pytest tests/ -v
        ;;
    quick)
        echo "Running quick smoke tests..."
        python3 -m pytest tests/test_state.py::TestArticleModel -v
        ;;
    *)
        if [ -n "$1" ]; then
            echo "Running tests: $TEST_TARGET"
            python3 -m pytest "$TEST_TARGET" -v
        else
            echo "Running all tests..."
            python3 -m pytest tests/ -v
        fi
        ;;
esac

echo ""
echo "✅ Test run complete!"