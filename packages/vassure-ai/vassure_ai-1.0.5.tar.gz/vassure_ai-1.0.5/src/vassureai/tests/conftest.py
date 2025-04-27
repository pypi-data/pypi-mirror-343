"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------
"""

import pytest
import sys
import os

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Note: pytest_plugins definition has been moved to the root conftest.py
# as per pytest best practices