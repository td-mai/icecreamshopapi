# Icecreamshopapi

This repository is a backend api service made by django, django_api_framework, used for the project icecreamshopweb

## Production

docker-compose up -d

## Development

*Prerequisites*

python3

apt-get install libmysqlclient-dev

### Database:

Mariadb (MySQL)

Use docker to run a sql server:

docker-compose up -d db
 
### App

*Create virtualenv*

pip install virtualenv

virtualenv venv

. venv/bin/activate

*Dependencies*

pip install -r requirements.txt

*Apply database migrations*

python manage.py migrate

*Create superuser* 

python manage.py createsuperuser

*Data seeding*

python manage.py loaddata fixtures/*.json

*Run server in dev mode*

In settings.py, set DEBUG=True

python manage.py runserver

### Test

python manage.py test

