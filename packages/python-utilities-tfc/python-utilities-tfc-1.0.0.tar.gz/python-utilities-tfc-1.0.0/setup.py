from setuptools import setup, find_packages

# Read the README.md file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-utilities-tfc",           
    version="1.0.0",                        
    author="Umar Khan",
    author_email="umar.khan@thecloudmania.com",
    description="Utility functions to work with Terraform Cloud and manage Terraform state.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(include=["tfc_utilities", "tfc_utilities.*"]),  # ✅
    python_requires=">=3.11",
    install_requires=[
        "requests",
    ],
)
