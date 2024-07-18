#!/usr/bin/env python3
""" expiring web cache module """

import redis
import requests
from typing import Callable
from functools import wraps

redis_client = redis.Redis()


def wrap_requests(method: Callable) -> Callable:
    """Tracks how many times a particular URL is accessed"""

    @wraps(method)
    def wrapper(*args, **kwargs):
        """Wrapper"""
        url = args[0]
        redis_client.incr(f"count:{url}")
        cached_response = redis_client.get(url)
        if cached_response:
            return cached_response.decode('utf-8')
        result = method(url)
        redis_client.setex(f"{url}, 10, {result}")
        return method(*args, **kwargs)

    return wrapper


@wrap_requests
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
