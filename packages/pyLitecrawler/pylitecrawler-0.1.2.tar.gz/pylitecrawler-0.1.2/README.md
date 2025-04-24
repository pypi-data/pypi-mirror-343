# pyLitecrawler

**pyLitecrawler** is a lightweight Python package for scraping, crawling, and analyzing both JavaScript and non-JavaScript websites.

## Features

- Scrape text from JS-rendered or static sites
- Depth-2 internal crawling
- Check URL response status (async)
- Detect if JavaScript content has rendered

## Installation

```bash
pip install -e .
```

## Usage

```python
from pylitecrawler import scrape_text_from_url, crawl_depth_2
```

## License

This project is licensed under the MIT License.
