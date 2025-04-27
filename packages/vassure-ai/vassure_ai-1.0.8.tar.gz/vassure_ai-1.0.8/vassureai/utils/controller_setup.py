"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Controller Setup Module for VAssureAI Framework
Handles the initialization and setup of test controllers
Manages test environment configuration and dependencies
"""

from browser_use.agent.service import Agent
from browser_use.controller.service import Controller

def register_controller(agent: Agent) -> Controller:
    """Register custom controller for browser-use agent"""
    controller = Controller()
    return controller