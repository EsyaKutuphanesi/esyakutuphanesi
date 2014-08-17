# -*- coding: utf-8 -*-
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError
from flask_mail import Mail

from settings import *

app = Flask(__name__)

for config_var in all_settings:
    app.config[config_var] = all_settings[config_var]

try:
    app.config.from_pyfile(path.dirname(path.realpath(__file__)) + '/ek.cfg')
except:
    pass

db = SQLAlchemy(app)
mail = Mail(app)

from messages import security_messages, security_config

for key, value in security_messages.iteritems():
    app.config['SECURITY_MSG_' + key] = value

for key, value in security_config.iteritems():
    app.config['SECURITY_' + key] = value

from views import *
from admin import *
from oauth_handler import *


default_host, default_port = ('0.0.0.0', 5000)

help_message = """
Available Subcommands
---------------------
runserver:
    Runs test server.
    Usage: python manage.py runserver [optional port number, or ipaddr:port]
    Default host 0.0.0.0 and default port is 5000.

destroy_db:
    Destroys all database.
    Usage: python manage.py destroy_db

create_db:
    Creates a new database with empty tables.
    Usage: python manage.py create_db

init_data:
    Loads sample datas to already created database.
    Usage: python manage.py init_data
"""

unvalid_usage_message = "That's not a valid usage."


def runserver(arguments):
    if len(arguments) == 3:
        if ":" in arguments[2]:
            values = arguments[2].split(":")
            app.run(values[0], int(values[1]))
        else:
            app.run(host=default_host, port=int(arguments[2]))

    elif len(arguments) == 2:
        app.run(host=default_host, port=default_port)

    else:
        print(unvalid_usage_message)


def create_db():
    try:
        db.create_all()
        print("Database with empty tables created.")
    except Exception, e:
        print str(e)


def init_data():
    roles = {
        'admin': 'admin',
        'member': 'member',
        'moderator': 'moderator'
    }

    users_list = [{
        'email': 'bilgi@esyakutuphanesi.com',
        'password': "$5$rounds=80000$Yj2S6AtoBQ7mOmuZ$gevIsEG8fTUw92bAfRJw9YQxdyq.0VRkKB3xvoi3cb/",  # ekekek
        'name': 'admin',
        'roles': [roles['admin']],
        'approved': 1
    }, ]

    categories = [u'Bebek ve çocuk', u'Doğada ve sporda', u'Elektronik', u'Giysi dolabı', u'Hırdavat', u'Keyiflik',
                  u'Kütüphane', u'Mobilya', u'Mutfak']

    stuff_types = {
        u'Doğada ve Sporda': [u' Hayvan dostu', u'Spor malzemeleri', u'Ulaşım', u'Yolda'],
        u'Elektronik': [u'Ev elektroniği', u'Bilgisayar', u'Beyaz eşya', u'Telefon'],
        u'Giysi dolabı': [u'Ayakkabı', u'Giysi', u'Gelinlik', u'Özel günlerde'],
        u'Keyiflik': [u'Film', u'Müzik', u'Oyun', u'Konsol oyunları'],
        u'Kütüphane': [u'Roman', u'Dergi', u'Teknik kitap']
    }

    try:
        for role_name in roles.values():
            role = Role(name=role_name)
            db.session.add(role)

        db.session.commit()

        for user in users_list:
            new_user = users.create_user(
                email=user.get('email'),
                password=user.get('password'),
                name=user.get('name'),
                approved=user.get('approved')
            )

            for role in user.get('roles'):
                role_db = Role.query.filter_by(name=role).first()

                new_user.roles.append(role_db)

            db.session.add(new_user)

        db.session.commit()

        for category in categories:
            new_category = Category(name=category)
            db.session.add(new_category)
            if category in stuff_types:
                for stuff_type in stuff_types[category]:
                    new_type = StuffType(name=stuff_type)
                    db.session.add(new_type)
                    new_category.type_list.append(new_type)
            else:
                new_type = StuffType(name=category)
                db.session.add(new_type)
                new_category.type_list.append(new_type)

        db.session.commit()

        print("Sample data loaded.")

    except OperationalError, e:
        print str(e)
        print("Did you create the database?")

    except Exception, e:
        print str(e)


def destroy_db():
    try:
        db.drop_all()
        print("All database destroyed.")
    except Exception, e:
        print str(e)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == "runserver":
            runserver(sys.argv)
        elif sys.argv[1] == "create_db":
            create_db()
        elif sys.argv[1] == "destroy_db":
            destroy_db()
        elif sys.argv[1] == "init_data":
            init_data()
        else:
            print(unvalid_usage_message)
            print(help_message)
    else:
        print(unvalid_usage_message)
        print(help_message)
