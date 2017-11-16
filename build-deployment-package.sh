#!/bin/bash

set -e

# workon batch-event-writer

pkgdir=$VIRTUAL_ENV/lib/python3.6/site-packages

zip_home=$(pwd)

cd $pkgdir

zip -r9 $zip_home/batch-event-writer.zip *

cd $zip_home

zip -g batch-event-writer.zip lambda_function.py
