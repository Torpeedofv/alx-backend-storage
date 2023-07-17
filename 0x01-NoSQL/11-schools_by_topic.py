#!/usr/bin/env python3
"""A modulr for a function"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """A function that returns the list of school having a specific topic"""
    return mongo_collection.find({"topic": topic})
