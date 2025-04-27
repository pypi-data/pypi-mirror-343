from setuptools import setup, find_packages

setup(
    name="mcp_query",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mcp_query = mcp_query.mcp_query:main",
        ],
    },
    author="Alvin Veroy",
    author_email="me@alvin.tech",
    description="A tool to query Context7 MCP server for documentation",
    long_description=open("README.md").read() if open("README.md", errors="ignore") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/alvinveroy/mcp_query",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)