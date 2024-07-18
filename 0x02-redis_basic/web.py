#!/usr/bin/env python3
""" expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

redis_client = redis.Redis()


def cache_page(expiration=10):
    """
    Decorator that caches the output of a function based on the URL parameter.

    Parameters:
    - expiration (int): The expiration time in seconds for the cache
    (default is 10 seconds)

    Returns:
    - Callable: The decorated function that caches its output
    """
    def decorator(func):
        @wraps(func)
        def wrapper(url: str):
            cached_page = r.get(f"cache:{url}")
            if cached_page:
                return cached_page.decode('utf-8')
            page_content = func(url)
            redis_client.setex(f"cache:{url}", expiration, page_content)
            return page_content
        return wrapper
    return decorator


def count_access(func):
    @wraps(func)
    def wrapper(url: str):
        redis_client.incr(f"count:{url}")
        return func(url)
    return wrapper


@cache_page(expiration=10)
@count_access
def get_page(url: str) -> str:
    """
    Obtain the HTML content of a particular URL

    Parameters:
    - url (string): The URL to obtain HTML content from

    Returns:
    - string: The HTML content
    """
    response = requests.get(url)
    return response.text
