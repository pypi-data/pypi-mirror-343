from setuptools import setup, find_packages

setup(
    name="puzzle-subway-mcp-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastmcp>=2.2.3",
        "httpx>=0.28.1",
    ],
    author="Puzzle",
    author_email="data-puzzle@sk.com",
    description="A FastMCP server for subway congestion information",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/puzzle-subway-mcp-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "puzzle-subway-mcp-server=main:main",
        ],
    },
) 