#!/usr/bin/env python3
"""inserts a new document in a collection based on kwargs"""



def insert_school(mongo_collection, **kwargs):
    """insert new document in a collection"""
    if mongo_collection is None:
        return[]
    return mongo_collection.insert_one(kwargs).inserted_id