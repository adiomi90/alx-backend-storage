#!/usr/bin/env python3
""" a function that returns the list of school having a specific topic """
import pymongo


def schools_by_topic(mongo_collection, topic):
    """ list all documents in a collection """
    if not mongo_collection:
        return []
    return list(mongo_collection.find({"topics": topic}))
