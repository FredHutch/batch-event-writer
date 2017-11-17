#!/bin/bash

set -e

# workon batch-event-writer

echo adding site-packages...
pkgdir=$VIRTUAL_ENV/lib/python3.6/site-packages

zip_home=$(pwd)

cd $pkgdir

zip -qr9 $zip_home/batch-event-writer.zip *

cd $zip_home

echo adding lambda function...
zip -g batch-event-writer.zip lambda_function.py

echo updating function code...
aws lambda update-function-code --function-name batch_event_writer \
  --zip-file fileb://batch-event-writer.zip
