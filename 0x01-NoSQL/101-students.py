#!/usr/bin/env python3
"""Top students"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    pipeline = [
        {"$unwind": "$scores"},
        {"$group": {
            "_id": "$_id",
            "averageScore": {"$avg": "$scores.score"},
            "name": {"$first": "$name"}  # Assuming student's name is stored in a field named "name"
        }},
        {"$sort": {"averageScore": -1}}  # Sort by average score in descending order
    ]

    result = mongo_collection.aggregate(pipeline)

    return [{"name": doc["name"], "averageScore": doc["averageScore"]}
            for doc in result]
