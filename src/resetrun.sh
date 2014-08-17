#!/bin/sh
python manage.py destroy_db
python manage.py create_db
python manage.py init_data

python manage.py runserver