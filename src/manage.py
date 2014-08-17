from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from settings import *

app = Flask(__name__)

for config_var in all_settings:
    app.config[config_var] = all_settings[config_var]

try:
    app.config.from_pyfile(path.dirname(path.realpath(__file__)) + '/ek.cfg')
except:
    pass

db = SQLAlchemy(app)
mail = Mail(app)

from messages import security_messages, security_config

for key, value in security_messages.iteritems():
    app.config['SECURITY_MSG_' + key] = value

for key, value in security_config.iteritems():
    app.config['SECURITY_' + key] = value

from views import *
from admin import *
from oauth_handler import *

host, port = ('0.0.0.0', 5000)

if __name__ == '__main__':
    app.run(host=host, port=port)
