"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------
"""

# VAssureAI Framework User Guide
Version: 1.0.9

## Introduction
VAssureAI is an intelligent test automation framework that makes it easy to create and run automated tests from PDF specifications. This guide will help you get started and make the most of the framework's features.

## Getting Started

### System Requirements
Before you begin, ensure your system has:
- Windows, macOS, or Linux operating system
- Python 3.8 or newer installed
- Google Chrome or Chromium browser
- PDF reader software
- Stable internet connection

### Installation Steps
1. Open a terminal/command prompt
2. Run: `pip install vassure-ai`
3. Verify installation: `vassure --version`

### Creating Your First Project
1. Create a new directory for your project
2. Open terminal in that directory
3. Run: `vassure init`
4. Follow the on-screen prompts

## Using the Framework

### Preparing Test Specifications
1. Create your test specifications in PDF format
2. Include clear step-by-step test procedures
3. Save PDFs in the `input_pdfs/` folder

### Running Tests
1. Open terminal in your project directory
2. Run: `vassure run`
3. The framework will:
   - Process your PDF specifications
   - Generate test scripts
   - Execute the tests
   - Create reports

### Understanding Test Results
Test results can be found in:
- `reports/` - HTML test reports
- `screenshots/` - Test step screenshots
- `videos/` - Test execution recordings
- `logs/` - Detailed execution logs

## Features

### PDF Processing
- Automatic test script generation from PDFs
- Support for complex test scenarios
- Smart interpretation of test steps

### Test Execution
- Automated browser testing
- Screenshot capture
- Video recording
- Self-healing capabilities

### Reporting
- Detailed HTML reports
- Step-by-step execution logs
- Visual evidence (screenshots/videos)
- Pass/Fail statistics

## Best Practices

### PDF Specifications
- Use clear, concise language
- Include expected results for each step
- Provide test data where needed
- Break complex scenarios into smaller steps

### Project Organization
- Keep PDFs organized in folders
- Use meaningful PDF filenames
- Regularly backup your project
- Review generated reports

### Troubleshooting Tips
- Check logs for detailed error messages
- Verify PDF file permissions
- Ensure stable internet connection
- Update Chrome/Chromium regularly

## Common Issues & Solutions

### Test Generation Issues
- **PDFs not detected**: Verify file permissions and location
- **Parsing errors**: Check PDF formatting and content
- **Missing steps**: Review PDF structure

### Execution Issues
- **Browser errors**: Update Chrome/Chromium
- **Timeout errors**: Check internet connection
- **Element not found**: Verify application state

## Support Resources
- Email: support@vassureai.com
- Documentation: https://docs.vassureai.com
- Community Forum: https://community.vassureai.com

## Glossary
- **PDF Specification**: Test case document in PDF format
- **Test Script**: Generated automation code
- **Self-healing**: Automatic handling of UI changes
- **Test Report**: Summary of test execution results