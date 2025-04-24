from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pyfi-finance",
    version="0.1.0",
    author="K Shivaprasad",
    description="A simple Python package for financial calculations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.0",
        "scipy>=1.5.0",
    ],
    entry_points={
        'console_scripts': [
            'compound-interest=pyfi_finance.cli:compound_interest_cli',
            'option-price=pyfi_finance.cli:option_price_cli',
            'portfolio-optimize=pyfi_finance.cli:portfolio_optimize_cli',
        ],
    },
)