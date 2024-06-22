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
    count = r.get(count_key)
    if count is None:
        count = 0
    else:
        count = int(count)
    count += 1
    r.set(count_key, count, ex=10)

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
