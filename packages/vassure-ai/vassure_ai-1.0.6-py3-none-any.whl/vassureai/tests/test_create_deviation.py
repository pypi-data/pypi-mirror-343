"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

Test Suite for Deviation Creation Functionality
Contains test cases to verify the creation and validation of deviations
in the VAssureAI system
"""

import pytest
import datetime
# Fix imports to use relative paths since we moved from src layout
from ..utils.base_test import BaseTest
from ..utils.logger import logger
from ..utils.config import Config

@pytest.mark.requires_browser
@pytest.mark.auto_generated
class TestCreateDeviation(BaseTest):
    """Test Case: Create deviation"""
    
    # Explicitly set this to True to ensure pytest collects this class
    __test__ = True

    @pytest.fixture(autouse=True)
    def setup_test(self, setup_base):
        """Setup test instance"""
        self.test_name = "test_create_deviation"
        self.retry_attempts = Config.retry.max_retries
        return self

    def get_all_test_steps(self):
        """Get all test steps for this test case"""
        return [
            "1.  Navigate to \"https://login.veevavault.com/auth/login\" url",
            "2.  Enter \"Vault.Admin@vaultbasics-automation.com\" in username text box",
            "3.  Click continue button",
            "4.  Enter \"SPOTLINE@veeva1234\" in password text box",
            "5.  Click log in button",
            "6.  wait for network idle",
            "7.  Click select vault dropdown",
            "8.  Select \"QualityBasicsDryRun25R1 (vaultbasics-automation.com)\" from dropdown options",
            "9.  wait for network idle",
            "10. Click document workspace tab collection menu",
            "11. Select \"QMS\" from menu items",
            "12. Verify \"QMS\" menu item selected successfully",
            "13. Click quality events menu",
            "14. Click deviations sub menu from quality events menu",
            "15. wait for network idle",
            "16. Verify \"All Deviations\" title is displayed",
            "17. Click create button",
            "18. wait for network idle",
            "19. Verify \"Create Deviation\" title is displayed"
        ]

    @pytest.mark.asyncio
    async def test_create_deviation(self):
        """Execute the test case"""
        logger.info(f"Starting {self.test_name} execution")
        test_steps = self.get_all_test_steps()

        for attempt in range(self.retry_attempts + 1):
            try:
                result = await self._execute_test(test_steps, f"{self.test_name} Results")
                if result:
                    logger.info(f"{self.test_name} completed successfully")
                    return result
                else:
                    logger.warning(f"{self.test_name} attempt {attempt + 1} failed")
            except Exception as e:
                logger.error(f"{self.test_name} attempt {attempt + 1} failed with error: {str(e)}")
                if attempt == self.retry_attempts:
                    raise

        return None

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])