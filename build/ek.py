from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sql'
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'dsaojfldckl;rfpodsewkfodlscx;lk'
app.config['NAME'] = 'Esya Kutuphanesi'
app.config['ADMIN_URL'] = '/admin'
db = SQLAlchemy(app)


if __name__ == '__main__':
    from models import *
    from views import *
    from admin import *
    app.run(host='0.0.0.0')
