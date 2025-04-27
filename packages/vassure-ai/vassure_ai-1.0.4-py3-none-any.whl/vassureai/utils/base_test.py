"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------
"""

# base_test.py
import pytest
import asyncio
import os
import psutil
from datetime import datetime
from browser_use.agent.service import Agent
from .pdfgenerator import TestReport
from .utilities import initialize_llm, save_screenshot, determine_status, get_timestamp
from .config import Config
from .controller_setup import register_controller
from .logger import logger
from ..metrics.monitoring import monitor
from ..metrics.metrics_reporter import metrics_reporter

class BaseTest:
    """Base class for VAssureAI test implementations"""
    
    __test__ = False  # Tell pytest not to collect this class for tests
    
    @pytest.fixture(autouse=True)
    def setup_base(self):
        """Setup base test instance"""
        self.test_name = None
        self.agent = None
        self.video_path = None
        self.screenshot_steps = []
        
        # Use developer's project directory for all output files
        self.project_root = os.getcwd()  # Developer's project directory
        self.screenshot_dir = os.path.join(self.project_root, "screenshots")
        self.reports_dir = os.path.join(self.project_root, "reports")
        self.videos_dir = os.path.join(self.project_root, "videos")
        self.logs_dir = os.path.join(self.project_root, "logs")
        self.metrics_dir = os.path.join(self.project_root, "metrics")
        
        # Ensure all output directories exist
        os.makedirs(self.screenshot_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        os.makedirs(self.videos_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        os.makedirs(self.metrics_dir, exist_ok=True)
        
        self.llm = initialize_llm()
        self.report = TestReport(
            filename_prefix=self.test_name or self.__class__.__name__,
            output_dir=self.reports_dir  # Use developer's reports directory
        )
        self.test_start_time = None
        
        # Override Config settings to use developer's project directories
        Config.browser.video_dir = self.videos_dir
            
        return self

    def get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / (1024 * 1024)

    async def setup_agent(self, test_steps):
        """Initialize and configure the browser-use agent"""
        if Config.browser.record_video:
            self.video_path = os.path.join(
                self.videos_dir,  # Use developer's videos directory
                f"{self.test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.webm"
            )
            
        # Initialize agent with core required parameters
        self.agent = Agent(
            task=" ".join(test_steps) if isinstance(test_steps, (list, tuple)) else test_steps,
            llm=self.llm,
            max_failures=Config.retry.max_retries,
            retry_delay=Config.retry.retry_delay,
            use_vision=Config.visual.highlight
        )
        
        # Set controller directly
        self.agent.controller = register_controller(self.agent)
        logger.info(f"Initialized test agent for {self.test_name}")
        return self.agent

    async def _execute_test(self, test_steps, title):
        """Execute a test case with given steps and generate a report"""
        self.report.add_title(title)
        self.test_start_time = datetime.now()
        monitor.start_test(self.test_name)
        
        try:
            # Setup agent with custom controller
            agent = await self.setup_agent(test_steps)
            
            # Run the test steps
            logger.info(f"Starting test execution: {self.test_name}")
            history = await agent.run()
            
            # Disable highlighting for screenshots
            if agent.browser_context and hasattr(agent.browser_context, 'page'):
                await agent.browser_context.page.evaluate('''() => {
                    const style = document.createElement('style');
                    style.innerHTML = '*:hover { outline: none !important; }';
                    document.head.appendChild(style);
                }''')
                
        except asyncio.TimeoutError as te:
            error_msg = f"Test execution timed out: {str(te)}"
            logger.error(error_msg)
            monitor.end_test(status="ERROR", error=error_msg)
            self.report.add_step(
                "Test Execution Timeout", 
                "ERROR", 
                datetime.now(), 
                None, 
                error_details=error_msg,
                video_path=self.video_path if Config.browser.record_video else None
            )
            self.report.generate()
            
            # Save metrics for failed test
            metrics_reporter.save_test_metrics(self.test_name, {
                "duration": (datetime.now() - self.test_start_time).total_seconds(),
                "status": "ERROR",
                "success_rate": 0,
                "steps": monitor.current_test_steps if hasattr(monitor, 'current_test_steps') else []
            })
            metrics_reporter.save_execution_summary()
            return None
            
        except Exception as e:
            error_msg = f"Test execution failed: {str(e)}"
            logger.error(error_msg)
            monitor.end_test(status="ERROR", error=error_msg)
            self.report.add_step(
                "Test Execution Error", 
                "ERROR", 
                datetime.now(), 
                None, 
                error_details=str(e),
                video_path=self.video_path if Config.browser.record_video else None
            )
            self.report.generate()
            
            # Save metrics for failed test
            metrics_reporter.save_test_metrics(self.test_name, {
                "duration": (datetime.now() - self.test_start_time).total_seconds(),
                "status": "ERROR",
                "success_rate": 0,
                "steps": monitor.current_test_steps if hasattr(monitor, 'current_test_steps') else []
            })
            metrics_reporter.save_execution_summary()
            return None
            
        finally:
            # Ensure browser cleanup
            await self.cleanup()

        # Process test results with enhanced error handling
        try:
            if not isinstance(test_steps, (list, tuple)):
                test_steps = [test_steps]
                
            completed_steps = 0
            total_steps = len(test_steps)
                
            for idx, (step, history_item) in enumerate(zip(test_steps, history.history)):
                monitor.start_step(step)
                status = determine_status(history_item)
                timestamp = get_timestamp(history_item)
                
                if status == "PASS":
                    completed_steps += 1
                
                # Update memory metrics
                monitor.update_memory_usage(self.get_memory_usage())
                
                # Get error details if any
                error_details = None
                if status == "FAIL":
                    error_details = str(history_item.result[0].error) if history_item.result else "Step failed"
                
                # Handle screenshots with retry logic
                screenshot_path = None
                if (any(keyword in str(step).lower() for keyword in ["verify"]) or 
                    Config.visual.screenshot_on_step or idx in self.screenshot_steps):
                    
                    for retry in range(3):  # Retry screenshots up to 3 times
                        try:
                            if history_item.state and history_item.state.screenshot:
                                await asyncio.sleep(1)
                                screenshot_path = save_screenshot(
                                    history_item.state.screenshot, 
                                    idx, 
                                    self.screenshot_dir
                                )
                                if screenshot_path:
                                    break
                        except Exception as e:
                            if retry == 2:  # Last retry
                                logger.error(f"Screenshot failed after retries: {str(e)}")
                
                # Add step to report with video if it was recorded
                self.report.add_step(
                    step, 
                    status, 
                    timestamp, 
                    screenshot_path,
                    error_details=error_details,
                    video_path=self.video_path if Config.browser.record_video else None
                )
                
                # End step monitoring
                monitor.end_step(status=status, error=error_details)
                
            self.report.generate()
            
            # Calculate success rate
            success_rate = (completed_steps / total_steps) * 100 if total_steps > 0 else 0
            
            # End test monitoring with success
            monitor.end_test(status="COMPLETED")
            
            # Save test metrics
            metrics_reporter.save_test_metrics(self.test_name, {
                "duration": (datetime.now() - self.test_start_time).total_seconds(),
                "status": "COMPLETED",
                "success_rate": success_rate,
                "steps": monitor.current_test_steps if hasattr(monitor, 'current_test_steps') else []
            })
            metrics_reporter.save_execution_summary()
            
            logger.info(f"Test execution completed: {self.test_name}")
            return history.final_result() if hasattr(history, 'final_result') else "Test completed"
            
        except Exception as e:
            error_msg = f"Error processing test results: {str(e)}"
            logger.error(error_msg)
            monitor.end_test(status="ERROR", error=error_msg)
            self.report.add_step(
                "Results Processing Error", 
                "ERROR", 
                datetime.now(), 
                None,
                error_details=str(e),
                video_path=self.video_path if Config.browser.record_video else None
            )
            self.report.generate()
            
            # Save metrics for failed test
            metrics_reporter.save_test_metrics(self.test_name, {
                "duration": (datetime.now() - self.test_start_time).total_seconds(),
                "status": "ERROR", 
                "success_rate": 0,
                "steps": monitor.current_test_steps if hasattr(monitor, 'current_test_steps') else []
            })
            metrics_reporter.save_execution_summary()
            return None

    async def cleanup(self):
        """Clean up browser and other resources"""
        if self.agent and hasattr(self.agent, 'browser_context'):
            try:
                if hasattr(self.agent.browser_context, 'page'):
                    await self.agent.browser_context.page.close()
                if hasattr(self.agent.browser_context, 'browser'):
                    await self.agent.browser_context.browser.close()
                logger.info(f"Browser cleanup completed for {self.test_name}")
            except Exception as e:
                logger.error(f"Browser cleanup failed: {str(e)}")
        self.agent = None