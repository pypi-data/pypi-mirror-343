"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

VAssureAI Command Line Interface
Handles framework commands like initialization.
"""

import click
import os
import sys
from pathlib import Path
from .utils.logger import logger

# Standard project structure
PROJECT_DIRS = [
    'input_pdfs',
    'tests',
    'tests/utils',
    'reports',
    'reports/pdf',
    'reports/html',
    'screenshots',
    'videos',
    'logs',
    'metrics',
    'metrics/metrics_data',
]

# Default file contents
DEFAULT_FILES = {
    'requirements.txt': '''# Core Dependencies
browser-use==0.1.41
pytest==8.3.5
pytest-asyncio==0.26.0
pytest-html==4.1.1
pytest-metadata==3.1.1
pytest-timeout==2.3.1
pytest-xdist==3.6.1
python-dotenv==1.0.1
langchain==0.3.22
langchain-google-genai==2.1.2
pydantic==2.10.4
psutil==7.0.0
plotly==5.18.0
reportlab==4.0.0
pillow==10.0.0
black==24.1.0
flake8==7.0.0
mypy==1.8.0
pytest-cov==4.1.0
PyPDF2==3.0.0
watchdog==3.0.0
Jinja2==3.1.0
click==8.1.8
''',
    'pytest.ini': '''[pytest]
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    auto_generated: mark test as auto-generated from PDF
    requires_browser: mark test as needing a browser instance
    network_sensitive: mark test as sensitive to network conditions

asyncio_mode = auto
''',
    '.env.example': '''# VAssureAI Framework Configuration
BROWSER_TYPE=chrome
HEADLESS_MODE=false
PDF_INPUT_DIR=input_pdfs
REPORT_DIR=reports
''',
    'conftest.py': '''"""Test Configuration for VAssureAI Framework Project"""
import pytest
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', f'test_run.log')),
        logging.StreamHandler()
    ]
)

@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Set up test environment"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        logging.warning("python-dotenv not installed. Environment variables will not be loaded from .env file.")
    yield
''',
    'tests/__init__.py': '''"""VAssureAI Test Package"""
''',
    'tests/test_example.py': '''"""Example VAssureAI Test"""
import pytest
from utils.base_test import BaseTest

class TestExample(BaseTest):
    """Example test class demonstrating VAssureAI framework usage"""
    
    @pytest.mark.auto_generated
    async def test_example(self):
        """Example test case"""
        # Your test implementation here
        assert True, "Example test passed"
'''
}

@click.group()
def cli():
    """VAssureAI Test Automation Framework CLI"""
    pass

@cli.command()
@click.argument('project_name')
def init(project_name: str):
    """Initialize a new VAssureAI project"""
    try:
        # Create project directory
        project_path = os.path.abspath(project_name)
        os.makedirs(project_path, exist_ok=True)
        logger.info(f"Initializing VAssureAI project in: {project_path}")
        
        # Create all required directories
        for directory in PROJECT_DIRS:
            dir_path = os.path.join(project_path, directory)
            os.makedirs(dir_path, exist_ok=True)
            # Create .gitkeep to ensure empty directories are tracked
            with open(os.path.join(dir_path, '.gitkeep'), 'w') as f:
                pass
            logger.info(f"Created directory: {dir_path}")
            
        # Create default files
        for filename, content in DEFAULT_FILES.items():
            file_path = os.path.join(project_path, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            logger.info(f"Created file: {file_path}")
            
        # Create .env from .env.example
        env_example = os.path.join(project_path, ".env.example")
        env_file = os.path.join(project_path, ".env")
        if os.path.exists(env_example):
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            logger.info("Created: .env (copy of .env.example)")
        
        logger.info("\n✅ VAssureAI project initialized successfully!")
        logger.info("\nNext steps:")
        logger.info("1. Create and activate a virtual environment:")
        logger.info("   python -m venv venv")
        logger.info("   venv\\Scripts\\activate  # On Windows")
        logger.info("   source venv/bin/activate # On Unix/macOS")
        logger.info(f"2. Install dependencies: pip install -r {os.path.join(project_path, 'requirements.txt')}")
        logger.info(f"3. Update the .env file with your settings")
        logger.info("4. Place your PDF test specifications in the input_pdfs directory")
        logger.info("5. Run 'vassure watch-pdfs' to generate tests")
        
    except Exception as e:
        logger.error(f"❌ Error initializing project: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    cli()