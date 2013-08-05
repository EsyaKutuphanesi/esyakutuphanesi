from flask import render_template
from flask.ext.login import login_required

from ek import app

@app.route('/')
@login_required
def home():
    print 'ok'
    return render_template('index.html')
