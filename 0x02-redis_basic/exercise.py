#!/usr/bin/env python3
"""Creates a class, a method, stores an instance of redis and
writes strings to redis"""

import redis
import uuid
from typing import Union, Callable
from functools import wraps


def replay(method: Callable) -> None:
    """displays the history of calls of a particular function"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    history = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for input, output in list(history):
        attr, data = input.decode("utf-8"), output.decode("utf-8")
        print(f"{method_key}(*{attr}) -> {data}")


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and ooutputs for a particular function"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result

    return wrapper


def count_calls(method: Callable) -> Callable:
    """count how many times methods of the Cache class are called."""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """Creation of a cache class that stores an instance of the redis client"""
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) ->\
            Union[str, bytes, int, float]:
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
