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
    # Connect to Redis
    r = redis.Redis()

    # Debugging: Check connection to Redis
    try:
        r.ping()
    except redis.ConnectionError as e:
        raise RuntimeError("Could not connect to Redis server") from e

    # Increment the access count
    count_key = f"count:{url}"
    count = r.get(count_key)
    if count is None:
        count = 0
    else:
        count = int(count)
    count += 1
    r.set(count_key, count, ex=10)

    # Debugging: Log the access count
    print(f"Access count for {url}: {count}")

    # Check and return cached content if available
    cache_key = f"cached:{url}"
    cached_content: Optional[bytes] = r.get(cache_key)
    if cached_content:
        print(f"Cache hit for {url}")
        return cached_content.decode("utf-8")

    # Fetch new content if not cached
    response = requests.get(url)
    html_content = response.text

    # Debugging: Log the response status
    print(f"Fetched content for {url} with status {response.status_code}")

    # Cache the new content
    r.set(cache_key, html_content, ex=10)
    return html_content


if __name__ == "__main__":
    # Test with http://google.com
    print(get_page("http://google.com"))
