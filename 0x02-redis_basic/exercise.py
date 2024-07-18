#!/usr/bin/env python3
"""
Module: excercise

Redis module
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Counts how many times methods of the Cache class are called

    Parameters:
    - method (Callable): The method to count

    Returns:
    - Callable: The value returned by the original method
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Conserve the original function’s name, docstring, etc"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs for a particular function

    Parameters:
    - method (Callable): The function to store the history for

    Returns:
    - Callable: The value returned by the original function
    """
    key = method.__qualname__
    inputs = "".join([key, ":inputs"])
    outputs = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Conserve the original function’s name, docstring, etc"""
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result

    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of calls of a particular function

    Parameters:
    - method (Callable): The function to display history from
    """
    key = method.__qualname__
    inputs = f"{key}:inputs"
    outputs = f"{key}:outputs"
    redis = method.__self__._redis
    method_count = redis.get(key).decode('utf-8')

    print(f'{key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for i, o in list(IOTuple):
        attr, data = i.decode("utf-8"), o.decode("utf-8")
        print(f'{key}(*{attr}) -> {data}')


class Cache:
    """
    Cache redis class
    """

    def __init__(self):
        """Creates the redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionTypes) -> str:
        """
        Generates a random key and store the input data in Redis using the
        random key

        Parameters:
        - data (str | bytes | int | float): The input data

        Returns:
        - string: The generated key
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionTypes:
        """
        Converts the data back to the desired format

        Parameters:
        - key (string): The key
        - fn (Callable): Optional arguments that converts the data back to the
        desired format

        Returns:
        - (str | bytes | int | float): The data
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """
        Converts the data from bytes to integer

        Parameters:
        - self (bytes): The data to convert

        Returns:
        - int: The converted data
        """
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """
        Converts the data from bytes to string

        Parameters:
        - self (bytes): The data to convert

        Returns:
        - string: The converted data
        """
        return self.decode("utf-8")
