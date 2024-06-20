#!/usr/bin/env python3
""" A class definition for redis cache """
import redis
import uuid
from functools import wraps
from typing import Union, Callable, Optional


from typing import Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator function that keeps track of
    the inputs and outputs of a method using Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Replays the method execution by retrieving the
    stored inputs and outputs from Redis cache.

    Args:
        method (Callable): The method to replay.

    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
    calls = cache.get(name).decode("utf-8")
    print("{} was called {} times:".format(name, calls))
    inputs = cache.lrange(name + ":inputs", 0, -1)
    outputs = cache.lrange(name + ":outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(name, i.decode('utf-8'),
                                     o.decode('utf-8')))


class Cache:
    """
    A class that represents a cache using Redis.

    Methods:
    - store(data: Union[str, bytes, int, float]) -> str:
    Stores the given data in the cache and returns the generated key.
    - get(key: str, fn: Optional[Callable] = None) -> Union[str, bytes,
    int, float, None]: Retrieves the data associated
    with the given key from the cache.
    - get_str(key: str) -> str: Retrieves the string data
    associated with the given key from the cache.
    - get_int(key: str) -> int: Retrieves the integer
    data associated with the given key from the cache.
    """

    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the given data in the cache and returns the generated key.

        Args:
        - data: The data to be stored in the cache.
        It can be a string, bytes, integer, or float.

        Returns:
        - The generated key associated with the stored data.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, bytes, int, float, None]:
        """
        Retrieves the data associated with the given key from the cache.

        Args:
        - key: The key associated with the data to be retrieved from the cache.
        - fn: An optional callable function to transform the retrieved data.

        Returns:
        - The retrieved data from the cache.
        If the key is not found, returns None.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieves the string data associated with the given key from the cache.

        Args:
        - key: The key associated with the string data
        to be retrieved from the cache.

        Returns:
        - The retrieved string data from the cache.
        If the key is not found, returns None.
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        Retrieves the integer data associated with
        the given key from the cache.

        Args:
        - key: The key associated with the integer
        data to be retrieved from the cache.

        Returns:
        - The retrieved integer data from the cache.
        If the key is not found, returns None.
        """
        return self.get(key, int)
