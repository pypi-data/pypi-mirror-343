from setuptools import setup, find_packages
import os
import re

# Read version from the package without importing it
with open(os.path.join('marqus_manner', 'version.py'), 'r') as f:
    version_match = re.search(r"version_info = ['\"]([^'\"]*)['\"]", f.read())
    version_info = version_match.group(1) if version_match else '0.0.0'

# Read the contents of README.md
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="marqus-manner",
    version=version_info,
    description="Security scanner for Model Context Protocol (MCP) servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Marqus AI",
    author_email="dev-support@marqus.ai",
    url="https://github.com/marqus-ai/marqus-manner",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "rich>=10.0.0",
        "pyjson5>=1.6.0",
        "lark>=1.1.0",
        "pydantic>=2.0.0",
        "aiohttp>=3.8.0",
        "asyncio>=3.4.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "isort>=5.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "build>=0.8.0",
            "twine>=4.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "marqus=marqus_manner.cli.main:run_cli",
        ],
    },
    package_data={
        "marqus_manner": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="security, mcp, aibom, scanning, vulnerability, ai-security",
)