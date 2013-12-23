from flask import render_template, flash, redirect, request
from flask.ext.login import current_user, login_user
from sqlalchemy.orm.exc import NoResultFound

from ek import app, db


from models import users, User, Role
from flask_login import current_user

@app.route('/')
def home():
    return render_template("index.html")