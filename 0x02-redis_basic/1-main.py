#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache

cache = Cache()

TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    result = cache.get(key, fn=fn)
    try:
        assert result == value
        print(f"Test case passed: {value} -> {result}")
    except AssertionError as e:
        print(f"Test case failed: {value} -> {result}")
        print(e)
