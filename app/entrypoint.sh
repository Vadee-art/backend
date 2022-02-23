#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput


# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# # Apply database migrations
# echo "Run development server"
# python manage.py runserver 0.0.0.0:8000

exec "$@"