#!/usr/bin/env python3
"""
Module 8-all

List all documents in Python
"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection

    Parameters:
    - mongo_collection (pymongo): The collection object

    Returns:
    - list: All documents in the collection, otherwise an empty list
    """
    return mongo_collection.find()
