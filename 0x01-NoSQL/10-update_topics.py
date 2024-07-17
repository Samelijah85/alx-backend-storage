#!/usr/bin/env python3
"""
Module 10-update_topics

Change school topics
"""


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics of a school document based on the name

    Parameters:
    - mongo_collection (pymongo): The collection object
    - name (string): The school name to update
    - topics (list of strings): The list of topics approached in the school
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
