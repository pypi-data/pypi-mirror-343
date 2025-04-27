"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------

Project Initialization Module for VAssureAI Framework
Sets up the directory structure and template files for new projects
"""

import os
import shutil
import sys
import pkg_resources
from pathlib import Path
from datetime import datetime
from .utils.logger import logger

PROJECT_DIRS = [
    'input_pdfs',
    'tests',
    'reports',
    'reports/pdf',
    'reports/html',
    'screenshots',
    'videos',
    'logs',
    'metrics',
    'metrics/metrics_data',
]

# Developer-focused README content - simple and task-oriented
DEVELOPER_README = """# VAssureAI Framework Project

## Overview
This project uses the VAssureAI framework for automated web testing. VAssureAI combines the power of AI with robust browser automation to create reliable, maintainable tests with minimal coding effort.

## Project Structure
```
project_root/
├── input_pdfs/           # Place your test specification PDFs here
├── tests/                # Auto-generated and custom test files
├── reports/              # Test execution reports (HTML, PDF)
├── screenshots/          # Test execution screenshots
├── videos/               # Browser recording videos
├── logs/                 # Test execution logs
└── metrics/              # Test performance metrics
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install the VAssureAI framework:
```bash
pip install vassure-ai
```

### Creating Tests

#### From PDF Specifications
VAssureAI can automatically generate test scripts from PDF test specifications:

1. Place your test specification PDFs in the `input_pdfs` folder
2. Run the PDF watcher to auto-generate tests:
```bash
vassure watch-pdfs
```

#### Writing Custom Tests
You can also write custom tests by extending the BaseTest class.

### Running Tests

Run all tests:
```bash
python -m pytest tests/ -v --asyncio-mode=auto --html=reports/test_report.html
```

Run a specific test:
```bash
python -m pytest tests/test_my_feature.py -v --asyncio-mode=auto --html=reports/test_report.html
```

## Configuration

The framework can be configured by creating a `.env` file in your project root with the following options:

```
# Browser configuration
BROWSER_TYPE=chromium
BROWSER_HEADLESS=false
BROWSER_RECORD_VIDEO=true

# AI model configuration
LLM_MODEL=gemini-2.0-flash-exp
LLM_API_KEY=your-api-key

# Test execution configuration
RETRY_MAX_RETRIES=2
RETRY_DELAY=5
```

## Documentation

For detailed information about using the VAssureAI framework, see the framework's user guide documentation which can be accessed by running:

```bash
vassure docs
```

"""

DEFAULT_FILES = {
    '.env': """# VAssureAI Configuration
# Browser configuration
BROWSER_TYPE=chromium
BROWSER_HEADLESS=false
BROWSER_RECORD_VIDEO=true

# AI model configuration
LLM_MODEL=gemini-2.0-flash-exp
LLM_API_KEY=your-api-key-here

# Test execution configuration
RETRY_MAX_RETRIES=2
RETRY_DELAY=5
""",
    'pytest.ini': """[pytest]
# Collection settings
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Markers
markers =
    auto_generated: mark test as auto-generated from PDF
    requires_browser: mark test as needing a browser instance
    network_sensitive: mark test as sensitive to network conditions
    load_test: mark test for load testing with parameters
    nottest: mark a class or function to not be collected as a test

# asyncio settings
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
""",
    'conftest.py': '''"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------

Test Configuration for VAssureAI Framework Project
Sets up fixtures and configuration for test execution
"""

import pytest
import os
import sys

# Add the project root directory to Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Set up test environment at the beginning of test session"""
    # Load environment variables from .env file if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("python-dotenv not installed. Environment variables will not be loaded from .env file.")
    
    yield
    
    # Teardown code after all tests have run
    print("Test session completed.")
''',
    'tests/__init__.py': '''"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------

Test Package for VAssureAI Framework Project
Contains test modules for automated testing
"""
''',
    'tests/test_sample.py': '''"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------

Sample Test Module
Demonstrates how to create tests with VAssureAI Framework
"""

import pytest
from vassureai.utils.base_test import BaseTest

class TestSample(BaseTest):
    """Sample test to demonstrate VAssureAI framework usage"""

    @pytest.fixture(autouse=True)
    def setup_test(self, setup_base):
        """Setup test instance"""
        self.test_name = "test_sample"
        return self

    def get_all_test_steps(self):
        """Get all test steps for this test case"""
        return [
            "1. Navigate to 'https://example.com'",
            "2. Verify the page title contains 'Example'",
            "3. Verify the heading 'Example Domain' is displayed"
        ]

    @pytest.mark.asyncio
    async def test_sample(self):
        """Execute the test case"""
        test_steps = self.get_all_test_steps()
        result = await self._execute_test(test_steps, "Sample Test Results")
        assert result is not None
'''
}

def create_project_structure(target_dir=None):
    """Create the directory structure for a new project"""
    if target_dir:
        base_dir = Path(target_dir)
    else:
        base_dir = Path.cwd()
    
    logger.info(f"Initializing VAssureAI project in: {base_dir}")
    
    # Create directory structure
    for directory in PROJECT_DIRS:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Created directory: {dir_path}")
    
    # Create default files
    for filename, content in DEFAULT_FILES.items():
        file_path = base_dir / filename
        if not file_path.exists():  # Don't overwrite existing files
            with open(file_path, 'w') as f:
                f.write(content)
            logger.info(f"Created file: {file_path}")
    
    # Always use our embedded developer README, no more fallbacks or template lookups
    readme_path = base_dir / 'README.md'
    if not readme_path.exists():  # Don't overwrite existing README
        with open(readme_path, 'w') as f:
            f.write(DEVELOPER_README)
        logger.info(f"Created developer README: {readme_path}")
    
    logger.info("VAssureAI project structure created successfully!")
    logger.info("Next steps:")
    logger.info("1. Add test specification PDFs to the input_pdfs directory")
    logger.info("2. Run 'vassure watch-pdfs' to generate tests")
    logger.info("3. Execute tests with 'python -m pytest tests/'")

def main():
    """Entry point for project initialization command"""
    target_dir = sys.argv[1] if len(sys.argv) > 1 else None
    create_project_structure(target_dir)

if __name__ == "__main__":
    main()