#!/usr/bin/env python3
""" A class definition for redis cache """
import requests
import redis


def get_page(url: str) -> str:
    """_summary_

    Args:
        url (str): _description_

    Returns:
        str: _description_
    """
    r = redis.Redis()
    count_key = f"count:{url}"
    count = r.get(count_key)
    if count is None:
        count = 0
    else:
        count = int(count)
    count += 1
    r.set(count_key, count, ex=10)
    cache_key = f"cached:{url}"
    cached_content = r.get(cache_key)
    if cached_content:
        return cached_content.decode("utf-8")
    response = requests.get(url)
    html_content = response.text
    r.set(cache_key, html_content, ex=10)
    return html_content
