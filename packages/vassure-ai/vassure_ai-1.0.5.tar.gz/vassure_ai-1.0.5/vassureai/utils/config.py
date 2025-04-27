"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Configuration Management Module for VAssureAI Framework
Handles framework configuration including:
- Environment settings
- Test execution parameters
- Logging configurations
- Report generation settings
"""

import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class RetryConfig:
    """Retry configuration for test execution"""
    max_retries: int = 3
    retry_delay: int = 2
    retry_on_network_error: bool = True

@dataclass
class BrowserConfig:
    """Browser configuration settings"""
    record_video: bool = True
    video_dir: str = "videos"
    screenshot_dir: str = "screenshots"
    headless: bool = True

@dataclass
class VisualConfig:
    """Visual validation configuration"""
    highlight: bool = True
    screenshot_on_step: bool = True
    screenshot_on_error: bool = True

@dataclass
class VAssureConfig:
    """Main VAssureAI framework configuration"""
    retry: RetryConfig = field(default_factory=RetryConfig)
    browser: BrowserConfig = field(default_factory=BrowserConfig)
    visual: VisualConfig = field(default_factory=VisualConfig)
    log_dir: str = "logs"
    report_dir: str = "reports"
    metrics_dir: str = "metrics"

    @classmethod
    def from_env(cls) -> 'VAssureConfig':
        """Create configuration from environment variables"""
        return cls(
            retry=RetryConfig(
                max_retries=int(os.getenv('VASSURE_MAX_RETRIES', '3')),
                retry_delay=int(os.getenv('VASSURE_RETRY_DELAY', '2')),
                retry_on_network_error=os.getenv('VASSURE_RETRY_ON_NETWORK', 'true').lower() == 'true'
            ),
            browser=BrowserConfig(
                record_video=os.getenv('VASSURE_RECORD_VIDEO', 'true').lower() == 'true',
                headless=os.getenv('VASSURE_HEADLESS', 'true').lower() == 'true'
            ),
            visual=VisualConfig(
                highlight=os.getenv('VASSURE_HIGHLIGHT', 'true').lower() == 'true',
                screenshot_on_step=os.getenv('VASSURE_SCREENSHOT_ON_STEP', 'true').lower() == 'true',
                screenshot_on_error=os.getenv('VASSURE_SCREENSHOT_ON_ERROR', 'true').lower() == 'true'
            )
        )

# Global configuration instance
Config = VAssureConfig.from_env()