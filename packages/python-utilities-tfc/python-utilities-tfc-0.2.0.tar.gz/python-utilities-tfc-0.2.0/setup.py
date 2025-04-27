from setuptools import setup, find_packages

# Read the README.md file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="python-utilities-tfc",           
    version="0.2.0",                        
    author="Umar Khan",
    author_email="umar.khan@thecloudmania.com",
    description="Utility functions to work with Terraform Cloud and manage Terraform state.",
    long_description=long_description,
    long_description_content_type="text/markdown",  
    project_urls={                        
        "Bug Tracker": "https://github.com/yourusername/python-utilities-tfc/issues",
    },
    classifiers=[                          
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",     
        "Operating System :: OS Independent",
    ],
    package_dir={"": "utilities"},         
    packages=find_packages(where="utilities"),
    python_requires=">=3.11",
    install_requires=[
        "requests",
    ],
)
