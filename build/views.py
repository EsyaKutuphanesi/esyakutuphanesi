from flask import render_template
from flask.ext.login import current_user

from ek import app

from models import User, Role, Category, Thing, Object

@app.route('/')
def home():
    objects = Object.query.all()

    if current_user.is_anonymous():
        return render_template('index.html', user=None, objects=objects)
    else:
        return render_template('index.html', user=current_user, objects= objects)


