""" A script that provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient

# Connect to the MongoDB server running on localhost at port 27017
client = MongoClient('mongodb://127.0.0.1:27017')
db = client.logs.nginx
print(f"{col.estimated_document_count()} logs")
print("Methods:")
for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
    count = col.count_documents({"method": method})
    print(f"\tmethod {method}: {count}")
status_count = col.count_documents({"method": "GET", "path": "/status"})
print(f"{status_count} status check")
print("IPs:")
topIps = col.aggregate([
    {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 10},
    {"$project": {"ip": "$_id", "count": 1, "_id": 0}}
])
for ip in topIps:
    print(f"\tip: {ip['ip']}: {ip['count']}")
