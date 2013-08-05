from flask import render_template
from flask.ext.login import current_user

from ek import app

@app.route('/')
def home():
    if current_user.is_anonymous():
        return render_template('index.html', user=None)
    else:
        return render_template('index.html', user=current_user)


