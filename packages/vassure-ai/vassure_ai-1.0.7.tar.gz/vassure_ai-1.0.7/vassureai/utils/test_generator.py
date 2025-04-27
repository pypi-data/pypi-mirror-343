"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Test Script Generator for VAssureAI Framework
Automatically generates test scripts from PDF test specifications
"""

import os
import time
import ast
from pathlib import Path
from typing import Dict, List, Optional, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from jinja2 import Environment, FileSystemLoader
import pytest
# Fix relative imports
from .utilities import PDFTestProcessor
from .logger import logger

# Naming the class without 'Test' prefix prevents pytest from collecting it
class ScriptGenerator:
    """Generates test scripts from PDF test specifications"""
    
    def __init__(self, input_dir: str = "input_pdfs", output_dir: str = "tests"):
        # Use project directory for input and output
        # When installed via pip, this will be the developer's project directory
        project_root = os.getcwd()  # Get the current working directory (developer's project)
        self.input_dir = os.path.join(project_root, input_dir)
        self.output_dir = os.path.join(project_root, output_dir)
        self.processor = PDFTestProcessor(self.input_dir)
        
        # Use absolute path for template loading
        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir, 'templates')
        self.template_env = Environment(loader=FileSystemLoader(templates_dir))
        
        # Create directories if they don't exist
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info(f"Test generator initialized with input_dir: {self.input_dir}, output_dir: {self.output_dir}")

    def copy_pdf_to_input_dir(self, pdf_path: str) -> str:
        """Copy PDF file to input directory and return new path"""
        try:
            if not os.path.isfile(pdf_path):
                logger.error(f"Source file does not exist: {pdf_path}")
                return None
                
            # Get just the filename from the path
            filename = os.path.basename(pdf_path)
            new_path = os.path.join(self.input_dir, filename)
            
            # Copy the file if it's not already in input_pdfs
            if os.path.normpath(pdf_path) != os.path.normpath(new_path):
                import shutil
                shutil.copy2(pdf_path, new_path)
                logger.info(f"Copied PDF file to: {new_path}")
            return new_path
            
        except Exception as e:
            logger.error(f"Failed to copy PDF file: {str(e)}")
            return None

    def _extract_existing_test_steps(self, file_path: str) -> Optional[Set[str]]:
        """Extract existing test steps from a test file"""
        try:
            with open(file_path, 'r') as f:
                tree = ast.parse(f.read())
                
            # Find the get_all_test_steps method
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == 'get_all_test_steps':
                    # Find the return statement with list of steps
                    for sub_node in ast.walk(node):
                        if isinstance(sub_node, ast.Return):
                            if isinstance(sub_node.value, ast.List):
                                # Extract string literals from list
                                return {
                                    ast.literal_eval(elt) 
                                    for elt in sub_node.value.elts 
                                    if isinstance(elt, ast.Str)
                                }
            return None
        except Exception as e:
            logger.error(f"Failed to extract steps from {file_path}: {str(e)}")
            return None
            
    def _needs_update(self, existing_steps: Set[str], new_steps: List[str]) -> bool:
        """Check if test needs to be updated based on step differences"""
        new_steps_set = set(new_steps)
        return bool(new_steps_set - existing_steps or existing_steps - new_steps_set)
        
    def generate_test_file(self, test_case: Dict) -> str:
        """Generate a test file from a test case dictionary"""
        try:
            # Create test file path
            file_name = f"test_{test_case['name'].lower().replace(' ', '_')}.py"
            file_path = os.path.join(self.output_dir, file_name)
            
            # Check if test file already exists
            if os.path.exists(file_path):
                existing_steps = self._extract_existing_test_steps(file_path)
                if existing_steps:
                    if not self._needs_update(existing_steps, test_case['steps']):
                        logger.info(f"Test {file_name} already exists and no updates needed")
                        return file_path
                    logger.info(f"Test {file_name} exists and will be updated with new steps")
            
            # Generate or update test file
            template = self.template_env.get_template('test_template.py')
            test_content = template.render(
                test_name=test_case['name'].lower().replace(' ', '_'),
                test_description=test_case['description'],
                test_steps=test_case['steps']
            )
            
            with open(file_path, 'w') as f:
                f.write(test_content)
                
            action = "Updated" if os.path.exists(file_path) else "Generated"
            logger.info(f"{action} test file: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Failed to generate/update test file: {str(e)}")
            return None
            
    def process_pdf(self, pdf_path: str) -> List[str]:
        """Process a PDF file and generate test scripts"""
        generated_files = []
        
        try:
            # Copy PDF to input directory if it's not already there
            input_pdf_path = self.copy_pdf_to_input_dir(pdf_path)
            if not input_pdf_path:
                return generated_files
                
            # Extract test cases from PDF
            test_cases = self.processor.extract_test_cases(input_pdf_path)
            
            # Use PDF filename without extension for test name
            pdf_name = os.path.splitext(os.path.basename(input_pdf_path))[0]
            
            # Generate test file for each test case
            for test_case in test_cases:
                test_case['name'] = pdf_name
                file_path = self.generate_test_file(test_case)
                if file_path:
                    generated_files.append(file_path)
                    
        except Exception as e:
            logger.error(f"Failed to process PDF {pdf_path}: {str(e)}")
            
        return generated_files
        
    def process_existing_pdfs(self):
        """Process all existing PDF files in the input directory"""
        if not os.path.exists(self.input_dir):
            logger.warning(f"Input directory {self.input_dir} does not exist")
            return
            
        logger.info(f"Processing existing PDF files in {self.input_dir}")
        processed = 0
        
        for filename in os.listdir(self.input_dir):
            if filename.lower().endswith('.pdf'):
                pdf_path = os.path.join(self.input_dir, filename)
                logger.info(f"Processing existing PDF: {pdf_path}")
                self.process_pdf(pdf_path)
                processed += 1
                
        logger.info(f"Processed {processed} existing PDF files")

class PDFHandler(FileSystemEventHandler):
    """Handles file system events for PDF files"""
    
    def __init__(self, generator: ScriptGenerator):
        self.generator = generator
    
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            logger.info(f"New PDF detected: {event.src_path}")
            self.generator.process_pdf(event.src_path)
            
    def on_modified(self, event):
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            logger.info(f"PDF modified: {event.src_path}")
            self.generator.process_pdf(event.src_path)

def start_pdf_watcher(input_path: str = "input_pdfs"):
    """Start watching for new PDF files in the input directory"""
    output_dir = "tests"
    
    # If input_path is a file, watch its directory
    if os.path.isfile(input_path):
        watch_dir = os.path.dirname(input_path)
        generator = ScriptGenerator(watch_dir, output_dir)
        # Process the specific file first
        generator.process_pdf(input_path)
    else:
        # Input path is a directory
        watch_dir = input_path
        generator = ScriptGenerator(watch_dir, output_dir)
        # Process all existing PDFs in the directory
        generator.process_existing_pdfs()
    
    # Start watching for new ones
    event_handler = PDFHandler(generator)
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=False)
    observer.start()
    
    try:
        logger.info(f"Started watching {watch_dir} for new PDF files...")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        logger.info("Stopped watching for PDF files")
    observer.join()

if __name__ == "__main__":
    start_pdf_watcher()