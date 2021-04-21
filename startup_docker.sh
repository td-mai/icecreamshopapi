#!/bin/bash

while ! nc -z $DATABASE_HOST  $DATABASE_PORT; do sleep 3; done
echo "Database is ready."
# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

echo "Apply create superuser"
python manage.py createsuperuser --noinput
# Data seeding
echo "Data seeding"
python manage.py loaddata fixtures/*.json

echo "Run server"
uwsgi --http :8000 --ini uwsgi.ini

