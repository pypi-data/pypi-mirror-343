```markdown
"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------

VAssureAI Framework Technical Guide
Version: 1.0.9
"""

# VAssureAI Framework Technical Guide

## Development Setup

### Git Hooks Installation
To ensure all Python and Markdown files maintain the required headers, install the pre-commit hook:

```bash
# From your project root
cp scripts/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit
```

### File Protection
All Python (.py) and Markdown (.md) files in this project must contain the following header:

```
"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
-----------------------
"""
```

This header is automatically added to:
- All new files created through the framework
- Files generated from PDF processing
- Existing files when running `vassure run`

### Project Structure
When installing the framework via pip and running `vassure init`, the following structure is created:

```
project/
├── input_pdfs/         # Place PDF files here for processing
├── logs/              # Test execution logs
├── reports/           # Generated test reports
├── screenshots/       # Test screenshots
├── videos/           # Test execution recordings
├── tests/            # Test files
├── pytest.ini        # PyTest configuration
├── requirements.txt  # Project dependencies
├── README.md         # Project overview and quick start guide
├── README.html       # HTML version of project overview
├── README.pdf        # PDF version of project overview
├── README.jpeg       # Project overview diagram
├── technicalguide.md  # Technical documentation
├── technicalguide.html # HTML version of technical guide
├── technicalguide.pdf  # PDF version of technical guide
├── technicalguide.jpeg # Technical architecture diagram
├── userguide.md      # User documentation
├── userguide.html    # HTML version of user guide
├── userguide.pdf     # PDF version of user guide
└── userguide.jpeg    # User guide workflow diagram
```

### Development Guidelines
1. All new Python and Markdown files must include the mandatory header
2. The pre-commit hook will prevent commits of files without proper headers
3. When generating new files from PDFs, file descriptions are automatically added below the header
4. Use the framework's built-in utilities for file creation to ensure consistency

### Framework Components
VAssureAI follows a modular architecture with several interconnected components:

```
VAssureAI/
├── core.py                 # Core framework initialization
├── start_framework.py      # Entry point script
├── conftest.py             # Global pytest configuration
├── actions/                # Custom test actions
├── input_pdfs/             # PDF test specifications
├── tests/                  # Test scripts 
├── utils/                  # Framework utilities
│   ├── base_test.py        # Base test class
│   ├── conftest.py         # Pytest fixtures
│   ├── config.py           # Configuration manager
│   ├── logger.py           # Logging system
│   ├── pdfgenerator.py     # PDF report generator
│   ├── test_generator.py   # Test script generator
│   └── utilities.py        # Common utilities
├── browser_use/            # Browser automation
│   ├── agent/              # Automation agent
│   └── controller/         # Browser controller
├── metrics/                # Performance metrics
└── templates/              # Code templates
```

The framework uses a layered architecture:

1. **Presentation Layer**: CLI interface and reporting
2. **Business Logic Layer**: Test generation and execution
3. **Integration Layer**: AI and browser automation
4. **Infrastructure Layer**: Logging, metrics, and utilities

## Entry Points

### `start_framework.py`

This is the main entry point for the framework. It:

1. Sets up the Python path
2. Initializes directories
3. Starts the PDF watcher if requested
4. Provides the main CLI interface

```python
# Main entry point in start_framework.py
def main():
    # Parse command line arguments
    # Initialize the framework
    # Start watching PDFs or begin test execution
    pass
```

### `core.py`

Contains the core initialization logic:

```python
async def init_framework():
    # Create required directories
    # Initialize configuration
    # Setup logging
    pass

def start_framework(pdf_dir: str, watch: bool = True):
    # Initialize framework
    # Start PDF watcher or process specific PDF
    # Handle exceptions
    pass
```

## Core Modules

### `conftest.py`

Global pytest configuration for the framework. It:

1. Registers custom pytest markers
2. Sets up global fixtures
3. Configures asyncio settings
4. Ensures required directories exist

```python
def pytest_configure(config):
    # Add custom markers
    # Create required directories
    pass
```

### `base_test.py`

The foundation class for all tests in the framework:

```python
class BaseTest:
    """Base class for VAssureAI test implementations"""
    
    @pytest.fixture(autouse=True)
    def setup_base(self):
        # Initialize test environment
        # Setup logging
        # Configure browser
        pass
        
    async def _execute_test(self, test_steps, test_name):
        # Initialize test agent
        # Execute each step
        # Capture results
        # Generate reports
        pass
```

## Test Generation Flow

The test generation process follows these steps:

1. **PDF Detection**: The framework monitors the `input_pdfs/` directory for new files
2. **PDF Parsing**: When a new PDF is detected, it extracts test steps and metadata
3. **Test Script Generation**: Creates a Python test script using the template
4. **Test Registration**: Registers the new test with pytest

Key components involved:

```python
# In test_generator.py
def start_pdf_watcher(pdf_dir, watch=True):
    # Set up file watcher or process single file
    # Call parse_pdf_and_create_test for each PDF
    pass
    
def parse_pdf_and_create_test(pdf_path):
    # Extract test metadata and steps from PDF
    # Format test steps for script
    # Generate test script using template
    pass
```

The generated test script inherits from `BaseTest` and contains:

1. Test metadata
2. Test steps as plain text
3. Implementation of test execution method

## Test Execution Flow

### Initialization Phase

1. **pytest startup**: pytest loads conftest.py and registers fixtures
2. **Test discovery**: pytest finds all test classes and methods
3. **Fixture setup**: Global fixtures are initialized

### Setup Phase

For each test:

1. **Environment initialization**: `setup_base` fixture is called
2. **Test-specific setup**: `setup_test` method is called
3. **Browser initialization**: Browser agent is configured

### Execution Phase

1. **Test method execution**: The test's main method is called
2. **Step execution**: Each step is processed by the AI agent
3. **Browser automation**: Browser actions are performed
4. **Result verification**: Assertions verify expected outcomes

### Teardown Phase

1. **Browser cleanup**: Browser connections are closed
2. **Resource cleanup**: Temporary resources are released
3. **Report generation**: Test reports are created

Key components:

```python
# In base_test.py
async def _execute_test(self, test_steps, test_name):
    try:
        # Initialize AI agent
        agent = Agent(browser_settings, llm_client)
        
        # Execute each step
        for step in test_steps:
            await self._execute_step(agent, step)
            
        # Generate final report
        return self._generate_report()
    except Exception as e:
        # Handle exceptions, retry if configured
```

## AI Integration

The framework integrates with LLMs for test execution and interpretation:

1. **Initialization**: LLM client is set up with API keys and configuration
2. **Step Interpretation**: Test steps are sent to the LLM for parsing
3. **Action Generation**: LLM determines the appropriate browser actions
4. **Self-healing**: LLM handles unexpected conditions by generating alternative actions

Key components:

```python
# In utilities.py
def initialize_llm(model_name=None, api_key=None):
    # Set up LLM client with appropriate configuration
    # Handle API authentication
    # Return configured client
    pass

# In agent/service.py
class Agent:
    async def execute_step(self, step_text):
        # Send step to LLM for interpretation
        # Convert LLM response to browser actions
        # Execute browser actions
        # Verify results
        pass
```

## Browser Automation

The framework uses Playwright for browser automation:

1. **Browser Setup**: Configure browser instance with appropriate settings
2. **Page Navigation**: Handle navigation events and timeouts
3. **Element Interaction**: Locate and interact with page elements
4. **Visual Verification**: Take screenshots and perform visual comparisons

Key components:

```python
# In controller_setup.py
def register_controller(browser_type=None, headless=None):
    # Create browser context with specified settings
    # Configure viewport, timeout, etc.
    # Return controller instance
    pass

# In agent/service.py
class Agent:
    async def _perform_browser_action(self, action):
        # Validate action parameters
        # Execute browser command
        # Handle edge cases
        # Return execution results
        pass
```

## Reporting and Metrics

The framework generates comprehensive reports and metrics:

1. **Test Reports**: HTML and PDF reports with test results
2. **Screenshots**: Visual evidence of test steps
3. **Videos**: Recorded browser sessions
4. **Logs**: Detailed execution logs
5. **Metrics**: Performance and reliability metrics

Key components:

```python
# In pdfgenerator.py
class TestReport:
    def generate_report(self):
        # Collect test results
        # Format test data
        # Generate report with appropriate template
        # Save to reports directory
        pass

# In metrics/metrics_reporter.py
def collect_metrics(test_name, start_time, end_time, status):
    # Calculate execution time
    # Record memory usage
    # Measure browser performance
    # Store in metrics database
    pass
```

## Configuration System

Configuration is managed through multiple layers:

1. **Default values**: Hard-coded defaults in `config.py`
2. **Environment variables**: Configuration through `.env` file
3. **Command line**: Override options via CLI arguments
4. **Test-specific**: Per-test configuration via markers

Key components:

```python
# In config.py
class Config:
    class browser:
        type = os.getenv("BROWSER_TYPE", "chromium")
        headless = to_bool(os.getenv("BROWSER_HEADLESS", "false"))
        record_video = to_bool(os.getenv("BROWSER_RECORD_VIDEO", "true"))
        
    class llm:
        model = os.getenv("LLM_MODEL", VASSURE_AI_MODEL)
        api_key = os.getenv("LLM_API_KEY", None)
        
    class retry:
        max_retries = int(os.getenv("RETRY_MAX_RETRIES", 2))
        delay = int(os.getenv("RETRY_DELAY", 5))
```

## Extension Points

The framework provides several extension points:

### Custom Actions

Create custom actions by adding methods to `actions/custom_actions.py`. These are automatically discovered and available to the agent.

```python
# In custom_actions.py
def perform_custom_login(agent, username, password):
    """Custom login action for specific application"""
    # Execute specialized login flow
    pass
```

### Test Hooks

Add pre/post test hooks via pytest fixtures in your conftest.py:

```python
@pytest.fixture(autouse=True)
def custom_setup_teardown():
    # Pre-test setup code
    yield
    # Post-test teardown code
```

### Browser Extensions

Extend browser capabilities by registering custom browser handlers:

```python
# Register custom handler for file downloads
def register_download_handler(page):
    page.on("download", handle_download)
```

## Troubleshooting

### Debugging Techniques

1. **Enable debug logging**: Set `LOG_LEVEL=DEBUG` in `.env`
2. **Run with visible browser**: Set `BROWSER_HEADLESS=false` in `.env`
3. **Step-by-step execution**: Set `BROWSER_SLOW_MO=100` for slow-motion execution

### Common Issues

1. **Browser Failures**: Usually due to timing issues or element selectors
   - Solution: Increase timeouts or use more robust selectors
2. **AI Interpretation Issues**: LLM may misinterpret complex test steps
   - Solution: Simplify step descriptions or use custom actions
3. **Performance Bottlenecks**: Slow execution in parallel tests
   - Solution: Adjust resource allocation or reduce browser instances

### Diagnostic Tools

```python
# Enable in-depth diagnostics
@pytest.mark.diagnostics
def test_with_diagnostics():
    # Test will run with extra instrumentation
    pass
```

## Conclusion

This technical guide provides a comprehensive overview of the VAssureAI framework architecture and implementation. By understanding these internal components and their interactions, developers can effectively extend the framework or contribute to its development.

For API references and detailed class documentation, please refer to the source code documentation comments.

## Environment Variables
The framework supports the following environment variables:

```
# Browser Configuration
VASSURE_BROWSER_TYPE=chromium|firefox|webkit
VASSURE_BROWSER_HEADLESS=true|false
VASSURE_BROWSER_SLOWMO=0
VASSURE_BROWSER_DEVTOOLS=true|false

# AI Configuration
VASSURE_AI_MODEL=ai_model
VASSURE_AI_API_KEY=your_api_key
VASSURE_AI_TEMPERATURE=0.7
VASSURE_AI_MAX_TOKENS=2048

# Test Configuration
VASSURE_MAX_RETRIES=3
VASSURE_RETRY_DELAY=5000
VASSURE_SCREENSHOT_ON_FAILURE=true
VASSURE_VIDEO_RECORDING=true
VASSURE_PARALLEL_TESTS=4

# Logging Configuration
VASSURE_LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
VASSURE_LOG_FORMAT=text|json
VASSURE_LOG_DIR=logs/
```

## Advanced Features

### Custom Action Development
Create custom actions by implementing the IAction interface:

```python
from vassureai.interfaces import IAction
from vassureai.types import ActionResult

class CustomAction(IAction):
    def __init__(self):
        self.name = "custom_action"
        self.description = "Performs a custom action"
        
    async def execute(self, params: dict) -> ActionResult:
        # Implementation
        pass
        
    def validate(self, params: dict) -> bool:
        # Validation logic
        pass
```

### Plugin System
Extend framework capabilities through plugins:

```python
from vassureai.plugins import VAssurePlugin

class CustomPlugin(VAssurePlugin):
    def __init__(self):
        super().__init__("custom_plugin", "1.0.0")
        
    def initialize(self):
        # Plugin initialization
        pass
        
    def teardown(self):
        # Cleanup
        pass
```

### Advanced Browser Automation
Complex browser interactions:

```python
async def handle_dynamic_content(page):
    # Wait for network idle
    await page.wait_for_load_state("networkidle")
    
    # Handle lazy loading
    await page.evaluate("""
        window.scrollTo(0, document.body.scrollHeight);
    """)
    
    # Wait for specific condition
    await page.wait_for_function("""
        () => document.querySelectorAll('.item').length > 10
    """)
```

### PDF Processing Pipeline

1. **PDF Loading**
```python
def load_pdf(path: str) -> PDFDocument:
    with open(path, 'rb') as file:
        parser = PDFParser(file)
        doc = PDFDocument(parser)
        return doc
```

2. **Text Extraction**
```python
def extract_text(pdf: PDFDocument) -> str:
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    
    for page in PDFPage.create_pages(pdf):
        interpreter.process_page(page)
        
    return retstr.getvalue()
```

3. **Test Step Parsing**
```python
def parse_steps(text: str) -> List[TestStep]:
    steps = []
    current_step = None
    
    for line in text.split('\n'):
        if is_step_header(line):
            if current_step:
                steps.append(current_step)
            current_step = TestStep()
        elif current_step:
            current_step.add_line(line)
            
    return steps
```

### Advanced Testing Features

#### Parallel Test Execution
```python
@pytest.mark.parallel
def test_parallel():
    """Tests marked with parallel will run concurrently"""
    pass

# Configuration in pytest.ini
[pytest]
markers =
    parallel: mark test to run in parallel
    slow: mark test as slow running
    flaky: mark test as flaky
```

#### Test Retry Logic
```python
class RetryableTest(BaseTest):
    @retry(max_attempts=3, delay=5)
    async def execute_with_retry(self):
        try:
            await self._execute_test()
        except RetryableException as e:
            self.logger.warning(f"Retrying due to: {e}")
            raise
```

#### Advanced Reporting
```python
class EnhancedReporter:
    def __init__(self):
        self.results = []
        self.metrics = {}
        
    def add_result(self, test_result: TestResult):
        self.results.append(test_result)
        self._update_metrics(test_result)
        
    def generate_report(self) -> str:
        template = self._load_template()
        return template.render(
            results=self.results,
            metrics=self.metrics,
            summary=self._generate_summary()
        )
```

### Self-Healing Capabilities

1. **Element Location Strategy**
```python
class ElementLocator:
    def __init__(self):
        self.strategies = [
            CSSStrategy(),
            XPathStrategy(),
            TextStrategy(),
            AIStrategy()
        ]
        
    async def find_element(self, page, selector):
        for strategy in self.strategies:
            try:
                element = await strategy.find(page, selector)
                if element:
                    return element
            except Exception:
                continue
        raise ElementNotFoundError(selector)
```

2. **AI-Based Recovery**
```python
class AIRecovery:
    def __init__(self, ai_client):
        self.ai_client = ai_client
        
    async def recover_from_failure(self, error, context):
        # Get alternative actions from AI
        alternatives = await self.ai_client.get_alternatives(
            error=error,
            context=context
        )
        
        # Try alternatives
        for action in alternatives:
            try:
                result = await action.execute()
                if result.success:
                    return result
            except Exception:
                continue
                
        raise UnrecoverableError(error)
```

### Performance Optimization

1. **Resource Management**
```python
class ResourceManager:
    def __init__(self):
        self.browser_pool = []
        self.max_browsers = 4
        
    async def get_browser(self):
        if len(self.browser_pool) < self.max_browsers:
            browser = await playwright.chromium.launch()
            self.browser_pool.append(browser)
            return browser
        return self.browser_pool[0]  # Round-robin
```

2. **Memory Management**
```python
class MemoryOptimizer:
    def cleanup_resources(self):
        gc.collect()
        self._close_unused_browsers()
        self._clear_screenshot_cache()
```

### Security Features

1. **Credential Management**
```python
class CredentialManager:
    def __init__(self):
        self.keyring = SystemKeyring()
        
    def store_credentials(self, service, username, password):
        encrypted = self._encrypt(password)
        self.keyring.set_password(service, username, encrypted)
```

2. **Security Headers**
```python
class SecurityMiddleware:
    def __init__(self):
        self.headers = {
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'X-Content-Type-Options': 'nosniff'
        }
        
    async def apply_security_headers(self, page):
        await page.set_extra_http_headers(self.headers)
```

## Deployment

### Docker Support
```dockerfile
FROM python:3.8-slim

# Install browser dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

# Install framework
RUN pip install vassure-ai

# Set environment variables
ENV VASSURE_BROWSER_TYPE=chromium
ENV VASSURE_BROWSER_HEADLESS=true

# Copy project files
COPY . /app
WORKDIR /app

CMD ["vassure", "run"]
```

### CI/CD Integration
Example GitHub Actions workflow:
```yaml
name: VAssure Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install vassure-ai
      - name: Run tests
        run: |
          vassure run
```

## Monitoring and Metrics

### Prometheus Integration
```python
class MetricsCollector:
    def __init__(self):
        self.test_duration = Summary(
            'test_duration_seconds',
            'Time spent executing tests'
        )
        self.test_results = Counter(
            'test_results_total',
            'Test execution results',
            ['result']
        )
```

### Grafana Dashboard
Example dashboard configuration for monitoring test executions:
```json
{
  "dashboard": {
    "id": null,
    "title": "VAssure Test Metrics",
    "panels": [
      {
        "title": "Test Duration",
        "type": "graph",
        "datasource": "Prometheus",
        "targets": [
          {
            "expr": "rate(test_duration_seconds_sum[5m])"
          }
        ]
      }
    ]
  }
}
```

## API Reference

### Core Classes

#### TestExecutor
Main class responsible for test execution:
```python
class TestExecutor:
    """Handles test execution and lifecycle management"""
    
    async def execute(self, test_spec: TestSpec) -> TestResult:
        """Execute a single test specification"""
        pass
        
    async def execute_batch(self, specs: List[TestSpec]) -> BatchResult:
        """Execute multiple test specifications"""
        pass
```

#### TestGenerator
Handles test script generation:
```python
class TestGenerator:
    """Generates test scripts from specifications"""
    
    def generate(self, spec: TestSpec) -> str:
        """Generate a test script from specification"""
        pass
        
    def validate(self, script: str) -> bool:
        """Validate generated test script"""
        pass
```