import time
from .utils import fetch_content, clean_html, get_internal_links

def crawl_depth_2(url: str, clean_text: bool = True, max_links: int = 10, delay: float = 1.0) -> dict:
    """
    Crawls the base URL and up to `max_links` internal links (depth 2).

    Args:
        url (str): The base URL to crawl.
        clean_text (bool): If True, cleans HTML and returns text content. Otherwise, returns raw HTML.
        max_links (int): Maximum number of internal links to crawl.
        delay (float): Delay in seconds between crawling each link.

    Returns:
        dict: Mapping of URL -> page content (cleaned or raw HTML).
    """
    visited = set()
    results = {}

    html1 = fetch_content(url)
    if not html1:
        return {"error": f"Failed to fetch URL: {url}"}

    results[url] = clean_html(html1) if clean_text else html1
    visited.add(url)

    internal_links = get_internal_links(url, html1)
    for link in list(internal_links)[:max_links]:
        if link not in visited:
            time.sleep(delay)
            html2 = fetch_content(link)
            visited.add(link)
            if html2:
                results[link] = clean_html(html2) if clean_text else html2

    return results
