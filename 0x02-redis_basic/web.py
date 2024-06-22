#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""

import requests
import redis
from typing import Optional


def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The content of the response from the URL.
    """
    r = redis.Redis()

    # Increment the access count
    count_key = f"count:{url}"
    count = r.incr(count_key)
    r.expire(count_key, 10)  # Set the expiration time to 10 seconds

    # Check and return cached content if available
    cache_key = f"cached:{url}"
    cached_content: Optional[bytes] = r.get(cache_key)
    if cached_content:
        return cached_content.decode("utf-8")

    # Fetch new content if not cached
    response = requests.get(url)
    html_content = response.text

    # Cache the new content
    r.set(cache_key, html_content, ex=10)
    return html_content


if __name__ == "__main__":
    # Test with http://google.com
    print(get_page("http://google.com"))
