from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smear_data_api",
    version="1.0.3",
    description="A Python package for interacting with the SMEAR API and processing data for continuous period.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Abdur Rahman",
    author_email="abdur.rahman@helsinki.fi",
    url="https://github.com/airdipu/SMEAR-data-api",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)