#!/bin/sh

set -e

python manage.py wait_for_db
# --noinput for dont asking Are you sure ... :)
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :${APP_PORT} --workers 4 --master --enable-threads --module teacheat.wsgi

