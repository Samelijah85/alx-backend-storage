#!/usr/bin/env python3
"""
Module 102-log_stats

Adds the top 10 of the most present IPs in the collection nginx
of the database logs
"""
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    logs_database = client.logs
    nginx_collection = logs_database.nginx
    total = nginx_collection.count_documents({})
    get = nginx_collection.count_documents({"method": "GET"})
    post = nginx_collection.count_documents({"method": "POST"})
    put = nginx_collection.count_documents({"method": "PUT"})
    patch = nginx_collection.count_documents({"method": "PATCH"})
    delete = nginx_collection.count_documents({"method": "DELETE"})
    path = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"})
    print(f"{total} logs")
    print("Methods:")
    print(f"\tmethod GET: {get}")
    print(f"\tmethod POST: {post}")
    print(f"\tmethod PUT: {put}")
    print(f"\tmethod PATCH: {patch}")
    print(f"\tmethod DELETE: {delete}")
    print(f"{path} status check")
    print("IPs:")
    sorted_ips = nginx_collection.aggregate(
        [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
         {"$sort": {"count": -1}}])
    i = 0
    for s in sorted_ips:
        if i == 10:
            break
        print(f"\t{s.get('_id')}: {s.get('count')}")
        i += 1
