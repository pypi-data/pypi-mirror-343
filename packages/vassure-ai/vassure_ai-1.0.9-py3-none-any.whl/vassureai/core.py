"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Core functionality for VAssureAI Framework
"""

import os
import sys
import asyncio
from .utils.test_generator import start_pdf_watcher
from .utils.logger import logger

async def init_framework():
    """Initialize the framework"""
    # Create required directories
    directories = [
        "input_pdfs",  # Always create this regardless of custom path
        "tests",
        "utils/templates",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Initialized directory: {directory}")

def start_framework(pdf_dir: str, watch: bool = True):
    """Start the VAssureAI framework"""
    try:
        # Initialize framework
        asyncio.run(init_framework())
        
        # Start PDF watcher
        logger.info("Starting VAssureAI Framework...")
        if os.path.isfile(pdf_dir):
            logger.info(f"Processing PDF file: {pdf_dir}")
        else:
            logger.info(f"Watching for PDFs in: {pdf_dir}")
        
        start_pdf_watcher(pdf_dir, watch)
        
    except KeyboardInterrupt:
        logger.info("Framework shutdown requested")
    except Exception as e:
        logger.error(f"Framework initialization failed: {str(e)}")
        raise