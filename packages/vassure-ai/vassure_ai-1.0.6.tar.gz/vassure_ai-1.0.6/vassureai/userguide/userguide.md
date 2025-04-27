"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------
"""

# VAssureAI Framework User Guide

## Table of Contents
- [What is VAssureAI?](#what-is-vassureai)
- [Quick Start Guide](#quick-start-guide)
- [Creating and Running Tests](#creating-and-running-tests)
- [Understanding Test Results](#understanding-test-results)
- [Troubleshooting](#troubleshooting)

## What is VAssureAI?

VAssureAI is an automated testing tool that helps you test your applications without writing code. You simply write your test steps in a PDF document with plain English, and the framework automatically converts them into working tests.

Key benefits include:
- **No Coding Required**: Create tests using simple English steps
- **AI-Powered Testing**: Tests automatically adapt to small UI changes
- **Visual Results**: Get screenshots and videos of test execution
- **Comprehensive Reports**: Detailed HTML and PDF reports

## Quick Start Guide

### Getting Started in 5 Simple Steps

#### Step 1: Initial Setup (One-time only)
1. **Prerequisites**
   - Make sure Python 3.11+ and Chrome/Firefox are installed on your computer
   - Have your application credentials ready (URL, username, password)

2. **Ask Your Administrator To Set Up The Environment**
   - They will install VAssureAI framework and initialize your project

#### Step 2: Write Your Test Cases
1. **Create a New PDF Document**
   - Use any PDF editor (Microsoft Word/Google Docs + Save as PDF)
   - Follow this simple format:
     ```
     Test Case: [Your Test Name]
     Description: [What the test does]
     
     Steps:
     1. [First action to take]
     2. [Second action to take]
     3. [What to verify]
     ...
     ```

2. **Example Test Case**:
   ```
   Test Case: Login to Application
   Description: Verify user can login successfully
   
   Steps:
   1. Navigate to login page
   2. Enter username in the username field
   3. Click continue button
   4. Enter password in password field
   5. Click login button
   6. Verify dashboard is displayed
   ```

#### Step 3: Generate Tests From Your PDFs
1. **Start the PDF Watcher**
   ```bash
   vassure watch-pdfs
   ```

2. **Add Your Test Cases**
   - Copy your PDF file into the `input_pdfs` folder
   - The framework will automatically detect and process it

#### Step 4: Run Your Tests
1. **Execute Tests**
   ```bash
   vassure run --html-report
   ```

2. **What Happens During Execution**
   - Tests run automatically in the browser
   - Progress is shown in the terminal window
   - Screenshots and videos are captured

#### Step 5: Review Test Results
1. **Open Test Reports**
   - Go to the `reports` folder
   - Open the HTML report in your browser
   - PDF reports are in `reports/pdf` folder

2. **What to Look For**
   - Green ✅ means test passed
   - Red ❌ means test failed
   - Screenshot evidence shows what happened

## Creating and Running Tests

### Best Practices for Writing Tests

1. **Keep Steps Simple**
   - One action per step
   - Be specific about what to click/type
   - Include verification points

2. **Name Things Clearly**
   - Use descriptive test names
   - Mention the feature being tested

3. **Include Verification Steps**
   - Add "Verify" steps to check results
   - Look for specific text or elements

### Common Test Actions

#### Navigation Actions
- "Navigate to [URL]"
- "Click on [button/link]"
- "Select [option] from dropdown"

#### Input Actions
- "Enter [text] in [field]"
- "Upload file [filename]"
- "Check the checkbox"

#### Verification Actions
- "Verify [text] is visible"
- "Verify page title contains [text]"
- "Verify button is enabled"

### Running Your Tests

#### Run All Tests
```bash
vassure run --html-report
```

#### Run a Specific Test
```bash
vassure run -t tests/test_login.py --html-report
```

## Understanding Test Results

### Test Reports

1. **HTML Reports**
   - Overall test summary
   - Step-by-step results
   - Screenshots of key steps
   - Error details for failures

2. **PDF Reports**
   - Formal documentation
   - Suitable for sharing with stakeholders

### Test Artifacts

1. **Screenshots**
   - Find in the `screenshots` folder
   - Named with timestamp and step number
   - Captured during verification steps

2. **Videos**
   - Find in the `videos` folder
   - Full recording of test execution
   - Helpful for debugging complex issues

3. **Logs**
   - Find in the `logs` folder
   - Detailed technical information
   - Useful for troubleshooting

## Troubleshooting

### Common Issues and Solutions

#### Test Not Running?
✓ Check if framework is started (terminal window should be open)  
✓ Verify PDF is in the correct folder (input_pdfs)  
✓ Make sure PDF follows the correct format  

#### Test Failed?
✓ Check screenshots in reports for visual clues  
✓ Review error message in logs  
✓ Verify your test steps match the application's current UI  
✓ Ensure the application is accessible  

#### Getting Help

If you encounter issues you can't resolve:
1. Consult with your test automation administrator
2. Check the detailed logs in the logs folder
3. Provide screenshots and videos of the issue when seeking help