"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------

PDF Generator Module for VAssureAI Framework
Handles PDF report generation and manipulation including:
- Test execution report generation
- PDF merging and splitting
- Adding watermarks and annotations
- PDF content extraction and validation
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, Image, PageBreak
from ..metrics.monitoring import monitor
from ..utils.logger import logger

class TestReport:
    def __init__(self, filename_prefix=None):
        """Initialize consolidated report"""
        os.makedirs('reports/pdf', exist_ok=True)
        prefix = f"{filename_prefix}_" if filename_prefix else ""
        self.filename = os.path.join('reports', 'pdf', f"{prefix}report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        self.doc = SimpleDocTemplate(
            self.filename,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )
        
        # Initialize styles
        self.styles = getSampleStyleSheet()
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2c3e50')
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#3498db')
        ))
        
        self.elements = []
        
    def add_title(self, title=None):
        """Add report title"""
        self.elements.append(Paragraph(
            title or "VAssureAI Test Execution Report",
            self.styles['CustomTitle']
        ))
        self.elements.append(Spacer(1, 0.2*inch))
        
        # Add timestamp
        self.elements.append(Paragraph(
            f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            self.styles['Normal']
        ))
        self.elements.append(Spacer(1, 0.2*inch))
        
    def add_test_summary(self):
        """Add overall test execution summary"""
        self.elements.append(Paragraph("Test Execution Summary", self.styles['CustomHeading']))
        
        summary_data = []
        total_tests = 0
        passed_tests = 0
        
        # Collect metrics from monitor
        for test_name, test_runs in monitor.metrics_history.items():
            for test_run in test_runs:
                total_tests += 1
                if test_run.status == "COMPLETED":
                    passed_tests += 1
                    
                # Add test details to summary
                summary_data.append([
                    test_name,
                    test_run.status,
                    f"{test_run.duration:.2f}s",
                    f"{test_run.success_rate:.1f}%"
                ])
        
        # Create summary table
        if summary_data:
            table = Table(
                [["Test Name", "Status", "Duration", "Success Rate"]] + summary_data,
                colWidths=[2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch],
                style=[
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ]
            )
            self.elements.append(table)
        
        self.elements.append(Spacer(1, 0.2*inch))
        
    def add_detailed_logs(self):
        """Add detailed execution logs"""
        self.elements.append(Paragraph("Detailed Test Logs", self.styles['CustomHeading']))
        
        # Process each test's logs
        for test_name, test_runs in monitor.metrics_history.items():
            for test_run in test_runs:
                # Add test header
                self.elements.append(Paragraph(
                    f"Test: {test_name}",
                    self.styles['Heading3']
                ))
                
                # Add step details
                for step in test_run.steps:
                    step_style = ParagraphStyle(
                        'StepStyle',
                        parent=self.styles['Normal'],
                        leftIndent=20,
                        textColor=colors.HexColor('#27ae60') if step.status == "PASS" 
                                else colors.HexColor('#e74c3c')
                    )
                    
                    # Format step information
                    step_text = f"""
                    Step: {step.step_name}
                    Status: {step.status}
                    Duration: {step.duration:.2f}s
                    {'Error: ' + step.error if step.error else ''}
                    """
                    
                    self.elements.append(Paragraph(step_text, step_style))
                    self.elements.append(Spacer(1, 0.1*inch))
                
                self.elements.append(PageBreak())
    
    def add_step(self, step_name, status, timestamp, screenshot_path=None, error_details=None, video_path=None):
        """Add a test step to the report"""
        step_style = ParagraphStyle(
            'StepStyle',
            parent=self.styles['Normal'],
            leftIndent=20,
            textColor=colors.HexColor('#27ae60') if status == "PASS" 
                    else colors.HexColor('#e74c3c')
        )
        
        # Format step information
        step_text = f"""
        Step: {step_name}
        Status: {status}
        Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
        {'Screenshot: ' + screenshot_path if screenshot_path else ''}
        {'Video: ' + video_path if video_path else ''}
        {'Error: ' + error_details if error_details else ''}
        """
        
        self.elements.append(Paragraph(step_text, step_style))
        self.elements.append(Spacer(1, 0.1*inch))
        
    def generate(self):
        """Generate the consolidated PDF report"""
        try:
            self.add_title()
            self.add_test_summary()
            self.add_detailed_logs()
            
            # Build PDF
            self.doc.build(self.elements)
            logger.info(f"Generated consolidated report: {self.filename}")
            
        except Exception as e:
            logger.error(f"Failed to generate consolidated report: {str(e)}")