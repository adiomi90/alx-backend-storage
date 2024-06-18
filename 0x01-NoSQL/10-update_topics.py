#!/usr/bin/env python3
""" a function that changes all topics of a school document based on the name """
import pymongo


def update_topics(mongo_collection, name, topics):
    """ update a document in a collection """
    return mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
