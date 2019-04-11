#!/usr/bin/env python3

"Lambda function to write a Batch state transition event to MongoDb"

# IMPORTANT - run this function in the HSE account (it used to run in Fred Hutch
# but no more).

import os
import datetime

from pymongo import MongoClient

STATES = [
    "SUBMITTED",
    "PENDING",
    "RUNNABLE",
    "STARTING",
    "RUNNING",
    "FAILED",
    "SUCCEEDED",
]
STATE_DICT = {}

for idx, state in enumerate(STATES):
    STATE_DICT[state] = idx


def handler(event, context):
    "Lambda event handler"
    print("event is {}".format(event))
    print("event type is {}".format(event.__class__.__name__))
    print("context is {}".format(context))
    client = MongoClient(os.getenv("MONGO_URL"))
    db0 = client.batch_events
    coll = db0["events"]
    # count = coll.count()
    # print("Done")
    print("event keys are: {}".format(event.keys()))
    detail = event["detail"]
    # TODO change detail['createdAt'] from a number (secs/epoch) to datetime obj
    detail["timestamp"] = datetime.datetime.now()
    detail["statusNum"] = STATE_DICT[detail["status"]]
    # copy JOB_GROUP_* environment vars (if any) to top level
    if "container" in detail and "environment" in detail["container"]:
        env = detail["container"]["environment"]
        job_group_vars = [
            {x["name"]: x["value"]} for x in env if x["name"].startswith("JOB_GROUP_")
        ]
        for item in job_group_vars:
            key = list(item.keys())[0]
            detail[key] = item[key]

    result = coll.insert_one(detail)
    print("Result of insert_one: {}".format(result))
    print("Acknowledged? {}".format(result.acknowledged))
    print("ID of inserted object: {}".format(str(result.inserted_id)))
    print("Done")
    return dict(statusCode=200, insertedID=str(result.inserted_id))
