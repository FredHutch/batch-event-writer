#!/usr/bin/env python3

"Lambda function to write a Batch state transition event to MongoDb"

import os
import json
import datetime

from pymongo import MongoClient

STATES = ['SUBMITTED', 'PENDING', 'RUNNABLE', 'STARTING',
          'RUNNING', 'FAILED', 'SUCCEEDED']
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
    coll = db0['events']
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
        message = obj['Message']
    detail = message['detail']
    detail['timestamp'] = datetime.datetime.now()
    detail['statusNum'] = STATE_DICT[detail['status']]
    # copy JOB_GROUP_* environment vars (if any) to top level
    if 'container' in detail and 'environment' in detail['container']:
        env = detail['container']['environment']
        job_group_vars = [{x['name']: x['value']}  \
            for x in env if x['name'].startswith('JOB_GROUP_')]
        for item in job_group_vars:
            key = list(item.keys())[0]
            detail[key] = item[key]

    result = coll.insert_one(detail)
    print("Result of insert_one: {}".format(result))
    print("Acknowledged? {}".format(result.acknowledged))
    print("ID of inserted object: {}".format(str(result.inserted_id)))
    print("Done")
