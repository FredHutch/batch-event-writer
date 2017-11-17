#!/usr/bin/env python3

"Lambda function to write a Batch state transition event to MongoDb"

import os
import json

from pymongo import MongoClient


def handler(event, context):
    "Lambda event handler"
    print("event is {}".format(event))
    print("event type is {}".format(event.__class__.__name__))
    print("context is {}".format(context))
    client = MongoClient(os.getenv("MONGO_URL"))
    db0 = client.testdb
    coll = db0['mycoll']
    print("event keys are: {}".format(event.keys()))
    print("type of event['body']: {}".format(event['body'].__class__.__name__))
    print("event body:\n{}".format(event['body']))
    if isinstance(event['body'], str):
        obj = json.loads(event['body'])
    else:
        obj = event['body']
    if isinstance(obj['Message'], str):
        message = json.loads(obj['Message'])
    else:
        message = obj['message']
    coll.insert_one(message)
    print("Done")
