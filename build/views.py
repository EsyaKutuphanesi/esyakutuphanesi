from flask import render_template
from flask.ext.login import current_user

from ek import app

from models import User, Role, Category, Thing, Object, Response, Request

@app.route('/')
def home():
    objects = Object.query.all()
    users = User.query.all()
    responses = Response.query.all()
    requests = Request.query.all()

    if current_user.is_anonymous():
        user = None
    else:
        user = current_user

    return render_template('index.html',
                           user=user,
                           objects=objects,
                           users=users,
                           responses=responses,
                           requests=requests,
                           )


