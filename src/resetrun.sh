#!/bin/sh
python manage.py database drop
python manage.py database create -s no
python manage.py database populate

python manage.py runserver -h 0.0.0.0 -p 5000