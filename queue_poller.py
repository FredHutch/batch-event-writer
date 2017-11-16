#!/usr/bin/env python3


"""
This is a temporary solution until I can deploy a lambda function that can see
internal Hutch machines, such as mydb, and write to them.

Until then, this will poll an SQS queue and write to a mongodb database
in mydb when there is a message.
"""

import os
import sys
import time
import json

import pymongo
import boto3

for var in ['MONGO_URL', 'QUEUE_URL']:
    bail = False
    if not os.getenv(var):
        bail = True
        print("Environment variable {} is not defined! Exiting.".format(var))
    if bail:
        sys.exit(1)

QUEUE_URL = os.getenv('QUEUE_URL')
MONGO_URL = os.getenv('MONGO_URL')
MONGO_CLIENT = pymongo.MongoClient(MONGO_URL)
MONGO_DB = MONGO_CLIENT.batch_events
MONGO_COLLECTION = MONGO_DB['events']
SQS = boto3.client("sqs")

print("About to start polling, will run forever....")


def delete_msg(msg):
    "Delete a message from the queue"
    print("Deleting message.")
    SQS.delete_message(QueueUrl=QUEUE_URL,
                       ReceiptHandle=msg['ReceiptHandle'])


while True:
    RESPONSE = SQS.receive_message(QueueUrl=QUEUE_URL)
    if 'Messages' in RESPONSE:
        for message in RESPONSE['Messages']:
            print("Got message")
            print(message['Body'])
            try:
                message_obj = json.loads(message['Body'])
            except json.JSONDecodeError:
                print("Message is not valid JSON, ignoring.")
                delete_msg(message)
                continue
            print("Before insert")
            try:
                MONGO_COLLECTION.insert_one(message_obj)
            except TypeError:
                print("Message must be a dict!")
                delete_msg(message)
                continue
            print("After insert, deleting message.")
            delete_msg(message)
    time.sleep(1)
