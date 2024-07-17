#!/usr/bin/env python3
"""
Module 9-insert_school

Insert a document in Python
"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs

    Parameters:
    - mongo_collection (pymongo): The collection object
    - kwargs (dict): Key value pair arguments

    Returns:
    - (string): New _id
    """
    new_document = mongo_collection.insert_one(kwargs)
    return new_document.inserted_id
