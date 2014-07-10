# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_mail import Mail
import os.path

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
PROFILE_PHOTO_PREFIX = 'profile_'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sql'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'dsaojfldckl;rfpodsewkfodlscx;lk'
app.config['NAME'] = 'Esya Kutuphanesi'
app.config['ADMIN_URL'] = '/admin'
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
# app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'tuz'
app.config['SECURITY_POST_REGISTER_VIEW'] = '/check_approved/register'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/check_approved/login'
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['SECURITY_EMAIL_SENDER'] = (u'Eşya Kütüphanesi', 'bilgi@esyakutuphanesi.com')

app.config['UPLOADS_FOLDER'] = os.path.dirname(os.path.realpath(__file__)) + '/static/photos'
#app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_USERNAME'] = 'username'
#app.config['MAIL_PASSWORD'] = 'password'

app.config.from_pyfile(os.path.dirname(os.path.realpath(__file__)) + '/ek.cfg')
db = SQLAlchemy(app)
mail = Mail(app)

from messages import security_messages, security_config

for key, value in security_messages.iteritems():
    app.config['SECURITY_MSG_'+key] = value

for key, value in security_config.iteritems():
    app.config['SECURITY_'+key] = value

from views import *
from admin import *
from oauth_handler import *

if __name__ == '__main__':
    app.run(host='0.0.0.0')
