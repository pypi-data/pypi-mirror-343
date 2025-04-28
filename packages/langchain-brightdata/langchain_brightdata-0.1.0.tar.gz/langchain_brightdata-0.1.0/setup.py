from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="langchain-brightdata",
    version="0.1.0",
    author="Bright Data",
    description="Bright Data tools for LangChain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "langchain-core>=0.3.56",
        "pydantic>=2.11.3",
        "requests>=2.32.0",
        "aiohttp>=3.11.0",
    ],
)