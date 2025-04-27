"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Pytest Configuration and Fixtures
"""

import json
import pytest
import asyncio
import os
from datetime import datetime

from ..metrics.load_tester import LoadTester
from .logger import logger
from ..metrics.monitoring import monitor
from ..metrics.metrics_reporter import metrics_reporter

def pytest_configure(config):
    """Configure pytest for VAssureAI framework"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "requires_browser: mark test as needing a browser instance"
    )
    config.addinivalue_line(
        "markers", "network_sensitive: mark test as sensitive to network conditions"
    )
    config.addinivalue_line(
        "markers", "load_test: mark test for load testing with parameters"
    )
    config.addinivalue_line(
        "markers", "auto_generated: mark test as auto-generated from PDF"
    )
    
    # Ensure required directories exist
    for dir_name in ['logs', 'reports', 'screenshots', 'metrics', 'videos', 'load_test_results']:
        os.makedirs(dir_name, exist_ok=True)

@pytest.fixture(scope="session")
def metrics_reporter_fixture():
    """Provide a metrics reporter instance for the test session"""
    return metrics_reporter

@pytest.fixture(autouse=True)
def setup_test_monitoring(request):
    """Automatically monitor all tests"""
    test_name = request.node.name
    monitor.start_test(test_name)
    yield
    monitor.end_test()

@pytest.fixture(scope="session", autouse=True)
def cleanup_old_artifacts(request):
    """Clean up old test artifacts before test session"""
    def remove_old_files(directory: str, keep_days: int = 7):
        """Remove files older than keep_days from directory"""
        if not os.path.exists(directory):
            return
            
        current_time = os.stat(directory).st_mtime
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                age_days = (current_time - os.stat(item_path).st_mtime) / (24 * 3600)
                if age_days > keep_days:
                    try:
                        os.remove(item_path)
                        logger.debug(f"Removed old file: {item_path}")
                    except Exception as e:
                        logger.error(f"Failed to remove {item_path}: {str(e)}")
    
    # Clean up old files
    for directory in ['screenshots', 'reports', 'logs', 'metrics', 'videos', 'load_test_results']:
        remove_old_files(directory)
        
    yield
    
    # After test session, generate final reports
    all_tests = list(monitor.metrics_history.keys())
    if all_tests:
        try:
            # Export individual test metrics
            for test_name in all_tests:
                metrics_reporter.export_metrics(test_name)
                
            # Generate combined performance report
            metrics_reporter.save_execution_summary()
            
            # Check for performance regressions
            for test_name in all_tests:
                trends = metrics_reporter.get_trend_analysis(test_name)
                if trends and trends.get('needs_attention'):
                    logger.warning(f"Performance regression detected in {test_name}")
                    for category, data in trends.items():
                        if isinstance(data, dict) and data.get('alert'):
                            logger.warning(f"  - {category}: {data}")
                            
        except Exception as e:
            logger.error(f"Failed to generate final reports: {str(e)}")

@pytest.fixture
def load_test(request):
    """Fixture for load testing a test function"""
    marker = request.node.get_closest_marker("load_test")
    if not marker:
        pytest.skip("Test not marked for load testing")
        
    # Get load test parameters from marker or use defaults
    params = marker.kwargs if marker else {}
    total_users = params.get("total_users", 10)
    iterations_per_user = params.get("iterations_per_user", 1)
    concurrent_users = params.get("concurrent_users", 5)
    ramp_up_time = params.get("ramp_up_time", 0)
    
    # Create load tester instance
    async def run_test():
        test_func = request.function
        tester = LoadTester(test_func)
        result = await tester.run_load_test(
            total_users=total_users,
            iterations_per_user=iterations_per_user,
            concurrent_users=concurrent_users,
            ramp_up_time=ramp_up_time
        )
        
        # Generate load test report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = os.path.join(
            'load_test_results',
            f'load_test_{request.node.name}_{timestamp}.txt'
        )
        report_text = tester.generate_load_test_report(report_file)
        
        # Export detailed results as JSON
        json_file = os.path.join(
            'load_test_results',
            f'load_test_{request.node.name}_{timestamp}.json'
        )
        try:
            with open(json_file, 'w') as f:
                json.dump({
                    'test_name': request.node.name,
                    'parameters': {
                        'total_users': total_users,
                        'iterations_per_user': iterations_per_user,
                        'concurrent_users': concurrent_users,
                        'ramp_up_time': ramp_up_time
                    },
                    'results': {
                        'duration': result.duration,
                        'success_rate': result.success_rate,
                        'throughput': result.throughput,
                        'avg_response_time': result.avg_response_time,
                        'peak_memory_mb': result.peak_memory_mb,
                        'network_retries': result.network_retries,
                        'error_count': len(result.error_details)
                    }
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to export load test results: {str(e)}")
            
        return result
    
    return run_test

@pytest.fixture
def browser_config(request):
    """Provide browser configuration with any custom markers"""
    config = {}
    
    # Get browser settings from markers
    browser_marker = request.node.get_closest_marker("browser")
    if browser_marker:
        config.update(browser_marker.kwargs)
        
    return config