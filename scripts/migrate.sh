#!/bin/sh

docker-compose exec web python manage.py migrate --noinput