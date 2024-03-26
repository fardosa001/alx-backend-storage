#!/usr/bin/env python3
"""Top students"""


def top_students(mongo_collection):
    """returns all students sorted by average score"""
    pipeline = [
        {
        "$project":
        {
            "name": "$name",
            "averageScore": {"$avg": "$Scores.score"}
        }
    },
    { "$sort": {"averageScore": -1}}
]

    result = mongo_collection.aggregate(pipeline)

    return [{"name": doc["name"], "averageScore": doc["averageScore"]}
            for doc in result]
