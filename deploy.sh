#!/bin/bash
git pull origin main
source .venv/bin/activate
python manage.py migrate
deactivate
mkdir /run/uwsgi/
mkdir /run/uwsgi/coreapi/
rm -f /run/uwsgi/coreapi/coreapi_django.sock
mkdir /var/log/uwsgi/
touch /var/log/uwsgi/coreapi_django.log
sudo uwsgi --ini uwsgi_config.ini
sudo systemctl restart nginx