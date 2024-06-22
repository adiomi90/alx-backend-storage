#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""

import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis connection
try:
    r = redis.Redis()
    r.ping()  # Test connection
except redis.ConnectionError:
    raise RuntimeError("Failed to connect to Redis. Make sure Redis is running on localhost:6379.")


def cache_page(func: Callable) -> Callable:
    """
    Decorator to cache the page content and track the access count.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        # Increment the access count
        count_key = f"count:{url}"
        r.incr(count_key)
        r.expire(count_key, 10)  # Set the expiration time to 10 seconds

        # Check and return cached content if available
        cache_key = f"cached:{url}"
        cached_content = r.get(cache_key)
        if cached_content:
            return cached_content.decode("utf-8")

        # Fetch new content if not cached
        html_content = func(url)

        # Cache the new content
        r.set(cache_key, html_content, ex=10)
        return html_content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response
    and tracking the request.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        str: The content of the response from the URL.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    # Test with http://slowwly.robertomurray.co.uk to simulate a slow response
    test_url = "http://slowwly.robertomurray.co.uk/delay/\
                5000/url/http://www.google.com"
    print(get_page(test_url))

    # Print count to verify increment
    count_key = f"count:{test_url}"
    count = r.get(count_key)
    if count:
        print(f"Access count for {test_url}: {int(count)}")
