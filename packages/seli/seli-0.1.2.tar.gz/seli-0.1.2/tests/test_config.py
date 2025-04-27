"""Pytest configuration for the seli tests."""

import sys
from pathlib import Path

# Add the src directory to the path so that imports work for tests
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path.resolve()))
