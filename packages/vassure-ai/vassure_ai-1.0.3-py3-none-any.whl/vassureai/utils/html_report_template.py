"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

HTML Report Template Handler
"""

from py.xml import html
import pytest
from datetime import datetime
from src.vassureai.metrics.monitoring import monitor
from metrics.metrics_reporter import MetricsReporter
from metrics.load_tester import LoadTestResult

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>VAssureAI Test Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background: linear-gradient(45deg, #2c3e50, #3498db);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .header h1 {
            margin: 0;
            font-size: 24px;
        }
        .summary {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .test-steps {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .step {
            border-left: 4px solid #3498db;
            padding: 10px;
            margin: 10px 0;
            background: #f8f9fa;
        }
        .step.pass {
            border-left-color: #2ecc71;
        }
        .step.fail {
            border-left-color: #e74c3c;
        }
        .screenshot {
            max-width: 100%;
            height: auto;
            margin: 10px 0;
            border-radius: 4px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .error {
            color: #e74c3c;
            background: #fdf2f2;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .logo {
            height: 40px;
            margin-right: 15px;
            vertical-align: middle;
        }
        .timestamp {
            color: #666;
            font-size: 0.9em;
        }
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            color: #666;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            <img src="data:image/png;base64,{logo_base64}" alt="VAssureAI" class="logo">
            VAssureAI Test Report
        </h1>
        <div class="timestamp">Generated: {timestamp}</div>
    </div>

    <div class="summary">
        <h2>Test Summary</h2>
        <div class="metrics">
            <div class="metric-card">
                <h3>Total Tests</h3>
                <p>{total_tests}</p>
            </div>
            <div class="metric-card">
                <h3>Pass Rate</h3>
                <p>{pass_rate}%</p>
            </div>
            <div class="metric-card">
                <h3>Duration</h3>
                <p>{duration}s</p>
            </div>
            <div class="metric-card">
                <h3>Memory Usage</h3>
                <p>{memory_usage} MB</p>
            </div>
        </div>
    </div>

    <div class="test-steps">
        <h2>Test Steps</h2>
        {steps_html}
    </div>

    <div class="footer">
        <p>© 2025 VAssureAI. All rights reserved.</p>
        <p>Author: {author}</p>
    </div>
</body>
</html>
'''

STEP_TEMPLATE = '''
<div class="step {status_class}">
    <h3>{step_name}</h3>
    <div class="timestamp">{timestamp}</div>
    <div class="status">Status: {status}</div>
    {screenshot_html}
    {error_html}
    {video_html}
</div>
'''

SCREENSHOT_TEMPLATE = '''
<img src="{screenshot_path}" alt="Step Screenshot" class="screenshot">
'''

ERROR_TEMPLATE = '''
<div class="error">
    <strong>Error:</strong> {error_message}
</div>
'''

VIDEO_TEMPLATE = '''
<div class="video">
    <a href="{video_path}" target="_blank">View Test Recording</a>
</div>
'''

def create_performance_section(test_name):
    """Create performance metrics section for a test"""
    metrics = monitor.get_test_summary(test_name)
    if not metrics:
        return None
        
    performance_div = html.div(class_="performance-metrics")
    performance_div.append(html.h3("Performance Metrics"))
    
    # Create metrics table
    table = html.table(class_="performance-table")
    headers = html.tr([
        html.th("Metric"),
        html.th("Value")
    ])
    table.append(headers)
    
    # Add metrics rows
    metrics_rows = [
        ("Total Runs", str(metrics.get("total_runs", 0))),
        ("Success Rate", f"{metrics.get('success_rate', 0):.2f}%"),
        ("Average Duration", f"{metrics.get('average_duration', 0):.2f}s"),
        ("Total Network Retries", str(metrics.get("total_network_retries", 0))),
        ("Peak Memory Usage", f"{metrics.get('peak_memory_mb', 0):.2f} MB")
    ]
    
    for metric, value in metrics_rows:
        row = html.tr([
            html.td(metric),
            html.td(value)
        ])
        table.append(row)
        
    performance_div.append(table)
    return performance_div

def create_load_test_section(result: LoadTestResult):
    """Create load test results section"""
    if not result:
        return None
        
    load_test_div = html.div(class_="load-test-results")
    load_test_div.append(html.h3("Load Test Results"))
    
    # Create summary table
    table = html.table(class_="load-test-table")
    headers = html.tr([
        html.th("Metric"),
        html.th("Value")
    ])
    table.append(headers)
    
    # Add load test metrics
    metrics_rows = [
        ("Total Users", str(result.total_users)),
        ("Concurrent Users", str(result.concurrent_users)),
        ("Total Iterations", str(result.total_iterations)),
        ("Duration", f"{result.duration:.2f}s"),
        ("Success Rate", f"{result.success_rate:.2f}%"),
        ("Throughput", f"{result.throughput:.2f} req/s"),
        ("Avg Response Time", f"{result.avg_response_time:.3f}s"),
        ("Peak Memory", f"{result.peak_memory_mb:.2f} MB"),
        ("Network Retries", str(result.network_retries))
    ]
    
    for metric, value in metrics_rows:
        row = html.tr([
            html.td(metric),
            html.td(value)
        ])
        table.append(row)
        
    load_test_div.append(table)
    
    # Add error summary if there are errors
    if result.error_details:
        load_test_div.append(html.h4("Error Summary"))
        error_list = html.ul(class_="error-list")
        for error in result.error_details[:10]:  # Show first 10 errors
            error_list.append(html.li(error))
        if len(result.error_details) > 10:
            error_list.append(
                html.li(f"... and {len(result.error_details) - 10} more errors")
            )
        load_test_div.append(error_list)
        
    return load_test_div

def create_trend_analysis_section(test_name):
    """Create trend analysis section for a test"""
    reporter = MetricsReporter()
    trends = reporter.get_trend_analysis(test_name)
    if not trends:
        return None
        
    trend_div = html.div(class_="trend-analysis")
    trend_div.append(html.h3("Performance Trends"))
    
    if trends.get('needs_attention'):
        warning = html.div(
            html.strong("⚠️ Performance Regression Detected"),
            class_="warning"
        )
        trend_div.append(warning)
    
    # Create trends table
    table = html.table(class_="trends-table")
    headers = html.tr([
        html.th("Metric"),
        html.th("Change"),
        html.th("Trend"),
        html.th("Status")
    ])
    table.append(headers)
    
    # Add trend rows
    for category, data in trends.items():
        if isinstance(data, dict):
            row = html.tr([
                html.td(category.replace('_', ' ').title()),
                html.td(f"{data.get('change_percentage', 0):.2f}%" if 'change_percentage' in data else f"{data.get('change', 0):.2f}"),
                html.td("↑" if data.get('trend') == 'up' else "↓"),
                html.td("⚠️" if data.get('alert') else "✓")
            ])
            table.append(row)
            
    trend_div.append(table)
    return trend_div

def pytest_html_report_title(report):
    """Customize the report title"""
    report.title = "AI Testing Framework Test Report"

def pytest_html_results_table_header(cells):
    """Add custom column headers to the results table"""
    cells.insert(2, html.th("Performance", class_="sortable"))
    cells.insert(3, html.th("Load Test", class_="sortable"))
    cells.pop()  # Remove the links column

def pytest_html_results_table_row(report, cells):
    """Add custom columns to the results table"""
    # Add performance metrics column
    if hasattr(report, "metrics"):
        metrics_summary = f"Success Rate: {report.metrics.get('success_rate', 0):.2f}%"
        if hasattr(report, "performance_warning"):
            metrics_summary = "⚠️ " + metrics_summary
        cells.insert(2, html.td(metrics_summary))
    else:
        cells.insert(2, html.td("N/A"))
        
    # Add load test column
    if hasattr(report, "load_test_result"):
        result = report.load_test_result
        load_test_summary = f"Users: {result.total_users}, Success: {result.success_rate:.1f}%"
        cells.insert(3, html.td(load_test_summary))
    else:
        cells.insert(3, html.td("N/A"))
        
    cells.pop()  # Remove the links column

def pytest_html_results_table_html(report, data):
    """Add custom HTML sections to the report"""
    extra_html = html.div(class_="extra")
    
    # Add performance metrics
    if hasattr(report, "metrics"):
        perf_section = create_performance_section(report.nodeid)
        if perf_section:
            extra_html.append(perf_section)
            
        # Add trend analysis
        trend_section = create_trend_analysis_section(report.nodeid)
        if trend_section:
            extra_html.append(trend_section)
            
    # Add load test results
    if hasattr(report, "load_test_result"):
        load_test_section = create_load_test_section(report.load_test_result)
        if load_test_section:
            extra_html.append(load_test_section)
            
    data.append(extra_html)

def pytest_html_report_data(report):
    """Add custom CSS and JavaScript to the report"""
    report.style_css += """
    .performance-metrics, .trend-analysis, .load-test-results {
        margin: 20px 0;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    .performance-table, .trends-table, .load-test-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
    }
    
    .performance-table th, .performance-table td,
    .trends-table th, .trends-table td,
    .load-test-table th, .load-test-table td {
        padding: 8px;
        border: 1px solid #ddd;
        text-align: left;
    }
    
    .performance-table th, .trends-table th, .load-test-table th {
        background-color: #f5f5f5;
    }
    
    .warning {
        color: #856404;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
    
    .error-list {
        list-style-type: none;
        padding-left: 0;
        margin: 10px 0;
    }
    
    .error-list li {
        color: #721c24;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 8px;
        margin: 5px 0;
        border-radius: 4px;
    }
    
    .chart-container {
        width: 100%;
        max-width: 800px;
        margin: 20px auto;
        padding: 15px;
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    """
    
    # Add Chart.js library
    report.extra_js = [
        'https://cdn.jsdelivr.net/npm/chart.js',
        '''
        // Create charts after the document is loaded
        document.addEventListener('DOMContentLoaded', function() {
            createTestResultsChart();
            createPerformanceChart();
            createTrendChart();
        });
        
        function createTestResultsChart() {
            const ctx = document.getElementById('testResultsChart');
            if (!ctx) return;
            
            const data = window.testData || {
                passed: parseInt(document.querySelector('.passed').textContent),
                failed: parseInt(document.querySelector('.failed').textContent),
                skipped: parseInt(document.querySelector('.skipped').textContent),
                error: parseInt(document.querySelector('.error').textContent)
            };
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['Passed', 'Failed', 'Skipped', 'Error'],
                    datasets: [{
                        data: [data.passed, data.failed, data.skipped, data.error],
                        backgroundColor: ['#2ecc71', '#e74c3c', '#f1c40f', '#95a5a6']
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Test Results Distribution'
                        }
                    }
                }
            });
        }
        
        function createPerformanceChart() {
            const ctx = document.getElementById('performanceChart');
            if (!ctx || !window.performanceData) return;
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: window.performanceData.labels,
                    datasets: [{
                        label: 'Execution Time (seconds)',
                        data: window.performanceData.durations,
                        backgroundColor: '#3498db'
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Test Execution Times'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        function createTrendChart() {
            const ctx = document.getElementById('trendChart');
            if (!ctx || !window.trendData) return;
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: window.trendData.dates,
                    datasets: [{
                        label: 'Success Rate',
                        data: window.trendData.rates,
                        borderColor: '#2ecc71',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Success Rate Trend'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }
        '''
    ]

@pytest.hookimpl(optionalhook=True)
def pytest_html_results_summary(prefix, summary, postfix):
    """Add custom summary section with charts to the report"""
    reporter = MetricsReporter()
    
    # Add Chart.js library
    summary.append(html.script(src="https://cdn.jsdelivr.net/npm/chart.js"))
    
    # Add chart containers
    charts_div = html.div(class_="charts-container")
    
    # Test Results Chart
    results_div = html.div(class_="chart-wrapper")
    results_div.append(html.h3("Test Results Distribution"))
    results_div.append(html.canvas(id="resultsChart"))
    charts_div.append(results_div)
    
    # Duration Chart
    duration_div = html.div(class_="chart-wrapper")
    duration_div.append(html.h3("Test Duration Distribution"))
    duration_div.append(html.canvas(id="durationChart"))
    charts_div.append(duration_div)
    
    summary.append(charts_div)
    
    # Add performance data for charts
    perf_data = reporter.get_performance_data()
    if perf_data:
        summary.append(html.script(f"""
            document.addEventListener('DOMContentLoaded', function() {{
                const resultsCtx = document.getElementById('resultsChart').getContext('2d');
                const durationCtx = document.getElementById('durationChart').getContext('2d');
                
                const passed = parseInt(document.querySelector('.passed').textContent);
                const failed = parseInt(document.querySelector('.failed').textContent);
                const skipped = parseInt(document.querySelector('.skipped').textContent);
                const error = parseInt(document.querySelector('.error').textContent);
                
                new Chart(resultsCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Passed', 'Failed', 'Skipped', 'Error'],
                        datasets: [{{
                            data: [passed, failed, skipped, error],
                            backgroundColor: ['#2ecc71', '#e74c3c', '#f1c40f', '#95a5a6']
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        plugins: {{
                            legend: {{
                                position: 'bottom'
                            }}
                        }}
                    }}
                }});
                
                const perfData = {perf_data};
                new Chart(durationCtx, {{
                    type: 'bar',
                    data: {{
                        labels: perfData.labels,
                        datasets: [{{
                            label: 'Duration (seconds)',
                            data: perfData.durations,
                            backgroundColor: '#3498db'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        scales: {{
                            y: {{
                                beginAtZero: true
                            }}
                        }}
                    }}
                }});
            }});
        """))
    
    # Add custom CSS for charts
    summary.append(html.style("""
        .charts-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin: 20px 0;
            padding: 20px;
        }
        .chart-wrapper {
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .chart-wrapper h3 {
            text-align: center;
            margin-bottom: 15px;
            color: #2c3e50;
        }
        canvas {
            max-height: 300px;
        }
    """))

@pytest.hookimpl(tryfirst=True)
def pytest_html_results_table_html(report, data):
    """Add custom HTML sections to the report"""
    extra_html = html.div(class_="extra")
    
    # Add performance metrics
    if hasattr(report, "metrics"):
        perf_section = create_performance_section(report.nodeid)
        if perf_section:
            extra_html.append(perf_section)
            
        # Add trend analysis
        trend_section = create_trend_analysis_section(report.nodeid)
        if trend_section:
            extra_html.append(trend_section)
            
    # Add load test results
    if hasattr(report, "load_test_result"):
        load_test_section = create_load_test_section(report.load_test_result)
        if load_test_section:
            extra_html.append(load_test_section)
            
    data.append(extra_html)

def pytest_html_report_data(report):
    """Add custom CSS and JavaScript to the report"""
    report.style_css += """
    .performance-metrics, .trend-analysis, .load-test-results {
        margin: 20px 0;
        padding: 15px;
        border: 1px solid #ddd;
        border-radius: 4px;
    }
    
    .performance-table, .trends-table, .load-test-table {
        width: 100%;
        border-collapse: collapse;
        margin: 10px 0;
    }
    
    .performance-table th, .performance-table td,
    .trends-table th, .trends-table td,
    .load-test-table th, .load-test-table td {
        padding: 8px;
        border: 1px solid #ddd;
        text-align: left;
    }
    
    .performance-table th, .trends-table th, .load-test-table th {
        background-color: #f5f5f5;
    }
    
    .warning {
        color: #856404;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 10px;
        margin: 10px 0;
        border-radius: 4px;
    }
    
    .error-list {
        list-style-type: none;
        padding-left: 0;
        margin: 10px 0;
    }
    
    .error-list li {
        color: #721c24;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 8px;
        margin: 5px 0;
        border-radius: 4px;
    }
    """