#!/usr/bin/env python3
"""
Setup script for CodexFix.
"""

from setuptools import find_packages, setup

# For consistency with other Python projects, we use setup.py
# but actual configuration is in pyproject.toml
if __name__ == "__main__":
    setup(
        packages=find_packages(),
    )
