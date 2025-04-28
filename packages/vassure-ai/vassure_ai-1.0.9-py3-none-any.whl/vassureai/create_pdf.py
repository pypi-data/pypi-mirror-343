"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_test_pdf():
    pdf_path = 'input_pdfs/create_deviation.pdf'
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Starting Y position
    y = 800
    
    # Write test case title
    c.drawString(72, y, 'Test Case: Create deviation')
    y -= 20  # Move down for next line
    
    # Test steps
    steps = [
        'Navigate to "https://login.veevavault.com/auth/login" url',
        'Enter "Vault.Admin@vaultbasics-automation.com" in username text box',
        'Click continue button',
        'Enter "SPOTLINE@veeva1234" in password text box',
        'Click log in button',
        'wait for network idle',
        'Click select vault dropdown',
        'Select "QualityBasicsDryRun25R1 (vaultbasics-automation.com)" from dropdown options',
        'wait for network idle',
        'Click document workspace tab collection menu',
        'Select "QMS" from menu items',
        'Verify "QMS" menu item selected successfully',
        'Click quality events menu',
        'Click deviations sub menu from quality events menu',
        'wait for network idle',
        'Verify "All Deviations" title is displayed',
        'Click create button',
        'wait for network idle',
        'Verify "Create Deviation" title is displayed'
    ]
    
    # Write each step
    for i, step in enumerate(steps, 1):
        c.drawString(72, y, f"{i}. {step}")
        y -= 20  # Move down for next line
    
    c.save()

if __name__ == "__main__":
    create_test_pdf()