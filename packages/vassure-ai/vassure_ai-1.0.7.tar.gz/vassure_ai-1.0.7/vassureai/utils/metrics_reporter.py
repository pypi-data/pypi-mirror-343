"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Metrics Reporter Module for VAssureAI Framework
Handles collection, analysis and reporting of test execution metrics including:
- Performance metrics
- Test execution times
- Resource utilization
- Success/failure statistics
"""

import time
import json
import logging
from datetime import datetime

class MetricsReporter:
    def __init__(self):
        self.start_time = time.time()
        self.end_time = None
        self.success_count = 0
        self.failure_count = 0
        self.execution_times = []
        self.resource_utilization = []

    def report_success(self, exec_time, resources):
        self.success_count += 1
        self.execution_times.append(exec_time)
        self.resource_utilization.append(resources)

    def report_failure(self, exec_time, resources):
        self.failure_count += 1
        self.execution_times.append(exec_time)
        self.resource_utilization.append(resources)

    def generate_report(self):
        self.end_time = time.time()
        total_time = self.end_time - self.start_time
        report = {
            "total_time": total_time,
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "average_execution_time": sum(self.execution_times) / len(self.execution_times) if self.execution_times else 0,
            "resource_utilization": self.resource_utilization
        }
        return json.dumps(report, indent=4, default=str)

    def save_report(self, file_path):
        report = self.generate_report()
        with open(file_path, 'w') as report_file:
            report_file.write(report)
        logging.info(f"Report saved to {file_path}")