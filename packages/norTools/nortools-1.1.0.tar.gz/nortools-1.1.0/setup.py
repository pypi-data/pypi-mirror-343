from setuptools import setup, find_packages

setup(
    name="norTools",
    version="1.1.0",  # Increment the version number
    description="A Python package for Dam, Dictor, and ScreenOpp utilities",
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
