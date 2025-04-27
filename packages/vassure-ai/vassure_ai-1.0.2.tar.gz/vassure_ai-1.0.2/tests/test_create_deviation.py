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
from utils.base_test import BaseTest
from utils.logger import logger
from utils.config import Config

@pytest.mark.requires_browser
@pytest.mark.auto_generated
class TestCreateDeviation(BaseTest):
    """
    Test Case: Create deviation
1. Navigate to "https://login.veevavault.com/auth/login" url
2. Enter "Vault.Admin@vaultbasics-automation.com" in username text box
3. Click continue button
4. Enter "SPOTLINE@veeva1234" in password text box
5. Click log in button
6. wait for network idle
7. Click select vault dropdown
8. Select "QualityBasicsDryRun25R1 (vaultbasics-automation.com)" from dropdown options
9. wait for network idle
10. Click document workspace tab collection menu
11. Select "QMS" from menu items
12. Verify "QMS" menu item selected successfully
13. Click quality events menu
14. Click deviations sub menu from quality events menu
15. wait for network idle
16. Verify "All Deviations" title is displayed
17. Click create button
18. wait for network idle
19. Verify "Create Deviation" title is displayed
    """
    
    __test__ = True
    
    @pytest.fixture(autouse=True)
    def setup_test(self, setup_base):
        """Setup test instance"""
        self.test_name = "create_deviation"
        self.retry_attempts = Config.retry.max_retries
        return self
    
    def get_all_test_steps(self):
        """Get all test steps for this test case"""
        return [
            "Here's the test case description converted into a list of specific, automatable test steps:",
            "1.  **Navigate to URL:** Open browser and navigate to \"https://login.veevavault.com/auth/login\".",
            "2.  **Enter Username:** Locate the username text box and enter \"Vault.Admin@vaultbasics-automation.com\".",
            "3.  **Click Continue:** Locate the \"Continue\" button and click it.",
            "4.  **Enter Password:** Locate the password text box and enter \"SPOTLINE@veeva1234\".",
            "5.  **Click Log In:** Locate the \"Log In\" button and click it.",
            "6.  **Wait for Network Idle:** Wait for the network activity to reach an idle state (e.g., no ongoing requests).",
            "7.  **Click Vault Dropdown:** Locate and click the vault selection dropdown.",
            "8.  **Select Vault:** Locate the option \"QualityBasicsDryRun25R1 (vaultbasics-automation.com)\" in the dropdown and select it.",
            "9.  **Wait for Network Idle:** Wait for the network activity to reach an idle state.",
            "10. **Click Document Workspace Tab:** Locate and click the \"Document Workspace\" tab within the tab collection menu.",
            "11. **Select QMS Menu Item:** Locate and select the \"QMS\" menu item.",
            "12. **Verify QMS Selected:** Verify that the \"QMS\" menu item is selected or highlighted, confirming successful selection.",
            "13. **Click Quality Events Menu:** Locate and click the \"Quality Events\" menu.",
            "14. **Click Deviations Sub Menu:** Locate and click the \"Deviations\" sub-menu within the \"Quality Events\" menu.",
            "15. **Wait for Network Idle:** Wait for the network activity to reach an idle state.",
            "16. **Verify All Deviations Title:** Verify that the page title or heading \"All Deviations\" is displayed.",
            "17. **Click Create Button:** Locate and click the \"Create\" button.",
            "18. **Wait for Network Idle:** Wait for the network activity to reach an idle state.",
            "19. **Verify Create Deviation Title:** Verify that the page title or heading \"Create Deviation\" is displayed.",
        ]
    
    @pytest.mark.asyncio
    async def test_execution(self):
        """Execute the test case"""
        logger.info(f"Starting {self.test_name} execution")
        test_steps = self.get_all_test_steps()
        
        # Execute test with retry logic
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