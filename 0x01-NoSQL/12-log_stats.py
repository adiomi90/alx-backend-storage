#!/usr/bin/env python3
""" a function that provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.27017/')
    collection = client.logs.nginx
    print(f"{col.estimated_document_count()} logs")
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = col.count_documents({'method': method})
        print("\tmethod {}: {}".format(method, count))
    status_get = col.count_documents({'method': 'GET', 'path': "/status"})
    print("{} status check".format(status_get))
    print("IPs:")
    topIps = col.aggregate([
        {"$group": {
            "_id": "$ip",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])
    for ip in topIps:
        print("\t{}: {}".format(ip.get('ip'), ip.get('count')))
