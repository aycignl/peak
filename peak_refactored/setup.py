#!/usr/bin/env python
"""Setup script for PEAK: Explainable Privacy Assistant through Automated Knowledge Extraction."""

from setuptools import setup, find_packages
import os

# Read README for long description
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# Read requirements
def read_requirements(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="peak",
    version="1.0.0",
    author="Ayca Gonul",
    author_email="gonul.ayci@boun.edu.tr",
    description="Explainable Privacy Assistant through Automated Knowledge Extraction",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/aycignl/peak",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "dev": read_requirements("requirements-dev.txt"),
        "test": ["pytest>=6.0", "pytest-cov>=2.0", "pytest-mock>=3.0"],
    },
    entry_points={
        "console_scripts": [
            "peak-train=peak.cli:train_command",
            "peak-predict=peak.cli:predict_command",
            "peak-explain=peak.cli:explain_command",
        ],
    },
    include_package_data=True,
    package_data={
        "peak": ["configs/*.yaml", "templates/*.txt"],
    },
)