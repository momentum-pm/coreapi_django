#!/bin/bash

source .env
source .venv/bin/activate

rm -r **/migrations/0**.py
source .venv/bin/activate
python manage.py makemigrations
for f in *; do
    cp $f/fixtures/**.py $f/migrations/ 2> /dev/null
done
/bin/bash scripts/local-remigrate.sh