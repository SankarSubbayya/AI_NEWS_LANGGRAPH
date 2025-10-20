#!/usr/bin/env python
"""
Comprehensive test runner for the AI News LangGraph system.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --unit       # Run only unit tests
    python run_tests.py --integration # Run only integration tests
    python run_tests.py --coverage   # Run with coverage report
    python run_tests.py --verbose    # Run with verbose output
"""

import sys
import argparse
import subprocess
from pathlib import Path


def run_tests(args):
    """Run pytest with specified arguments."""
    cmd = ["pytest"]

    # Add test directory
    cmd.append("tests/")

    # Add markers based on arguments
    if args.unit:
        cmd.extend(["-m", "unit"])
    elif args.integration:
        cmd.extend(["-m", "integration"])
    elif args.performance:
        cmd.extend(["-m", "performance"])

    # Add coverage if requested
    if args.coverage:
        cmd.extend([
            "--cov=src/ai_news_langgraph",
            "--cov-report=html",
            "--cov-report=term-missing"
        ])

    # Add verbose output
    if args.verbose:
        cmd.append("-vv")
    else:
        cmd.append("-v")

    # Add specific test file if provided
    if args.file:
        cmd.append(args.file)

    # Add pytest options
    if args.failed_first:
        cmd.append("--failed-first")

    if args.last_failed:
        cmd.append("--last-failed")

    if args.parallel:
        cmd.extend(["-n", str(args.parallel)])

    # Print command
    print(f"Running: {' '.join(cmd)}\n")

    # Run tests
    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode


def run_specific_test_suites():
    """Run specific test suites with detailed reporting."""

    test_suites = [
        ("State Models", "tests/test_state.py"),
        ("Prompts", "tests/test_prompts.py"),
        ("Workflow Nodes", "tests/test_nodes_v2.py"),
        ("Tools", "tests/test_tools_direct.py"),
        ("Integration", "tests/test_integration.py")
    ]

    print("="*60)
    print("RUNNING TEST SUITES")
    print("="*60)

    results = {}
    for name, test_file in test_suites:
        if Path(test_file).exists():
            print(f"\n{'='*60}")
            print(f"Testing: {name}")
            print(f"{'='*60}")

            result = subprocess.run(
                ["pytest", test_file, "-v", "--tb=short"],
                capture_output=True,
                text=True
            )

            # Parse results
            output = result.stdout
            if "passed" in output:
                status = "✅ PASSED"
            elif "failed" in output:
                status = "❌ FAILED"
            else:
                status = "⚠️ UNKNOWN"

            results[name] = status
            print(output)

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for suite, status in results.items():
        print(f"{suite:20} {status}")
    print("="*60)


def check_test_environment():
    """Check that test environment is properly set up."""

    requirements = {
        "pytest": "pytest",
        "pytest-asyncio": "pytest-asyncio",
        "pytest-cov": "pytest-cov",
        "pytest-mock": "pytest-mock"
    }

    print("Checking test environment...")
    missing = []

    for name, package in requirements.items():
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {name} installed")
        except ImportError:
            print(f"❌ {name} not installed")
            missing.append(package)

    if missing:
        print(f"\n⚠️ Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False

    print("✅ Test environment ready\n")
    return True


def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Run AI News LangGraph tests")

    # Test selection
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests only")
    parser.add_argument("--all", action="store_true", help="Run all test suites with summary")

    # Options
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--file", help="Run specific test file")
    parser.add_argument("--failed-first", action="store_true", help="Run failed tests first")
    parser.add_argument("--last-failed", action="store_true", help="Run only last failed tests")
    parser.add_argument("--parallel", type=int, help="Run tests in parallel (number of workers)")
    parser.add_argument("--check", action="store_true", help="Check test environment only")

    args = parser.parse_args()

    # Check environment
    if args.check or not check_test_environment():
        if args.check:
            return 0
        return 1

    # Run tests
    if args.all:
        run_specific_test_suites()
        return 0
    else:
        return run_tests(args)


if __name__ == "__main__":
    sys.exit(main())