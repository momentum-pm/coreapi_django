#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A coreapi_django beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
#celery -A coreapi_django worker --beat --scheduler django --loglevel=info
