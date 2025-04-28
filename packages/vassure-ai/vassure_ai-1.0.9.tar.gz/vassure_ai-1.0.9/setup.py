"""
-----------------------
Author: Sukumar Kutagulla (Read-only)
Designation: Test Automation Architect (Read-only)
Copyright (c) 2025. All Rights Reserved.
-----------------------
"""

from setuptools import setup, find_namespace_packages
import os

# Function to read requirements.txt
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Create documentation directories if they don't exist
for doc_dir in ['docs/readme', 'docs/technical', 'docs/user']:
    os.makedirs(doc_dir, exist_ok=True)

# Copy documentation files to docs directory if they exist
doc_files = {
    'README': ['README.md', 'README.html', 'README.pdf', 'README.jpeg', 'README.png'],
    'technicalguide': ['technicalguide.md', 'technicalguide.html', 'technicalguide.pdf', 'technicalguide.jpeg', 'technicalguide.png'],
    'userguide': ['userguide.md', 'userguide.html', 'userguide.pdf', 'userguide.jpeg', 'userguide.png']
}

for doc_type, files in doc_files.items():
    target_dir = f'docs/{"readme" if doc_type == "README" else "technical" if "technical" in doc_type else "user"}'
    for file in files:
        src = file if doc_type == "README" else file
        dst = os.path.join(target_dir, file)
        if os.path.exists(src) and not os.path.exists(dst):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                import shutil
                shutil.copy2(src, dst)
            except:
                pass

setup(
    name="vassure_ai",
    version="1.0.9",
    packages=find_namespace_packages(where="src", include=["vassureai*"]),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        'vassureai': [
            'docs/readme/*',
            'docs/technical/*',
            'docs/user/*',
            'templates/*',
            'metrics/metrics_data/*.json',
            'userguide/*',
            'pytest.ini',
            'README.*'
        ]
    },
    data_files=[
        ('docs/readme', [f'docs/readme/{f}' for f in os.listdir('docs/readme')] if os.path.exists('docs/readme') else []),
        ('docs/technical', [f'docs/technical/{f}' for f in os.listdir('docs/technical')] if os.path.exists('docs/technical') else []),
        ('docs/user', [f'docs/user/{f}' for f in os.listdir('docs/user')] if os.path.exists('docs/user') else [])
    ],
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "vassure=vassureai.cli:cli",
        ],
    },
    python_requires=">=3.8",
    author="Sukumar Kutagulla",
    author_email="sukumar.kutagulla@vassureai.com",
    description="VAssureAI Test Automation Framework",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ]
)