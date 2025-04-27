"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Utilities Module for VAssureAI Framework
Provides common utility functions including:
- File handling operations
- Data manipulation helpers
- Common test utilities
- System interaction functions
"""

import os
import base64
from datetime import datetime
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from .config import Config
import PyPDF2
from typing import List, Dict

# Load environment variables
load_dotenv()

class TestConfig:
    """Configuration class for test settings"""
    BASE_URL = os.getenv("BASE_URL")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL = "gemini-2.0-flash-exp"

def initialize_llm():
    """Initialize the LLM with API key from environment"""
    return ChatGoogleGenerativeAI(
        model=TestConfig.MODEL,
        api_key=SecretStr(TestConfig.API_KEY)
    )

def save_screenshot(base64_screenshot, step_index, screenshot_dir="screenshots"):
    """Save base64 screenshot to file"""
    os.makedirs(screenshot_dir, exist_ok=True)
    if not base64_screenshot:
        return None
        
    try:
        screenshot_path = os.path.join(
            screenshot_dir, 
            f"step_{step_index}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        screenshot_data = base64.b64decode(
            base64_screenshot.split(',')[1] if ',' in base64_screenshot else base64_screenshot
        )
        with open(screenshot_path, "wb") as f:
            f.write(screenshot_data)
        return screenshot_path if os.path.exists(screenshot_path) else None
    except Exception as e:
        print(f"Screenshot save failed: {str(e)}")
        return None

def determine_status(history_item):
    """Determine the status of a test step based on history item"""
    status = "PASS"
    if history_item.result and history_item.result[0].error:
        status = "FAIL"
    elif not history_item.result or "error" in str(history_item.result[0].extracted_content).lower():
        status = "FAIL"
    return status

def get_timestamp(history_item):
    """Get the timestamp for a test step"""
    return (datetime.fromtimestamp(history_item.metadata.step_start_time) 
            if history_item.metadata else datetime.now())

class common_utilities:
    """Common utility functions for test steps"""
    
    @staticmethod
    def get_login_steps():
        """Return common login test steps"""
        return [
            f'Navigate to login page {TestConfig.BASE_URL}',
            'wait for network idle',  # Wait for page load
            f'Enter username {TestConfig.USERNAME} in username field',
            f'Click continue button',
            'wait for network idle',
            f'Enter password {TestConfig.PASSWORD} in password field',
            f'Click login button',
            'wait for network idle',
            'verify cart icon is visible'
        ]

    @staticmethod
    def get_select_vault():
        """Selects the vault from dropdown"""
        return [
            'wait for element "text=Select a vault"',
            f'Click select a vault dropdown',
            'wait for network idle',
            'wait for element "text=QualityBasicsDryRun25R1"',
            f'Click "QualityBasicsDryRun25R1 (vaultbasics-automation.com)" vault option',
            'wait for network idle'
        ]
        
    @staticmethod
    def get_retry_config():
        """Get retry configuration for test steps"""
        return {
            "max_retries": Config.retry.max_retries,
            "retry_delay": Config.retry.retry_delay,
            "retry_on_network_error": Config.retry.retry_on_network_error
        }

class PDFTestProcessor:
    """Process PDF test specifications and convert them to executable test steps"""
    
    def __init__(self, pdf_dir: str = "input_pdfs"):
        """Initialize PDFTestProcessor
        
        Args:
            pdf_dir: Directory containing PDF files, or path to a specific PDF file
        """
        self.pdf_dir = os.path.dirname(pdf_dir) if os.path.isfile(pdf_dir) else pdf_dir
        self.llm = initialize_llm()
        
        # Create directory if it doesn't exist
        if not os.path.isfile(pdf_dir):  # Only create if pdf_dir is a directory path
            os.makedirs(self.pdf_dir, exist_ok=True)

    def extract_test_cases(self, pdf_path: str) -> List[Dict]:
        """Extract test cases from PDF file"""
        test_cases = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract text from each page
                full_text = ""
                for page in pdf_reader.pages:
                    full_text += page.extract_text()
                
                # Process the text to identify test cases
                test_blocks = self._split_into_test_blocks(full_text)
                
                # Convert each test block to structured format
                for block in test_blocks:
                    test_case = self._convert_to_test_case(block)
                    if test_case:
                        test_cases.append(test_case)
                        
        except Exception as e:
            print(f"Failed to process PDF {pdf_path}: {str(e)}")
            
        return test_cases
    
    def _split_into_test_blocks(self, text: str) -> List[str]:
        """Split PDF text into individual test case blocks"""
        # Split text on common test case markers
        markers = ["Test Case:", "Test ID:", "Test Scenario:"]
        blocks = []
        
        current_block = ""
        for line in text.split('\n'):
            if any(marker in line for marker in markers):
                if current_block:
                    blocks.append(current_block.strip())
                current_block = line
            else:
                current_block += "\n" + line
                
        if current_block:
            blocks.append(current_block.strip())
            
        return blocks
    
    def _convert_to_test_case(self, block: str) -> Dict:
        """Convert a test block to structured test case format"""
        try:
            # Use LLM to parse the test case text into structured steps
            prompt = f"""
            Convert this test case description into a list of specific test steps:
            {block}
            
            Format each step as a clear instruction that can be automated.
            """
            
            response = self.llm.invoke(prompt)
            steps = self._parse_llm_response(response.content if hasattr(response, 'content') else str(response))
            
            return {
                "name": self._extract_test_name(block),
                "description": block,
                "steps": steps
            }
            
        except Exception as e:
            print(f"Failed to convert test block: {str(e)}")
            return None
    
    def _extract_test_name(self, block: str) -> str:
        """Extract test name from test block"""
        first_line = block.split('\n')[0]
        return first_line.split(':', 1)[1].strip() if ':' in first_line else "Unnamed Test"
    
    def _parse_llm_response(self, response: str) -> List[str]:
        """Parse LLM response into list of test steps"""
        steps = []
        
        # Remove markdown code blocks if present
        response = response.replace('```', '').strip()
        
        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Skip comment lines and markdown markers
            if line.startswith(('#', '//', '--', '```', '>')):
                continue
                
            # Clean up step format - remove numbering and bullet points
            if any(line.startswith(prefix) for prefix in ['-', '*', '+'] or 
                  (line[0].isdigit() and line[1:3] in ['. ', ') ', '- '])):
                line = line[line.find(' ')+1:].strip()
                
            # Remove any additional formatting markers
            line = line.strip('*').strip('_').strip()
            
            # Remove step numbers if they exist like "1. ", "Step 1: "
            if line.startswith(('Step ', 'step ')):
                parts = line.split(':', 1)
                if len(parts) > 1:
                    line = parts[1].strip()
                    
            # Skip empty lines after cleanup
            if line:
                steps.append(line)
                
        return steps