#!/usr/bin/env python3
""" A function that insert documents in a collection based on kwargs """
import pymongo


def insert_school(mongo_collection, **kwargs):
    """ insert a document in a collection """
    if not mongo_collection:
        return None
    return mongo_collection.insert_one(kwargs).inserted_id
