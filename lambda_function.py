#!/usr/bin/env python3

"Lambda function to write a Batch state transition event to MongoDb"

from pymongo import MongoClient
import os

def handler(event, context):
    "Lambda event handler"
    print("event is {}".format(event))
    print("context is {}".format(context))
    client = MongoClient(os.getenv("MONGO_URL"))
    db0 = client.testdb
    coll = db0['mycoll']
    coll.insert_one({"lambda_says": "hello"})
    print("Done")
