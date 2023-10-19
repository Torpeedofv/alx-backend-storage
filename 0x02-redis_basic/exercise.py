#!/usr/bin/env python3
"""Creates a class, a method, stores an instance of redis and
writes strings to redis"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(fn: callable) -> Callable:
    key = fn.__qualname__


    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return fn(self, *args, **kwargs)


    return wrapper

class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        else:
            return data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: int) -> Union[int, None]:
        return self.get(key, fn=int)
