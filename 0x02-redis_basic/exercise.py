#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function """
    key_inputs = method.__qualname__ + ":inputs"
    key_outputs = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped method"""
        self._redis.rpush(key_inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(key_outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ to count how many times methods of the Cache class are called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """wrapped method"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """cache class"""
    def __init__(self):
        """store an instance of the Redis client as a
        private variable named _redis (using redis.Redis())
        and flush the instance using flushdb."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generates a random key (e.g. using uuid),
        store the input data in Redis using the random
        key and return the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Callable = None) -> Union[str, bytes, int, float]:
        """a method used to convert the data back to the desired format."""
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """automatically parametrize Cache.get
        with the correct conversion function."""
        data = self._redis.get(key)
        return data.decode("utf-8")

    def get_int(self, key: str) -> int:
        """automatically parametrize Cache.get
        with the correct conversion function."""
        data = self._redis.get(key)
        try:
            data = int(value.decode("utf-8"))
        except Exception:
            data = 0
        return data
