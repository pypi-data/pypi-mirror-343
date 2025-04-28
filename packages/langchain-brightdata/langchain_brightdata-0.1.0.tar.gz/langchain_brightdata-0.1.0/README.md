# LangChain Bright Data Tools

This package integrates Bright Data's services with LangChain.

## Tools Included

- **BrightDataSERP**: Perform search engine queries with geo-targeting
- **BrightDataUnblocker**: Access websites that might be geo-restricted
- **BrightDataWebScraperAPI**: Extract structured data from websites

## Installation

```bash
pip install langchain-brightdata
```

## Usage

```python

from langchain_brightdata import BrightDataSERP

# Initialize the tool with your API key
search_tool = BrightDataSERP(bright_data_api_key="your-api-key")

# Use the tool
results = search_tool.invoke({
    "query": "artificial intelligence news",
    "search_engine": "google",
    "country": "us"
})

```
## Authentication

You'll need a Bright Data API key. You can set it as an environment variable:

```bash
export BRIGHT_DATA_API_KEY="your-api-key"

```

Or pass it directly when initializing the tools.