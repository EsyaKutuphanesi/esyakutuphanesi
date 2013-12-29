from flask import render_template, flash, redirect, request
from flask.ext.login import current_user, login_user
from sqlalchemy.orm.exc import NoResultFound

from ek import app, db


from models import users, User, Role
from flask_login import current_user

@app.route('/')
def home():
    return render_template("index.html",user=current_user)
"""
@app.route('/logme',methods=["GET", "POST"])
def logme():
    form = LoginForm()
    if form.validate_on_submit():
        # login and validate the user...
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("/"))
    return render_template("login.html", form=form)
"""