"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Metrics Reporter Module for VAssureAI Framework
Handles collection, aggregation and reporting of test execution metrics
Provides functionality for generating performance and test execution reports
"""

import os
import json
import time
import psutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from .monitoring import monitor
from ..utils.logger import logger

class MetricsReporter:
    """Handles collection and storage of test execution metrics"""
    
    def __init__(self):
        self.metrics_dir = os.path.dirname(os.path.abspath(__file__))
        self.metrics_data_dir = os.path.join(self.metrics_dir, "metrics_data")
        os.makedirs(self.metrics_dir, exist_ok=True)
        os.makedirs(self.metrics_data_dir, exist_ok=True)
        
    def _get_system_metrics(self) -> Dict:
        """Get current system metrics"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
                "disk_usage_percent": disk.percent,
                "disk_free_gb": disk.free / (1024 * 1024 * 1024)
            }
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {str(e)}")
            return {}

    def export_metrics(self, test_name: str) -> bool:
        """Export metrics for a specific test to files"""
        try:
            # Get test metrics from monitor
            test_runs = monitor.metrics_history.get(test_name, [])
            if not test_runs:
                logger.warning(f"No metrics found for test: {test_name}")
                return False

            # Export metrics for each test run
            for test_run in test_runs:
                self.save_test_metrics(test_name, test_run)

            # Generate performance report for this test
            self.save_execution_summary()
            return True

        except Exception as e:
            logger.error(f"Failed to export metrics for {test_name}: {str(e)}")
            return False
        
    def save_test_metrics(self, test_name: str, test_run: object) -> str:
        """Save metrics for a single test run"""
        try:
            # Create metrics filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{timestamp}.json"
            filepath = os.path.join(self.metrics_data_dir, filename)
            
            # Collect metrics
            metrics = {
                "test_name": test_name,
                "timestamp": timestamp,
                "duration": test_run["duration"] if isinstance(test_run, dict) else getattr(test_run, "duration", 0),
                "status": test_run["status"] if isinstance(test_run, dict) else getattr(test_run, "status", "UNKNOWN"),
                "success_rate": test_run["success_rate"] if isinstance(test_run, dict) else getattr(test_run, "success_rate", 0),
                "system_metrics": self._get_system_metrics(),
                "steps": []
            }
            
            # Add step-level metrics
            steps = test_run["steps"] if isinstance(test_run, dict) else getattr(test_run, "steps", [])
            for step in steps:
                step_metrics = {
                    "name": step["step_name"] if isinstance(step, dict) else getattr(step, "step_name", "Unknown"),
                    "status": step["status"] if isinstance(step, dict) else getattr(step, "status", "UNKNOWN"),
                    "duration": step["duration"] if isinstance(step, dict) else getattr(step, "duration", 0),
                    "error": step.get("error", None) if isinstance(step, dict) else getattr(step, "error", None)
                }
                metrics["steps"].append(step_metrics)
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(metrics, f, indent=2)
                
            logger.info(f"Saved test metrics to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save test metrics: {str(e)}")
            return None
            
    def save_execution_summary(self) -> str:
        """Save summary metrics for all tests"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"execution_summary_{timestamp}.json"
            filepath = os.path.join(self.metrics_data_dir, filename)
            
            summary = {
                "timestamp": timestamp,
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "total_duration": 0,
                "average_duration": 0,
                "success_rate": 0,
                "system_metrics": self._get_system_metrics(),
                "tests": {}
            }
            
            # Collect metrics from monitor
            for test_name, test_runs in monitor.metrics_history.items():
                test_metrics = []
                for test_run in test_runs:
                    summary["total_tests"] += 1
                    
                    status = test_run["status"] if isinstance(test_run, dict) else getattr(test_run, "status", "UNKNOWN")
                    
                    if status == "COMPLETED":
                        summary["passed_tests"] += 1
                    else:
                        summary["failed_tests"] += 1
                    
                    duration = test_run["duration"] if isinstance(test_run, dict) else getattr(test_run, "duration", 0)
                    success_rate = test_run["success_rate"] if isinstance(test_run, dict) else getattr(test_run, "success_rate", 0)
                    
                    summary["total_duration"] += duration
                    test_metrics.append({
                        "duration": duration,
                        "status": status,
                        "success_rate": success_rate
                    })
                
                summary["tests"][test_name] = test_metrics
            
            # Calculate averages
            if summary["total_tests"] > 0:
                summary["average_duration"] = summary["total_duration"] / summary["total_tests"]
                summary["success_rate"] = (summary["passed_tests"] / summary["total_tests"]) * 100
            
            # Save to file
            with open(filepath, 'w') as f:
                json.dump(summary, f, indent=2)
                
            logger.info(f"Saved execution summary to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to save execution summary: {str(e)}")
            return None

    def get_trend_analysis(self, test_name: str) -> Dict:
        """Analyze performance trends for a test"""
        try:
            # Get test metrics files for this test
            metrics_files = sorted([f for f in os.listdir(self.metrics_data_dir) 
                                 if f.startswith(f"{test_name}_")])
            
            if not metrics_files:
                return None
                
            # Load metrics data
            metrics_data = []
            for file in metrics_files[-10:]:  # Analyze last 10 runs
                with open(os.path.join(self.metrics_data_dir, file)) as f:
                    metrics_data.append(json.load(f))
                    
            if not metrics_data:
                return None
                
            # Calculate trends
            trends = {
                "needs_attention": False,
                "duration_trend": self._calculate_trend([m["duration"] for m in metrics_data]),
                "success_rate_trend": self._calculate_trend([m["success_rate"] for m in metrics_data]),
                "memory_trend": self._calculate_trend([m["system_metrics"]["memory_usage_percent"] for m in metrics_data])
            }
            
            # Check for significant regressions
            if (trends["duration_trend"].get("change", 0) > 20 or  # 20% slower
                trends["success_rate_trend"].get("change", 0) < -10 or  # 10% less successful
                trends["memory_trend"].get("change", 0) > 30):  # 30% more memory
                trends["needs_attention"] = True
                
            return trends
            
        except Exception as e:
            logger.error(f"Failed to analyze trends for {test_name}: {str(e)}")
            return None

    def _calculate_trend(self, values: List[float]) -> Dict:
        """Calculate trend metrics for a series of values"""
        if not values or len(values) < 2:
            return {}
            
        recent_avg = sum(values[-3:]) / min(3, len(values))  # Average of last 3
        old_avg = sum(values[:-3]) / max(1, len(values)-3)  # Average of rest
        
        if old_avg == 0:  # Avoid division by zero
            percent_change = 0
        else:
            percent_change = ((recent_avg - old_avg) / old_avg) * 100
            
        return {
            "recent_avg": round(recent_avg, 2),
            "old_avg": round(old_avg, 2),
            "change": round(percent_change, 2),
            "alert": abs(percent_change) > 20  # Alert if change > 20%
        }

    def get_performance_data(self) -> str:
        """Get performance data for charts"""
        data = {
            "labels": [],
            "durations": []
        }
        
        for test_name, test_runs in monitor.metrics_history.items():
            for run in test_runs:
                data["labels"].append(test_name)
                duration = run["duration"] if isinstance(run, dict) else getattr(run, "duration", 0)
                data["durations"].append(round(duration, 2))
        
        return json.dumps(data)

    def get_trend_data(self) -> str:
        """Get trend data for charts"""
        data = {
            "dates": [],
            "rates": []
        }
        
        # Get all summary files
        summary_files = sorted([f for f in os.listdir(self.metrics_data_dir) 
                             if f.startswith("execution_summary_")])
        
        for file in summary_files[-10:]:  # Get last 10 executions
            with open(os.path.join(self.metrics_data_dir, file)) as f:
                summary = json.load(f)
                date = datetime.strptime(summary["timestamp"], "%Y%m%d_%H%M%S")
                data["dates"].append(date.strftime("%Y-%m-%d %H:%M"))
                data["rates"].append(round(summary["success_rate"], 2))
        
        return json.dumps(data)

# Global instance
metrics_reporter = MetricsReporter()