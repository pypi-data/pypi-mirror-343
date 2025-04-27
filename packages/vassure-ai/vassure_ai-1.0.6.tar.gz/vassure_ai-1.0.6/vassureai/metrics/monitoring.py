"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Test Execution Monitoring for VAssureAI Framework
Tracks test execution progress and metrics in real-time
"""

from datetime import datetime
from typing import Dict, List
from ..utils.logger import logger

class Monitor:
    """Monitors test execution and collects metrics"""
    
    def __init__(self):
        self.metrics_history = {}
        self.current_test = None
        self.current_test_steps = []
        self.current_step = None
        self.step_start_time = None
    
    def start_test(self, test_name: str) -> None:
        """Start monitoring a new test"""
        self.current_test = test_name
        self.current_test_steps = []
        self.metrics_history.setdefault(test_name, [])
        logger.info(f"Started monitoring test: {test_name}")
    
    def start_step(self, step_name: str) -> None:
        """Start monitoring a test step"""
        self.current_step = {
            "step_name": step_name,
            "status": None,
            "start_time": datetime.now(),
            "duration": 0,
            "error": None
        }
        self.step_start_time = datetime.now()
        logger.debug(f"Started step: {step_name}")
        
    def end_step(self, status: str, error: str = None) -> None:
        """End monitoring of current step"""
        if self.current_step:
            duration = (datetime.now() - self.step_start_time).total_seconds()
            self.current_step.update({
                "status": status,
                "duration": duration,
                "error": error
            })
            self.current_test_steps.append(self.current_step)
            logger.debug(f"Completed step: {self.current_step['step_name']} ({status})")
            
    def end_test(self, status: str = None, error: str = None) -> None:
        """End monitoring of current test"""
        if self.current_test:
            duration = sum(step["duration"] for step in self.current_test_steps)
            completed_steps = sum(1 for step in self.current_test_steps if step["status"] == "PASS")
            total_steps = len(self.current_test_steps)
            success_rate = (completed_steps / total_steps * 100) if total_steps > 0 else 0
            
            test_run = type("TestRun", (), {
                "status": status or "COMPLETED",
                "duration": duration,
                "success_rate": success_rate,
                "steps": self.current_test_steps,
                "error": error
            })
            
            self.metrics_history[self.current_test].append(test_run)
            logger.info(f"Completed monitoring test: {self.current_test}")
            
            self.current_test = None
            self.current_test_steps = []
            self.current_step = None
            self.step_start_time = None
            
    def update_memory_usage(self, usage: float) -> None:
        """Update memory usage metrics for current step"""
        if self.current_step:
            self.current_step["memory_usage"] = usage
            
    def get_test_summary(self, test_name: str) -> Dict:
        """Get summary metrics for a test"""
        if test_name not in self.metrics_history:
            return None
            
        test_runs = self.metrics_history[test_name]
        if not test_runs:
            return None
            
        total_runs = len(test_runs)
        successful_runs = sum(1 for run in test_runs if run.status == "COMPLETED")
        total_duration = sum(run.duration for run in test_runs)
        
        return {
            "total_runs": total_runs,
            "success_rate": (successful_runs / total_runs * 100) if total_runs > 0 else 0,
            "average_duration": total_duration / total_runs if total_runs > 0 else 0,
            "total_network_retries": sum(len([s for s in run.steps if "retry" in s["step_name"].lower()]) for run in test_runs),
            "peak_memory_mb": max(
                (max((s.get("memory_usage", 0) for s in run.steps), default=0) for run in test_runs),
                default=0
            )
        }

# Global instance
monitor = Monitor()