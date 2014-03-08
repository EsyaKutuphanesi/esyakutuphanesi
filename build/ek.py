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
app.config['SECURITY_PASSWORD_HASH'] = 'sha256_crypt'
app.config['SECURITY_PASSWORD_SALT'] = 'tuz'
app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['UPLOADS_FOLDER'] = os.path.dirname(os.path.realpath(__file__)) + '/photos'
#app.config['MAIL_USE_SSL'] = True
#app.config['MAIL_USERNAME'] = 'username'
#app.config['MAIL_PASSWORD'] = 'password'

db = SQLAlchemy(app)


if __name__ == '__main__':
    from models import *
    from views import *
    from admin import *
    from forms import *
    security = Security(app, users, register_form=ExtendedRegisterForm)
    mail = Mail(app)
    app.run(host='0.0.0.0')
