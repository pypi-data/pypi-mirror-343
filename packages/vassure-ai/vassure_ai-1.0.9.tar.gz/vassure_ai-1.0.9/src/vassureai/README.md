"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------
"""

# VAssureAI Framework Developer Guide
Version: 1.0.9

An AI-powered test automation framework that combines Pytest with LLM for intelligent test execution and self-healing capabilities.

## Key Features

- 🤖 AI-Powered Test Generation from PDF specifications
- 🔄 Self-healing test execution with retry mechanisms
- 📝 Comprehensive test reporting (HTML, PDF)
- 📸 Automated screenshot and video capture
- 📊 Performance metrics and analysis
- 🚀 Parallel test execution support
- 🎯 Custom action system for robust test steps

## Quick Start

### Prerequisites

- Python 3.11+
- Virtual Environment
- Required Environment Variables (add to .env file):
  ```
  BASE_URL=https://your-app-url.com
  USERNAME=your-username
  PASSWORD=your-password
  LLM_API_KEY=your-api-key
  ```

### Installation

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```

2. Install the framework:
   ```bash
   pip install vassure-ai
   ```

3. Initialize your project:
   ```bash
   vassure init
   ```

### Project Structure
```
project/
├── input_pdfs/     # Place PDF specifications here
├── logs/           # Execution logs
├── reports/        # Test reports
│   ├── html/      # HTML format reports
│   └── pdf/       # PDF format reports
├── screenshots/    # Test screenshots  
├── videos/        # Test recordings
├── tests/         # Generated test files
├── metrics/       # Test performance metrics
│   └── metrics_data/ # Raw metrics data
├── .env          # Environment configuration
├── conftest.py   # Test configuration
├── pytest.ini    # Pytest configuration
└── README.md     # Project documentation
```

### Configuration
Create a `.env` file in your project root with these settings:
```
# Browser configuration
BROWSER_TYPE=chromium  # chromium, firefox, webkit
BROWSER_HEADLESS=false
BROWSER_RECORD_VIDEO=true
BROWSER_TIMEOUT=30000

# AI model configuration
LLM_API_KEY=your-api-key-here
LLM_MAX_TOKENS=4096

# Test execution configuration
RETRY_MAX_RETRIES=2
RETRY_ON_NETWORK=true
```
