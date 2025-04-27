# setup.py

from setuptools import setup, find_packages

setup(
    name="python_utilities_tfc",         # 📦 your package name
    version="0.1.0",                     # version
    description="Utilities for working with Terraform Cloud",
    author="Umar Khan",
    author_email="umar.khan@thecloudmania.com",
    packages=find_packages(include=["utilities", "utilities.*"]),
    install_requires=[
        "requests",                     
    ],
    python_requires=">=3.11",             
)
