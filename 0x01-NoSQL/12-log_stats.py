#!/usr/bin/env python3
""" a function that provides some stats about Nginx logs stored in MongoDB """
from pymongo import MongoClient

# Connect to the MongoDB server running on localhost at port 27017
client = MongoClient('mongodb://localhost:27017/')  # Adjust the connection string as needed
db = client.logs
collection = db.nginx

# Count the total number of documents in the collection
total_logs = collection.count_documents({})

# Count the number of documents for each HTTP method
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
method_counts = {method: collection.count_documents({"method": method}) for method in methods}

# Count the number of documents with method=GET and path=/status
get_status_count = collection.count_documents({"method": "GET", "path": "/status"})

# Display the results
print(f"{total_logs} logs")
print("Methods:")
for method in methods:
    print(f"\tmethod {method}: {method_counts[method]}")
print(f"{get_status_count} status check")

# Close the connection
client.close()
