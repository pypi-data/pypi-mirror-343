"""
Setup script for TGrab.

This setup script is designed to be robust and future-proof, ensuring that
TGrab can be installed and used even years after its creation.
"""

import os
import re
from setuptools import setup, find_packages # type: ignore

# Read version from __init__.py with more robust error handling
try:
    with open(os.path.join("tgrab", "__init__.py"), "r", encoding="utf-8") as f:
        content = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            version = version_match.group(1)
        else:
            version = "0.1.0"  # Default version if not found
except Exception as e:
    print(f"Warning: Could not read version from __init__.py: {e}")
    version = "0.1.0"  # Default version

# Read README for long description with error handling
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except Exception as e:
    print(f"Warning: Could not read README.md: {e}")
    long_description = "TGrab - A tool for downloading media from Telegram"

setup(
    name="gibgram",
    version=version,
    description="GibGram: A powerful tool for downloading media from Telegram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Hazrat Mosaddique Ali",
    author_email="mosaddiqx@gmail.com",  # Author's email
    url="https://github.com/mosaddiX/gibgram",  # Updated repository URL
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.8",  # Updated minimum Python version

    # Define dependencies with specific version ranges
    # This ensures compatibility while allowing for security updates
    install_requires=[
        "telethon>=1.28.0,<2.0.0",  # Telegram client library
        "cryptg>=0.4.0,<1.0.0",      # For faster encryption/decryption
        "rich>=13.0.0,<14.0.0",      # For rich terminal output
        "python-dotenv>=1.0.0,<2.0.0",  # For environment variable handling
        "pillow>=10.0.0,<11.0.0",    # For image processing
        "aiohttp>=3.8.0,<4.0.0",     # For async HTTP requests
        "aiofiles>=23.0.0,<24.0.0",  # For async file operations
    ],

    # Define development dependencies
    extras_require={
        "dev": [
            "pytest>=7.0.0,<8.0.0",
            "pytest-asyncio>=0.21.0,<0.22.0",
            "black>=23.0.0,<24.0.0",
            "isort>=5.12.0,<6.0.0",
            "flake8>=6.0.0,<7.0.0",
            "mypy>=1.0.0,<2.0.0",
        ],
    },

    entry_points={
        "console_scripts": [
            "gibgram=tgrab.cli:main",
        ],
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Utilities",
    ],

    keywords="gibgram, telegram, media, download, cli, bot",

    project_urls={
        "Bug Reports": "https://github.com/mosaddiX/gibgram/issues",
        "Source": "https://github.com/mosaddiX/gibgram",
        "Documentation": "https://mosaddix.github.io/gibgram/",
    },
)
