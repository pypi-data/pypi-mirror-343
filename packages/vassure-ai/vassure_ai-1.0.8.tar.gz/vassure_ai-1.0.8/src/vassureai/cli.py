"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

CLI Module for VAssureAI Framework
"""

import os
import sys
import click
import shutil
from pathlib import Path
from .utils.file_protection import get_protected_header

@click.group()
def cli():
    """VAssureAI Framework CLI"""
    pass

@cli.command()
@click.argument('test_name')
def create_test(test_name: str):
    """Create a new test case template"""
    try:
        template_path = os.path.join(os.path.dirname(__file__), 'utils', 'templates', 'test_template.py')
        test_file = os.path.join(os.path.dirname(__file__), 'tests', f"test_{test_name.lower()}.py")
        
        # Ensure tests directory exists
        os.makedirs(os.path.dirname(test_file), exist_ok=True)
        
        if os.path.exists(template_path):
            shutil.copy(template_path, test_file)
            with open(test_file, 'r') as f:
                content = f.read()
            
            content = content.replace('TestTemplate', f'Test{test_name.title()}')
            
            with open(test_file, 'w') as f:
                f.write(content)
                
            click.echo(f"✅ Created new test: {test_file}")
        else:
            click.echo("❌ Test template not found", err=True)
            
    except Exception as e:
        click.echo(f"❌ Error creating test: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('project_name')
def init(project_name: str):
    """Initialize a new VAssureAI project"""
    try:
        # Create project directory
        project_path = os.path.abspath(project_name)
        os.makedirs(project_path, exist_ok=True)
        
        # Create required directories
        directories = [
            'input_pdfs',
            'reports/pdf',
            'reports/assets',
            'screenshots',
            'logs',
            'videos'
        ]
        
        for directory in directories:
            os.makedirs(os.path.join(project_path, directory), exist_ok=True)
            
        # Create configuration files
        create_config_file(project_path)
        create_readme(project_path)
        create_gitignore(project_path)
        create_requirements(project_path)
        create_sample_test(project_path)
        
        click.echo(f"✅ Initialized VAssureAI project in {project_path}")
        
    except Exception as e:
        click.echo(f"❌ Error initializing project: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def run():
    """Run tests in the project"""
    try:
        # Get package root directory
        package_dir = os.path.dirname(__file__)
        tests_dir = os.path.join(package_dir, 'tests')
        
        if not os.path.exists(tests_dir):
            click.echo("❌ No tests directory found", err=True)
            sys.exit(1)
            
        # Run pytest with our configuration
        os.system(f"pytest {tests_dir} -v --asyncio-mode=auto")
        
    except Exception as e:
        click.echo(f"❌ Error running tests: {str(e)}", err=True)
        sys.exit(1)

def create_config_file(project_path: str):
    """Create default configuration file"""
    config_path = os.path.join(project_path, '.env')
    with open(config_path, 'w') as f:
        f.write(get_protected_header() + '''
# VAssureAI Configuration

# Base URL for testing
BASE_URL=https://your-app-url.com

# Test credentials
USERNAME=your-username
PASSWORD=your-password

# LLM Configuration
GEMINI_API_KEY=your-api-key

# Browser Settings
VASSURE_RECORD_VIDEO=true
VASSURE_HEADLESS=true

# Test Settings
VASSURE_MAX_RETRIES=3
VASSURE_RETRY_DELAY=2
VASSURE_RETRY_ON_NETWORK=true

# Visual Settings
VASSURE_HIGHLIGHT=true
VASSURE_SCREENSHOT_ON_STEP=true
VASSURE_SCREENSHOT_ON_ERROR=true
''')

def create_readme(project_path: str):
    """Create README file"""
    readme_path = os.path.join(project_path, 'README.md')
    with open(readme_path, 'w') as f:
        f.write(get_protected_header() + '''
# VAssureAI Test Automation Project

This project uses VAssureAI Framework for test automation.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Add your PDF test cases in the `input_pdfs` directory

3. Run the framework:
   ```
   vassure run
   ```

## Project Structure

- `input_pdfs/` - Place your PDF test cases here
- `tests/` - Generated test scripts
- `reports/` - Test execution reports
- `screenshots/` - Test step screenshots
- `logs/` - Execution logs
- `videos/` - Test recordings

## Commands

- Initialize project: `vassure init PROJECT_NAME`
- Create new test: `vassure create-test TEST_NAME`
- Run framework: `vassure run`

For detailed documentation, see the [VAssureAI Documentation](src/vassureai/userguide/userguide.md).
''')

def create_gitignore(project_path: str):
    """Create .gitignore file"""
    gitignore_path = os.path.join(project_path, '.gitignore')
    with open(gitignore_path, 'w') as f:
        f.write('''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Project
screenshots/
reports/
logs/
videos/
.env
''')

def create_requirements(project_path: str):
    """Create requirements.txt"""
    requirements_path = os.path.join(project_path, 'requirements.txt')
    with open(requirements_path, 'w') as f:
        f.write('''vassure-ai>=1.0.5
pytest>=8.3.5
pytest-asyncio>=0.26.0
pytest-html>=4.1.1
python-dotenv>=1.0.0
''')

def create_sample_test(project_path: str):
    """Create a sample test file"""
    sample_test_path = os.path.join(project_path, 'tests', 'test_sample.py')
    os.makedirs(os.path.dirname(sample_test_path), exist_ok=True)
    
    with open(sample_test_path, 'w') as f:
        f.write(get_protected_header() + '''
import pytest
from vassureai.utils.base_test import BaseTest
from vassureai.utils.logger import logger
from vassureai.utils.config import Config

@pytest.mark.requires_browser
class TestSample(BaseTest):
    """Sample test case for demonstration"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, setup_base):
        """Setup test instance"""
        self.test_name = "sample_test"
        self.retry_attempts = Config.retry.max_retries
        return self
        
    def get_all_test_steps(self):
        """Get all test steps for this test case"""
        return [
            "Navigate to login page",
            "Enter username",
            "Click continue",
            "Enter password",
            "Click login",
            "Verify successful login"
        ]
        
    @pytest.mark.asyncio
    async def test_execution(self):
        """Execute the test case"""
        logger.info(f"Starting {self.test_name} execution")
        test_steps = self.get_all_test_steps()
        
        for attempt in range(self.retry_attempts + 1):
            try:
                result = await self._execute_test(test_steps, f"{self.test_name} Results")
                if result:
                    logger.info(f"{self.test_name} completed successfully")
                    return result
                else:
                    logger.warning(f"{self.test_name} attempt {attempt + 1} failed")
            except Exception as e:
                logger.error(f"{self.test_name} attempt {attempt + 1} failed with error: {str(e)}")
                if attempt == self.retry_attempts:
                    raise
                
        return None
''')

def main():
    """CLI entry point"""
    cli()

if __name__ == "__main__":
    main()