#!/usr/bin/env python3
""" A utility function that sorts students by average score """


def top_students(mongo_collection):
    """ scores """
    return mongo_collection.aggregate([
        {"$project": {
            name: "$name",
            averageScore: {"$avg": "$topics.score"}
        }},
        {"$sort": {averageScore: -1}}
    ])
