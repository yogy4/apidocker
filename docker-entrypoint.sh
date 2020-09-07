#!/bin/sh
set -e
flask db upgrade
# gunicorn -c gunicorn.config.py wsgi:app
gunicorn --bind 0.0.0.0:5000 wsgi:app_serv