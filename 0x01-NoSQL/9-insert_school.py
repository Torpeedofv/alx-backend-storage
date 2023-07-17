#!/usr/bin/env python3
"""A module for a function"""

import pymongo


def insert_school(mongo_collection, **kwargs):
    """A function that inserts a new document in a collection
    based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id
