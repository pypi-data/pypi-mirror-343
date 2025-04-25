"""
Setup script for SAM Local Watcher.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sam-local-watcher",
    version="0.1.0",
    author="AWS SAM Team",
    author_email="your.email@example.com",
    description="A utility for watching and syncing AWS SAM local development files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sam-local-watcher",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "watchdog>=2.1.0",
        "cfn-flip>=1.3.0",
        "pyyaml>=5.1",
    ],
    entry_points={
        "console_scripts": [
            "sam-watcher=sam_local_watcher.cli:main",
        ],
    },
)
