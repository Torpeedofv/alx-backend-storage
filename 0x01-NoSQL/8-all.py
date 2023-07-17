#!/usr/bin/env python3
"""A function that list all documents in a collection"""

import pymongo


def list_all(mongo_collection):
    if mongo_collection is None:
        return []
    return mongo_collection.find()
