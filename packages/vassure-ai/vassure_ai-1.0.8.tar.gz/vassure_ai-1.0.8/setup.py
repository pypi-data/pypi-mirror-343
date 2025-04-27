from setuptools import setup, find_packages

setup(
    name="vassure_ai",
    version="1.0.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pytest>=7.4.3",
        "pytest-asyncio>=0.21.1",
        "pytest-html>=4.1.1",
        "langchain>=0.0.352",
        "langchain-google-genai>=0.0.6",
        "pypdf2>=3.0.1",
        "python-dotenv>=1.0.0",
        "jinja2>=3.1.2",
        "pydantic>=2.5.2",
    ],
    entry_points={
        "console_scripts": [
            "vassure=vassure_ai.start_framework:main",
        ],
    },
)