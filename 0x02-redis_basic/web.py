#!/bin/usr/env python3
import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
r = redis.Redis()


def cache_response(expiration: int):
    """Decorator to cache the response of a function with a given expiration time."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(url: str) -> str:
            cached_content = r.get(f"cached:{url}")
            if cached_content:
                print("Returning cached content")
                return cached_content.decode('utf-8')
            print("Fetching new content")
            content = func(url)
            r.setex(f"cached:{url}", expiration, content)
            return content
        return wrapper
    return decorator


def count_access(func: Callable):
    """Decorator to count the number of accesses to a URL."""
    @wraps(func)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        r.incr(count_key)
        return func(url)
    return wrapper


@count_access
@cache_response(10)
def get_page(url: str) -> str:
    """Fetch the HTML content of a URL and cache it."""
    response = requests.get(url)
    return response.text


# Example usage
if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
    print(get_page(url))
    print(get_page(url))
    print(r.get(f"count:{url}").decode('utf-8'))
