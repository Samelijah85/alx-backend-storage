#!/usr/bin/env python3
"""
Module 11-schools_by_topic

Demonstrates a function that returns a list of school having a specific topic
"""


def schools_by_topic(mongo_collection, topic):
    """
    Searches for schools having a specific topic

    Parameters:
    - mongo_collection (pymongo): The collection object
    - topic (string): The topic to be searched

    Returns:
    - list: Schools having the specified topic
    """
    return mongo_collection.find({"topics": topic})
