"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README.md with proper encoding
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="vassure-ai",
    version="1.0.5",
    packages=find_packages(),  # Changed from find_packages(where="src")
    # Removed package_dir={"": "src"} since package is now at root level
    include_package_data=True,
    install_requires=[
        "browser-use>=0.1.41",
        "pytest>=8.3.5",
        "pytest-asyncio>=0.26.0",
        "pytest-html>=4.1.1",
        "pytest-metadata>=3.1.1",
        "pytest-timeout>=2.3.1",
        "pytest-xdist>=3.6.1",
        "python-dotenv>=1.0.0",
        "langchain>=0.1.0",
        "langchain-google-genai>=0.0.10", 
        "pydantic>=2.10.0",
        "psutil>=5.9.0",
        "plotly>=5.18.0",
        "reportlab>=4.0.0",
        "pillow>=10.0.0",
        "PyPDF2>=3.0.0",
        "watchdog>=3.0.0",
        "Jinja2>=3.1.0",
        "click>=8.0.0"
    ],
    package_data={
        "vassureai": [
            "userguide/*.html",
            "userguide/*.md",
            "userguide/*.pdf",
            "userguide/*.png",
            "userguide/*.jpeg",
            "README.html",
            "README.md",
            "utils/**/*",
            "templates/**/*",
            "actions/**/*",
            "metrics/**/*",
            "tests/**/*"
        ]
    },
    entry_points={
        "console_scripts": [
            "vassure=vassureai.cli:main",
        ],
    },
    author="Sukumar Kutagulla",
    author_email="automationsukumar@gmail.com",
    description="VAssureAI Test Automation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vassure-ai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: BDD",
    ],
    python_requires=">=3.8",
)