"""
Root conftest.py file to configure Python path for tests.
This file is automatically loaded by pytest.
"""

import sys
from pathlib import Path

# Add the project root to Python path so we can import src modules
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print(f"Added to Python path: {project_root}")
print(f"Python path: {sys.path[:3]}")  # Show first 3 paths for debugging