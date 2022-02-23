#!/bin/sh

export $(cat .env)
docker-compose exec db psql -U $SQL_USER -d $SQL_DATABASE