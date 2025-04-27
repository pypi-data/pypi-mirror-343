"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Load Testing Module for VAssureAI Framework
Provides functionality for performance and load testing
Handles concurrent user simulation and performance metrics collection
"""

import time
import asyncio
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from ..utils.logger import logger

@dataclass
class LoadTestResult:
    """Load test execution results"""
    start_time: datetime
    end_time: datetime
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_response_time: float
    peak_response_time: float
    requests_per_second: float
    errors: List[str]
    performance_metrics: Dict[str, float]

class LoadTester:
    """Handles load test execution and metrics collection"""
    
    def __init__(self):
        self.results = []
        
    async def run_load_test(self, test_func, num_users: int, duration: int) -> LoadTestResult:
        """Run a load test with specified number of users and duration"""
        start_time = datetime.now()
        tasks = []
        results_queue = asyncio.Queue()
        
        # Create user tasks
        for i in range(num_users):
            task = asyncio.create_task(
                self._run_user_session(i, test_func, duration, results_queue)
            )
            tasks.append(task)
        
        # Wait for all tasks to complete
        await asyncio.gather(*tasks)
        
        # Process results
        total_requests = 0
        successful_requests = 0
        failed_requests = 0
        total_response_time = 0
        peak_response_time = 0
        errors = []
        
        while not results_queue.empty():
            result = await results_queue.get()
            total_requests += 1
            if result["success"]:
                successful_requests += 1
                total_response_time += result["response_time"]
                peak_response_time = max(peak_response_time, result["response_time"])
            else:
                failed_requests += 1
                errors.append(result["error"])
        
        end_time = datetime.now()
        test_duration = (end_time - start_time).total_seconds()
        
        result = LoadTestResult(
            start_time=start_time,
            end_time=end_time,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            average_response_time=total_response_time / total_requests if total_requests > 0 else 0,
            peak_response_time=peak_response_time,
            requests_per_second=total_requests / test_duration if test_duration > 0 else 0,
            errors=errors,
            performance_metrics=self._get_performance_metrics()
        )
        
        self.results.append(result)
        return result
        
    async def _run_user_session(self, user_id: int, test_func, duration: int, results_queue: asyncio.Queue) -> None:
        """Run a single user session"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                func_start = time.time()
                await test_func(user_id)
                response_time = time.time() - func_start
                
                await results_queue.put({
                    "success": True,
                    "response_time": response_time,
                    "error": None
                })
                
            except Exception as e:
                await results_queue.put({
                    "success": False,
                    "response_time": 0,
                    "error": str(e)
                })
                
            # Small delay between requests
            await asyncio.sleep(0.1)
            
    def _get_performance_metrics(self) -> Dict[str, float]:
        """Get system performance metrics during load test"""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            return {
                "cpu_usage_percent": cpu_percent,
                "memory_usage_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024)
            }
        except Exception as e:
            logger.error(f"Failed to collect performance metrics: {str(e)}")
            return {}