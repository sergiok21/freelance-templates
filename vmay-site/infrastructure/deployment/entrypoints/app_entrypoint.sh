#!/bin/sh

set -e

cd /app/photo

echo "Migrate DB"
python manage.py migrate --settings=photo.settings.$DJANGO_MODE

echo "Collect static"
python manage.py collectstatic --noinput --settings=photo.settings.$DJANGO_MODE

echo "Start Gunicorn"
exec gunicorn photo.gateway_interfaces.wsgi:application --bind 0.0.0.0:9000
