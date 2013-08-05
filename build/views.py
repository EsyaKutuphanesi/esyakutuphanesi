from flask import render_template
from flask.ext.login import login_required, current_user

from ek import app

@app.route('/')
@login_required
def home():
    return render_template('index.html', user=current_user)
