from setuptools import setup, find_packages

setup(
    name="moneymcp",
    version="0.1.1",
    description="A financial analysis MCP server that provides tools for comprehensive market data analysis",
    author="easyllms",
    author_email="contract@easyllms.com",
    packages=find_packages(),
    install_requires=[
        "yfinance",
        "fastmcp",
        "finnhub-python",
        "fredapi",
        "pandas",
        "pydantic",
    ],
    entry_points={
        "console_scripts": [
            "mymcp=mymcp.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 
