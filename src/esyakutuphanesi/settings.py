# -*- coding: utf-8 -*-
from os import path

project_settings = {
    'DEBUG': True,
    'SECRET_KEY': 'dsaojfldckl;rfpodsewkfodlscx;lk',
    'NAME': 'Esya Kutuphanesi',
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///db.sql',
    'UPLOADS_FOLDER': path.dirname(path.realpath(__file__)) + '/static/photos',
}

admin_settings = {
    'ADMIN_URL': '/admin'
}

mail_settings = {
    'MAIL_SERVER': 'localhost',
    'MAIL_PORT': 25,
    # 'MAIL_USE_SSL': True,
    # 'MAIL_USERNAME': 'username',
    # 'MAIL_PASSWORD': 'password',
}

security_settings = {
    'SECURITY_REGISTERABLE': True,
    'SECURITY_RECOVERABLE': True,
    'SECURITY_CHANGEABLE': True,
    # 'SECURITY_CONFIRMABLE': True,
    'SECURITY_PASSWORD_HASH': 'sha256_crypt',
    'SECURITY_PASSWORD_SALT': 'tuz',
    'SECURITY_POST_REGISTER_VIEW': '/check_approved/register',
    'SECURITY_POST_REGISTER_VIEW': '/check_approved/register',
    'SECURITY_POST_LOGIN_VIEW': '/check_approved/login',
    'SECURITY_EMAIL_SENDER': (u'Eşya Kütüphanesi', 'bilgi@esyakutuphanesi.com'),

}

all_settings = dict(
    project_settings.items() +
    admin_settings.items() +
    mail_settings.items() +
    security_settings.items()
)


PROFILE_PHOTO_PREFIX = 'profile_'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
