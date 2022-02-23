#!/bin/sh

docker-compose exec web python manage.py makemigrations --noinput