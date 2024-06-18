#!/usr/bin/env python3

from pymongo import MongoClient

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
    
    # Print the statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_checks} status check")

if __name__ == "__main__":
    log_stats()
