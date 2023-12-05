#!/bin/bash

set -o errexit
set -o nounset

celery -A coreapi_django worker -l INFO --concurrency=10 -n worker1@%h
#celery -A coreapi_django worker -l INFO --concurrency=10 -n worker1@%h && celery -A coreapi_django worker -l INFO --concurrency=10 -n worker2@%h

#-P solo
#celery multi start 4 -A coreapi_django -l INFO