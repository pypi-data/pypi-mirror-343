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
from pathlib import Path
from .init_project import create_project_structure
from .utils.test_generator import start_pdf_watcher
from .utils.logger import logger

@click.group()
def cli():
    """VAssureAI Framework CLI"""
    pass

@cli.command()
@click.argument('project_name', required=False)
def init(project_name=None):
    """Initialize a new VAssureAI project"""
    try:
        if project_name:
            # Create the project directory first
            os.makedirs(project_name, exist_ok=True)
            target_dir = os.path.abspath(project_name)
        else:
            # Use current directory
            target_dir = os.getcwd()
        
        # Use the new project initialization function
        create_project_structure(target_dir)
        
        click.echo(f"✅ VAssureAI project initialized successfully in {target_dir}")
        click.echo("\nNext steps:")
        click.echo("1. Add test specification PDFs to the input_pdfs directory")
        click.echo("2. Run 'vassure watch-pdfs' to generate tests")
        click.echo("3. Execute tests with 'python -m pytest tests/'")
        
    except Exception as e:
        click.echo(f"❌ Error initializing project: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('input_path', required=False)
def watch_pdfs(input_path=None):
    """Watch for PDF files and generate tests"""
    try:
        if not input_path:
            input_path = os.path.join(os.getcwd(), "input_pdfs")
            
        if not os.path.exists(input_path):
            os.makedirs(input_path, exist_ok=True)
            click.echo(f"Created input directory: {input_path}")
            
        click.echo(f"Watching for PDF files in: {input_path}")
        click.echo("Press Ctrl+C to stop")
        
        # Start the PDF watcher
        start_pdf_watcher(input_path)
        
    except KeyboardInterrupt:
        click.echo("\nPDF watcher stopped")
    except Exception as e:
        click.echo(f"❌ Error watching PDF files: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--test-dir', '-t', default='tests', help='Directory containing test files')
@click.option('--html-report', '-r', is_flag=True, help='Generate HTML report')
@click.option('--parallel', '-n', type=int, help='Run tests in parallel')
def run(test_dir, html_report, parallel):
    """Run tests in the project"""
    try:
        # Build pytest command
        cmd = f"python -m pytest {test_dir} -v --asyncio-mode=auto"
        
        # Add HTML report option
        if html_report:
            cmd += " --html=reports/test_report.html"
            
        # Add parallel execution option
        if parallel and parallel > 0:
            cmd += f" -n {parallel}"
            
        click.echo(f"Running tests: {cmd}")
        exit_code = os.system(cmd)
        
        # Exit with the exit code from pytest
        if exit_code != 0:
            sys.exit(exit_code)
            
    except Exception as e:
        click.echo(f"❌ Error running tests: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
@click.argument('pdf_path')
def process_pdf(pdf_path):
    """Process a single PDF file to generate tests"""
    try:
        from .utils.test_generator import ScriptGenerator
        
        if not os.path.exists(pdf_path):
            click.echo(f"❌ PDF file not found: {pdf_path}", err=True)
            sys.exit(1)
            
        click.echo(f"Processing PDF file: {pdf_path}")
        
        # Create test generator
        generator = ScriptGenerator()
        
        # Process the PDF
        generated_files = generator.process_pdf(pdf_path)
        
        if generated_files:
            click.echo(f"✅ Generated {len(generated_files)} test files:")
            for file in generated_files:
                click.echo(f"  - {file}")
        else:
            click.echo("⚠️ No test files generated")
            
    except Exception as e:
        click.echo(f"❌ Error processing PDF: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def version():
    """Display VAssureAI version"""
    try:
        import pkg_resources
        version = pkg_resources.get_distribution("vassure-ai").version
        click.echo(f"VAssureAI Framework v{version}")
    except:
        click.echo("VAssureAI Framework (version unknown)")

@cli.command()
def interactive():
    """Launch VAssureAI in interactive mode with menu-driven options"""
    # Color settings similar to batch file
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    
    # Clear screen (works on both Windows and Unix-like systems)
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Print welcome banner
    click.echo(f"{CYAN}=========================================={RESET}")
    click.echo(f"{CYAN}         VAssureAI Framework            {RESET}")
    click.echo(f"{CYAN}=========================================={RESET}")
    click.echo()
    
    # Display welcome message
    logger.info("Welcome to VAssureAI Framework")
    click.echo()
    
    # Primary action selection
    click.echo(f"{WHITE}Select action:{RESET}")
    click.echo(f"{CYAN}1{RESET} - Create/Update Tests from PDF")
    click.echo(f"{CYAN}2{RESET} - Execute Existing Tests")
    choice = click.prompt("Enter choice", default="1")
    
    # Default settings
    run_tests = "n"
    execution_mode = "sequential"
    num_workers = "auto"
    
    if choice == "1":
        click.echo()
        click.echo(f"{YELLOW}Selected: Create/Update Tests from PDF{RESET}")
        click.echo()
        
        # Ask for input file path
        pdf_path = click.prompt("Enter PDF file path (or press Enter to use default input_pdfs folder)", default="input_pdfs")
        
        # Check if path exists
        if not os.path.exists(pdf_path):
            click.echo(f"{RED}Error: Path does not exist: {pdf_path}{RESET}")
            sys.exit(1)
        
        # Ask for test execution preference
        run_tests = click.prompt("Run tests after generation? (Y/N)", default="N").lower()
        
        if run_tests == "y":
            # Configure test execution
            click.echo()
            click.echo(f"{WHITE}Select execution mode:{RESET}")
            click.echo(f"{CYAN}1{RESET} - Sequential (Default)")
            click.echo(f"{CYAN}2{RESET} - Parallel")
            mode_choice = click.prompt("Enter choice", default="1")
            
            if mode_choice == "2":
                execution_mode = "parallel"
                num_workers = click.prompt("Enter number of parallel workers (auto/2/3/4/etc)", default="auto")
        
        # Show current settings
        click.echo()
        click.echo(f"{WHITE}Current Settings:{RESET}")
        click.echo(f"{YELLOW}-------------------{RESET}")
        click.echo(f"- Mode: Create/Update Tests")
        click.echo(f"- PDF Path: {pdf_path}")
        click.echo(f"- Run Tests: {run_tests.upper()}")
        if run_tests == "y":
            click.echo(f"- Execution Mode: {execution_mode}")
            if execution_mode == "parallel":
                click.echo(f"- Workers: {num_workers}")
        
        # Confirm settings
        if not click.confirm("Continue with these settings?", default=True):
            click.echo(f"{YELLOW}Operation cancelled by user.{RESET}")
            return
        
        # Start PDF watcher
        click.echo(f"{YELLOW}Starting PDF watcher...{RESET}")
        try:
            # Import in function scope to avoid import issues
            from .utils.test_generator import start_pdf_watcher, ScriptGenerator
            
            if os.path.isfile(pdf_path):
                # Process a single PDF file
                generator = ScriptGenerator()
                generated_files = generator.process_pdf(pdf_path)
                
                if generated_files and run_tests == "y":
                    # Run the generated tests
                    for file in generated_files:
                        _run_test(file, execution_mode, num_workers)
            else:
                # Start watching a directory
                start_pdf_watcher(pdf_path)
                click.echo(f"{GREEN}Framework started. Watching for PDF changes in: {pdf_path}{RESET}")
                click.echo("Press Ctrl+C to stop")
                try:
                    # Keep the script running until Ctrl+C
                    while True:
                        import time
                        time.sleep(1)
                except KeyboardInterrupt:
                    click.echo(f"{YELLOW}PDF watcher stopped by user.{RESET}")
        
        except Exception as e:
            click.echo(f"{RED}Error starting PDF watcher: {str(e)}{RESET}")
            sys.exit(1)
            
    elif choice == "2":
        click.echo()
        click.echo(f"{YELLOW}Selected: Execute Existing Tests{RESET}")
        click.echo()
        
        # Configure test execution
        click.echo(f"{WHITE}Select execution mode:{RESET}")
        click.echo(f"{CYAN}1{RESET} - Sequential (Default)")
        click.echo(f"{CYAN}2{RESET} - Parallel")
        mode_choice = click.prompt("Enter choice", default="1")
        
        if mode_choice == "2":
            execution_mode = "parallel"
            num_workers = click.prompt("Enter number of parallel workers (auto/2/3/4/etc)", default="auto")
        
        # Check test directory
        tests_dir = "tests"
        if not os.path.exists(tests_dir) or not os.listdir(tests_dir):
            alt_tests_dir = "vassureai/tests"
            if os.path.exists(alt_tests_dir) and os.listdir(alt_tests_dir):
                tests_dir = alt_tests_dir
        
        # Show current settings
        click.echo()
        click.echo(f"{WHITE}Current Settings:{RESET}")
        click.echo(f"{YELLOW}-------------------{RESET}")
        click.echo(f"- Mode: Execute Tests")
        click.echo(f"- Test Directory: {tests_dir}")
        click.echo(f"- Execution Mode: {execution_mode}")
        if execution_mode == "parallel":
            click.echo(f"- Workers: {num_workers}")
        
        # Confirm settings
        if not click.confirm("Continue with these settings?", default=True):
            click.echo(f"{YELLOW}Operation cancelled by user.{RESET}")
            return
        
        # Build pytest command
        cmd = f"python -m pytest {tests_dir} -v --asyncio-mode=auto --html=reports/report.html --self-contained-html"
        
        # Add parallel execution if selected
        if execution_mode == "parallel":
            cmd += f" -n {num_workers}"
        
        # Run tests
        click.echo(f"{YELLOW}Executing existing tests...{RESET}")
        click.echo()
        
        exit_code = os.system(cmd)
        
        if exit_code == 0:
            click.echo(f"{GREEN}Test execution completed successfully!{RESET}")
        else:
            click.echo(f"{RED}Test execution completed with failures.{RESET}")
        
    else:
        click.echo(f"{RED}Invalid choice. Exiting...{RESET}")
        sys.exit(1)

def _run_test(test_file, execution_mode="sequential", num_workers="auto"):
    """Helper function to run a single test file"""
    # Build pytest command
    cmd = f"python -m pytest {test_file} -v --asyncio-mode=auto --html=reports/report.html --self-contained-html"
    
    # Add parallel execution if selected
    if execution_mode == "parallel":
        cmd += f" -n {num_workers}"
    
    # Run the test
    click.echo(f"Running test: {test_file}")
    exit_code = os.system(cmd)
    
    if exit_code == 0:
        click.echo("\033[92mTest execution successful!\033[0m")
    else:
        click.echo("\033[91mTest execution failed.\033[0m")

def main():
    """CLI entry point"""
    cli()

if __name__ == "__main__":
    main()