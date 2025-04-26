from setuptools import setup, find_packages
import os

# Read README for long description
try:
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Multi-Agent Generator - Generate multi-agent AI code from natural language"

# Read requirements if the file exists, otherwise use a default list
requirements = [
    "streamlit>=1.22.0",
    "crewai>=0.28.0",
    "langchain>=0.1.0",
    "langgraph>=0.0.10",
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
    "pydantic>=2.0.0",
]

try:
    if os.path.exists('requirements.txt'):
        with open('requirements.txt') as f:
            requirements = f.read().splitlines()
except Exception:
    # If there's any issue reading requirements.txt, use the default list
    pass

setup(
    name="multi-agent-generator",
    version="0.1.0",
    description="Generate multi-agent AI teams using CrewAI, LangGraph, and ReAct",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your@email.com",
    url="https://github.com/aakriti1318/multi-agent-generator",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "multi-agent-generator=multi_agent_generator.__main__:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)