"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------

CLI interface for VAssureAI Framework
"""

import os
import sys
import click
import shutil
from pathlib import Path
from typing import Optional

@click.group()
def cli():
    """VAssureAI Test Automation Framework CLI"""
    pass

@cli.command()
@click.argument('project_name')
@click.option('--path', '-p', default='.', help='Path where the project should be created')
def init(project_name: str, path: str):
    """Initialize a new VAssureAI test automation project"""
    project_path = os.path.join(path, project_name)
    
    try:
        # Create project structure
        directories = [
            'tests',
            'input_pdfs',
            'reports',
            'screenshots',
            'logs',
            'utils',
            'actions'
        ]
        
        os.makedirs(project_path, exist_ok=True)
        for dir_name in directories:
            os.makedirs(os.path.join(project_path, dir_name), exist_ok=True)
            
        # Create essential files
        create_config_file(project_path)
        create_readme(project_path)
        create_gitignore(project_path)
        create_requirements(project_path)
        create_sample_test(project_path)
        
        click.echo(f"✅ Successfully created VAssureAI project: {project_name}")
        click.echo("\nNext steps:")
        click.echo("1. cd " + project_name)
        click.echo("2. pip install -r requirements.txt")
        click.echo("3. Add your PDF test cases in the input_pdfs directory")
        click.echo("4. Run 'vassure run' to start the framework")
        
    except Exception as e:
        click.echo(f"❌ Error creating project: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--pdf-dir', '-p', default='input_pdfs', help='Directory containing PDF test cases')
@click.option('--watch/--no-watch', default=True, help='Watch for new PDFs')
def run(pdf_dir: str, watch: bool):
    """Run the VAssureAI framework"""
    try:
        from vassureai.core import start_framework
        start_framework(pdf_dir, watch)
    except Exception as e:
        click.echo(f"❌ Error running framework: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('test_name')
def create_test(test_name: str):
    """Create a new test case template"""
    try:
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'test_template.py')
        test_file = f"test_{test_name.lower()}.py"
        
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

def get_protected_header():
    """Get the protected content header"""
    return '''"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------
"""
'''

def create_config_file(project_path: str):
    """Create default configuration file"""
    config_path = os.path.join(project_path, 'vassure_config.py')
    with open(config_path, 'w') as f:
        f.write(get_protected_header() + '''
"""
VAssureAI Framework Configuration
"""

class Config:
    """Framework configuration settings"""
    
    class browser:
        """Browser settings"""
        headless = False
        record_video = True
        video_dir = "videos"
        
    class retry:
        """Retry settings"""
        max_retries = 3
        retry_delay = 1
        
    class visual:
        """Visual settings"""
        highlight = True
        screenshot_on_step = True
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
- `utils/` - Utility functions
- `actions/` - Custom test actions

## Commands

- Initialize project: `vassure init PROJECT_NAME`
- Run framework: `vassure run`
- Create new test: `vassure create-test TEST_NAME`
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
env/
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

# VAssureAI
logs/
reports/
screenshots/
videos/
*.log
''')

def create_requirements(project_path: str):
    """Create requirements.txt"""
    req_path = os.path.join(project_path, 'requirements.txt')
    with open(req_path, 'w') as f:
        f.write('''vassure-ai>=1.0.0
pytest>=8.3.5
pytest-asyncio>=0.26.0
pytest-html>=4.1.1
''')

def create_sample_test(project_path: str):
    """Create a sample test file"""
    test_dir = os.path.join(project_path, 'tests')
    test_path = os.path.join(test_dir, 'test_sample.py')
    with open(test_path, 'w') as f:
        f.write(get_protected_header() + '''
"""
Sample test case created by VAssureAI Framework
"""

import pytest
from vassureai.base_test import BaseTest

class TestSample(BaseTest):
    """Sample test case demonstrating VAssureAI framework usage"""
    
    @pytest.fixture(autouse=True)
    def setup_test(self, setup_base):
        """Setup test instance"""
        self.test_name = "sample_test"
        return self
        
    def get_test_steps(self):
        """Define test steps"""
        return [
            "1. Navigate to application URL",
            "2. Enter username",
            "3. Enter password",
            "4. Click login button",
            "5. Verify successful login"
        ]
    
    @pytest.mark.asyncio
    async def test_execution(self):
        """Execute the test case"""
        test_steps = self.get_test_steps()
        return await self._execute_test(test_steps, "Sample Test Results")
''')

def main():
    """CLI entry point"""
    cli()

if __name__ == "__main__":
    main()