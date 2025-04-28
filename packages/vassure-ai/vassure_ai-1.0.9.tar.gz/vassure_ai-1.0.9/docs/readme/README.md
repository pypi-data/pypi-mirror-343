"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------
"""

# VAssureAI Framework Developer Guide
Version: 1.0.9

## Quick Start

1. Install via pip:
```bash
pip install vassure-ai
```

2. Initialize project:
```bash
vassure init
```

3. Place test specification PDFs in `input_pdfs/` directory

4. Run tests:
```bash
vassure run
```

## Basic Project Structure
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

## Minimum Requirements
- Python 3.8+
- Chrome/Chromium browser
- PDF reader

## Configuration
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

## Documentation
- See userguide.md for detailed usage instructions
- See technicalguide.md for technical details

## Support
For technical support or questions, please contact support@vassureai.com