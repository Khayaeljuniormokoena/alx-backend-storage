#!/usr/bin/env python3

from pymongo import MongoClient
from collections import Counter

def log_stats():
    client = MongoClient()
    db = client.logs
    nginx_collection = db.nginx
    
    # Number of documents in the collection
    total_logs = nginx_collection.count_documents({})
    
    # Count documents for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: nginx_collection.count_documents({"method": method}) for method in methods}
    
    # Count documents with method=GET and path=/status
    status_checks = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    
    # Get the top 10 most present IPs
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(nginx_collection.aggregate(pipeline))
    
    # Print the statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_checks} status check")
    
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")

if __name__ == "__main__":
    log_stats()
