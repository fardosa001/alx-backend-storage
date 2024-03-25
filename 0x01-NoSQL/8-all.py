#!/usr/bin/env python3
"""lists all documents in a collection"""
import pymongo


def list_all(mongo_collection):
    """lists all document in a collection"""
    if not mongo_collection:
        return []
    return list(mongo_collection.find())