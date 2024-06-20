#!/usr/bin/env python3
"""Module to fetch and cache a webpage's HTML content using Redis."""

import requests
import redis
from typing import Optional

# Initialize Redis client globally
r = redis.Redis()


def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache it.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the URL.
    """
    count_key = f"count:{url}"
    cache_key = f"cached:{url}"

    # Increment the access count for the URL
    r.incr(count_key)

    # Check if the content is already cached
    cached_content: Optional[bytes] = r.get(cache_key)
    if cached_content:
        return cached_content.decode("utf-8")

    # Fetch the content from the URL
    response = requests.get(url)
    html_content = response.text

    # Cache the content with an expiration time of 10 seconds
    r.set(cache_key, html_content, ex=10)

    return html_content


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay\
            /5000/url/http://www.example.com"
    print(get_page(url))
    print(get_page(url))
