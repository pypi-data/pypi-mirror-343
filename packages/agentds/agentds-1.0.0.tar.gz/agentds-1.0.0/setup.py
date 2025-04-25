"""
Setup script for the agentds package.
"""
from setuptools import setup

setup(
    name="agentds",
    version="1.0.0",
    py_modules=["__init__", "auth", "client", "config", "task"],
    packages=["utils", "examples"],
    package_data={
        "": ["*.txt", "*.md"],
    },
) 