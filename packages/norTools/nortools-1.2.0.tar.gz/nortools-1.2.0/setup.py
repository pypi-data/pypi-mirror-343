from setuptools import setup, find_packages
import os

# Read the contents of README.md
with open(os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="norTools",  # Updated module name
    version="1.2.0",  # Increment the version number here
    description="A Python package for Dam, Dictor, and ScreenOpp utilities",
    long_description=long_description,  # Use the contents of README.md
    long_description_content_type="text/markdown",  # Specify the format of the long description
    author="Syed",
    packages=find_packages(),
    install_requires=[
        "flet",  # Add dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
