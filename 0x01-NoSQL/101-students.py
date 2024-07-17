#!/usr/bin/env python3
"""
Module 101-students

Demonstrates a Python function that returns all students sorted by average
score
"""


def top_students(mongo_collection):
    """
    Sorts all students by average

    Parameters:
    - mongo_collection (pymongo): The collection object

    Returns:
    - list: all students sorted by age
    """
    return mongo_collection.aggregate([
        {"$project": {
            "name": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
