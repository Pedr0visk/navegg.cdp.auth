#!/bin/sh

echo "Running migration..."
python manage.py migrate --noinput
echo "finished migration"

echo "Running server..."
echo ${USER}
# python manage.py collectstatic --no-input

gunicorn --bind 0.0.0.0:9000 core.wsgi