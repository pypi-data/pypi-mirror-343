"""
-----------------------
Author: Sukumar Kutagulla
Designation: Test Automation Architect
-----------------------
"""

# VAssureAI Framework

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

1. Clone the repository
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Using the Framework (Easy Way)

The easiest way to use the framework is through the `start_framework.bat` file:

1. **Start the Framework**:
   - Double-click `start_framework.bat`
   - Or run it from command prompt: `.\start_framework.bat`

2. **Choose Your Action**:
   The batch file will show a menu with two options:
   - `1` - Create/Update Tests from PDF
   - `2` - Execute Existing Tests

3. **For Creating/Updating Tests (Option 1)**:
   - Place your test case PDF files in the `input_pdfs/` folder
   - Choose whether to run tests after generation
   - If running tests, select execution mode:
     - Sequential (Default): Runs tests one by one
     - Parallel: Runs multiple tests simultaneously

4. **For Executing Tests (Option 2)**:
   - Select execution mode (Sequential/Parallel)
   - For parallel execution, specify number of workers
   - The framework will execute all tests and generate reports

5. **View Results**:
   - HTML reports: Open `reports/report.html`
   - Screenshots: Check `screenshots/` folder
   - Video recordings: Available in `videos/` folder
   - Logs: Check `logs/` folder for detailed execution logs

### Advanced Usage (Command Line)

1. Start the framework:
   ```bash
   python start_framework.py
   ```

2. Run specific test:
   ```bash
   pytest tests/test_name.py -v --asyncio-mode=auto
   ```

3. Run all tests:
   ```bash
   pytest -v --asyncio-mode=auto
   ```

## Framework Structure

```
vassureai/
├── actions/                 # Custom test actions
│   ├── __init__.py
│   └── custom_actions.py    # Custom test implementations
├── input_pdfs/             # Test case PDF specifications
│   ├── create_deviation.pdf # Sample test case
│   └── sample_test_cases.pdf # Example test cases
├── logs/                   # Test execution logs
│   └── test_run_*.log      # Timestamped log files
├── metrics/                # Performance metrics data
├── reports/               # Test execution reports
│   ├── assets/           # Report static assets
│   └── pdf/             # PDF format reports
├── screenshots/           # Test execution screenshots
│   └── step_*_*.png      # Step-wise screenshots
├── tests/                # Test implementations
│   ├── __init__.py
│   ├── login_test.py     # Login functionality test
│   └── test_create_deviation.py # Deviation creation test
├── userguide/            # Framework documentation
│   ├── userguide.md     # Detailed user guide
│   ├── userguide.html   # HTML formatted guide
│   ├── userguide.pdf    # PDF version of guide
│   ├── userguide.png    # Guide diagrams/images
│   └── userguide.jpeg   # Guide screenshots
├── utils/                # Framework utilities
│   ├── __init__.py
│   ├── base_test.py      # Base test class
│   ├── config.py         # Configuration management
│   ├── conftest.py       # Pytest configuration
│   ├── controller_setup.py # Browser setup
│   ├── logger.py         # Logging configuration
│   ├── metrics_reporter.py # Test metrics collection
│   ├── monitoring.py     # Test monitoring
│   ├── pdfgenerator.py   # Report generation
│   ├── test_generator.py # Test script generator
│   ├── templates/        # Template files
│   │   └── test_template.py # Test script template
│   └── utilities.py      # Common utilities
├── videos/               # Test execution recordings
├── .env                 # Environment configuration
├── .gitignore           # Git ignore rules
├── create_pdf.py        # PDF creation utility
├── pytest.ini          # Pytest configuration
├── requirements.txt    # Project dependencies
├── start_framework.bat # Windows startup script
└── start_framework.py  # Framework startup script
```

## Creating Tests

1. **From PDF Specifications**:
   - Create a PDF file with your test case
   - Include test title, description, and numbered steps
   - Place the PDF in `input_pdfs/` directory
   - Use Option 1 in `start_framework.bat` to generate test script

2. **Manual Creation**:
   - Create new test file in `tests/` directory
   - Inherit from `BaseTest` class
   - Implement test steps using `common_utilities`

## Test Execution Modes

### Sequential Mode
- Tests run one after another
- Good for debugging and detailed analysis
- Default mode for test execution

### Parallel Mode
- Multiple tests run simultaneously
- Faster execution for large test suites
- Configure number of parallel workers
- Use when tests are independent

## Reports and Artifacts

### Test Reports
- HTML reports with detailed execution status
- Pass/Fail statistics
- Step-by-step execution details
- Screenshots embedded in reports

### Visual Evidence
- Screenshots captured at each step
- Video recordings of test execution
- Helps in debugging and analysis

### Execution Logs
- Detailed logs with timestamps
- Error messages and stack traces
- Performance metrics

## Risks and Dependencies

### Critical Dependencies
1. **LLM Integration**:
   - Current dependency on specific LLM
   - Requires valid API key and stable API service
   - API version compatibility requirements
   - Risk of API changes or deprecation

2. **Browser Dependencies**:
   - Relies on specific browser versions for automation
   - Chrome/Firefox WebDriver compatibility
   - Risk of browser updates breaking automation

3. **Python Environment**:
   - Python 3.11+ requirement
   - Key library dependencies:
     - Pytest and pytest-asyncio for test execution
     - Reportlab for PDF generation
     - Langchain for LLM integration
     - Selenium/Playwright for browser automation

### Potential Risks

1. **AI/LLM Related**:
   - Model response variations affecting test stability
   - API rate limits and costs
   - Model version changes impacting behavior
   - Need for periodic retraining or updates

2. **Test Stability**:
   - Self-healing mechanisms may mask underlying issues
   - Network dependencies for external services
   - Timing-sensitive test steps
   - Browser rendering inconsistencies

3. **Security Considerations**:
   - API key management
   - Test data security
   - Credential handling in environment variables
   - PDF content security

4. **Maintenance Requirements**:
   - Regular updates for browser drivers
   - PDF test case format compatibility
   - Framework component version synchronization
   - Performance monitoring and optimization

### Risk Mitigation Strategies

1. **Version Control**:
   - Lock dependency versions in requirements.txt
   - Regular compatibility testing
   - Documented update procedures

2. **Monitoring and Alerts**:
   - Performance metrics tracking
   - Error rate monitoring
   - Resource usage alerts
   - API usage tracking

3. **Backup Procedures**:
   - Regular backup of test artifacts
   - Version control for test cases
   - Alternative execution paths
   - Fallback mechanisms for critical features

4. **Best Practices**:
   - Regular security audits
   - Performance benchmarking
   - Code review processes
   - Documentation updates

## Documentation

For detailed documentation, see [User Guide](userguide/userguide.md).

## Support

For issues and feature requests, please contact the framework maintainers.

## License

Copyright (c) 2025. All Rights Reserved.
