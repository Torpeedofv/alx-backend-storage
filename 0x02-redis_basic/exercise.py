#!/usr/bin/env python3
"""Creates a class, a method, stores an instance of redis and
writes strings to redis"""

import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float]:
        data = self.__redis.get(key)
        if data is not None and fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=str)

    def get_int(self, key: int) -> Union[int, None]:
        return self.get(key, fn=int)
