"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------
"""

# VAssureAI Framework Project

## Overview
This project uses the VAssureAI framework for automated web testing. VAssureAI combines the power of AI with robust browser automation to create reliable, maintainable tests with minimal coding effort.

## Project Structure
```
project_root/
├── input_pdfs/           # Place your test specification PDFs here
├── tests/                # Auto-generated and custom test files
├── reports/              # Test execution reports
│   ├── html/            # HTML format reports
│   └── pdf/             # PDF format reports
├── screenshots/          # Test execution screenshots
├── videos/               # Browser recording videos
├── logs/                # Test execution logs
├── metrics/             # Test performance metrics
│   └── metrics_data/    # Raw metrics data
├── .env                 # Environment configuration
├── conftest.py          # Test configuration
├── pytest.ini           # Pytest configuration
└── README.md            # Project documentation
```

## Getting Started

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Virtual environment (recommended)
- Chrome/Chromium browser
- PDF reader

### Installation

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install the VAssureAI framework:
```bash
pip install vassure-ai
```

3. Initialize your project structure:
```bash
vassure init
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

### Using the Framework

There are several ways to use the framework:

#### Using the Interactive Mode (Recommended)

1. Start the interactive CLI mode:
```bash
vassure interactive
```

2. Follow the menu prompts to:
   - Create/Update Tests from PDF files
   - Execute existing tests
   - Configure test execution options

This interactive mode is especially helpful for new users or when you prefer a guided experience rather than remembering CLI commands.

#### Direct Command Line Usage

1. Process PDF files to generate tests:
```bash
vassure watch-pdfs
```

2. Run all tests:
```bash
vassure run
```

3. Run tests with specific options:
```bash
vassure run --parallel 3 --html-report
```

### Creating Tests

#### From PDF Specifications
VAssureAI can automatically generate test scripts from PDF test specifications:

1. Place your test specification PDFs in the `input_pdfs` folder
2. Use the interactive mode or run the PDF watcher to auto-generate tests:
```bash
vassure interactive
# Select option 1: Create/Update Tests from PDF
```
or
```bash
vassure watch-pdfs
```

#### Writing Custom Tests
You can also write custom tests by extending the BaseTest class:

```python
import pytest
from vassureai.utils.base_test import BaseTest

class TestMyFeature(BaseTest):
    """Test custom feature"""

    @pytest.fixture(autouse=True)
    def setup_test(self, setup_base):
        self.test_name = "test_my_feature"
        return self

    def get_all_test_steps(self):
        return [
            "1. Navigate to 'https://example.com'",
            "2. Click on the 'Login' button",
            "3. Enter 'username' in the username field",
            "4. Enter 'password' in the password field",
            "5. Click the 'Submit' button",
            "6. Verify that 'Welcome' text is displayed"
        ]

    @pytest.mark.asyncio
    async def test_my_feature(self):
        test_steps = self.get_all_test_steps()
        result = await self._execute_test(test_steps, "My Feature Test")
        assert result is not None
```

### Running Tests

Run tests using the interactive mode:
```bash
vassure interactive
# Select option 2: Execute Existing Tests
```

Or run directly using command line:

Run all tests:
```bash
vassure run --html-report
```

Run a specific test:
```bash
vassure run --test-dir tests/test_my_feature.py --html-report
```

Run tests in parallel:
```bash
vassure run --parallel 4 --html-report
```

## Key Features

### AI-Powered Test Execution
VAssureAI uses AI to interpret test steps and interact with the browser intelligently, making tests more resilient to UI changes.

### Interactive Mode
A menu-driven interface that simplifies test creation and execution without remembering command line arguments.

### Visual Validation
The framework can capture screenshots at each test step and perform visual validation.

### Comprehensive Reporting
Detailed HTML and PDF reports are generated after test execution, providing insights into test results and performance metrics.

### Test Parallelization
Tests can be run in parallel for faster execution times.

## Troubleshooting

### Common Issues

1. **Test not finding elements**
   - Ensure the element selectors are correct
   - Try increasing the timeout settings

2. **Test execution is slow**
   - Consider running tests in headless mode
   - Use parallel execution with the `--parallel` option

3. **AI model not working correctly**
   - Check your API key configuration
   - Ensure you have internet connectivity

4. **Interactive mode not working**
   - Ensure you have the latest version of the framework
   - Check that your Python environment is correctly set up

### Getting Help
For more detailed information, refer to the VAssureAI documentation:
https://github.com/Spotline-Inc/VAssureAI

## License
This project is licensed under the MIT License - see the LICENSE file for details.