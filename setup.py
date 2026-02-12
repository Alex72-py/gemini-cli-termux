#!/usr/bin/env python3
"""
Gemini CLI for Termux - Setup Configuration
Author: Alex72-py
License: MIT
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip() 
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]

setup(
    name="gemini-cli-termux",
    version="1.0.0",
    author="Alex72-py",
    author_email="",
    description="Native Gemini AI CLI for Termux on Android",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alex72-py/gemini-cli-termux",
    packages=find_packages(exclude=["tests", "docs"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Communications :: Chat",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Android",
        "Environment :: Console",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gemini-termux=gemini_cli.main:main",
            "gt=gemini_cli.main:main",  # Short alias
        ],
    },
    include_package_data=True,
    package_data={
        "gemini_cli": [
            "data/*.toml",
            "data/*.txt",
        ],
    },
    zip_safe=False,
    keywords="gemini ai cli termux android google generative-ai chatbot",
    project_urls={
        "Bug Reports": "https://github.com/Alex72-py/gemini-cli-termux/issues",
        "Source": "https://github.com/Alex72-py/gemini-cli-termux",
        "Documentation": "https://github.com/Alex72-py/gemini-cli-termux#readme",
    },
)
