from setuptools import setup, find_packages 

with open("app/README.md", "r") as f:
    long_description = f.read()

setup(
    name="testserverhax",
    version="0.1.0",
    description="MCP test server with pip package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "app"},
    packages=find_packages(where="app"),
    author="HA",
    license="MIT",
    install_requires=[
        "uv",
        "mcp",
        "mcp-use",
        "mcp[cli]",
        "langchain-ollama",
        "langchain-openai",
        "langchain-anthropic"
    ],
    extras_require={"dev": ["pytest", "twine"]},
    python_requires=">=3.12",
)