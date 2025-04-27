"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Execution Reporter for VAssureAI Framework
Provides links to execution results, logs and metrics
"""

import os
import glob
import json
from datetime import datetime
from utils.logger import logger

# ANSI color codes for Windows terminal
COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'CYAN': '\033[96m',
    'WHITE': '\033[97m',
    'RESET': '\033[0m'
}

def get_latest_files():
    """Get the latest execution artifacts and documentation"""
    try:
        # Get latest HTML report
        report_path = os.path.abspath("reports/report.html")
        
        # Get latest log file
        log_files = glob.glob("logs/test_run_*.log")
        latest_log = max(log_files, key=os.path.getctime) if log_files else None
        log_path = os.path.abspath(latest_log) if latest_log else None
        
        # Get latest metrics files
        metrics_files = glob.glob("metrics/metrics_data/*.json")
        latest_metrics = max(metrics_files, key=os.path.getctime) if metrics_files else None
        metrics_path = os.path.abspath(latest_metrics) if latest_metrics else None

        # Get documentation files (HTML only)
        userguide_path = os.path.abspath("userguide/userguide.html")
        readme_path = os.path.abspath("README.html")
        
        # Get last 5 test runs data
        recent_metrics = sorted(metrics_files, key=os.path.getctime, reverse=True)[:5] if metrics_files else []
        recent_results = []
        for metric_file in recent_metrics:
            try:
                with open(metric_file, 'r') as f:
                    data = json.load(f)
                    recent_results.append({
                        'timestamp': data.get('timestamp', ''),
                        'passed': data.get('passed', 0),
                        'failed': data.get('failed', 0),
                        'duration': data.get('duration', 0)
                    })
            except Exception:
                continue
        
        return {
            "report": f"file:///{report_path}" if os.path.exists(report_path) else None,
            "log": f"file:///{log_path}" if log_path else None,
            "metrics": f"file:///{metrics_path}" if metrics_path else None,
            "userguide": f"file:///{userguide_path}" if os.path.exists(userguide_path) else None,
            "readme": f"file:///{readme_path}" if os.path.exists(readme_path) else None,
            "recent_results": recent_results
        }
    except Exception as e:
        logger.error(f"Failed to get execution artifacts: {str(e)}")
        return {}

def format_duration(seconds):
    """Format duration in seconds to human readable format"""
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"

def print_execution_summary():
    """Print links to execution artifacts with enhanced display"""
    files = get_latest_files()
    
    print(f"\n{COLORS['CYAN']}VAssureAI Framework Resources{COLORS['RESET']}")
    print("=" * 40)

    # Documentation Section
    print(f"\n{COLORS['WHITE']}Documentation:{COLORS['RESET']}")
    print("-" * 20)
    if files.get("userguide"):
        print(f"User Guide: {files['userguide']}")
    if files.get("readme"):
        print(f"README: {files['readme']}")

    # Latest Execution Artifacts
    print(f"\n{COLORS['WHITE']}Latest Execution Artifacts:{COLORS['RESET']}")
    print("-" * 20)
    if files.get("report"):
        print(f"HTML Report: {files['report']}")
    if files.get("log"):
        print(f"Log File: {files['log']}")
    if files.get("metrics"):
        print(f"Metrics JSON: {files['metrics']}")

    # Recent Test Run History
    if files.get("recent_results"):
        print(f"\n{COLORS['WHITE']}Recent Test Run History:{COLORS['RESET']}")
        print("-" * 20)
        for idx, result in enumerate(files["recent_results"], 1):
            status = f"{COLORS['GREEN']}✓{COLORS['RESET']}" if result['failed'] == 0 else f"{COLORS['RED']}✗{COLORS['RESET']}"
            print(f"{status} Run {idx}: {result['passed']} passed, {result['failed']} failed - Duration: {format_duration(result['duration'])}")