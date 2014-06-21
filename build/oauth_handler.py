from flask import url_for, request, session, redirect
from flask_oauth import OAuth
from flask.ext.security import login_user
from models import users, Connection, User
from ek import app, db

FACEBOOK_APP_ID = app.config['FACEBOOK_APP_ID'] #'1478430419047146'
FACEBOOK_APP_SECRET = app.config['FACEBOOK_APP_SECRET']#'a4e998278e99029f86abaa2eb4ef95df'

oauth = OAuth()

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth',
                            consumer_key=FACEBOOK_APP_ID,
                            consumer_secret=FACEBOOK_APP_SECRET,
                            request_token_params={'scope': ('email, ')}
)

@app.route("/provider_login", methods=["GET", "POST"])
@app.route("/provider_login/<provider_id>", methods=["GET", "POST"])
def provider_login(provider_id=None):
    providers = {
        'facebook': {
            'object': facebook,
            'url': 'facebook_authorized'
        }
    }
    provider = providers[provider_id]['object']
    url = providers[provider_id]['url']
    return provider.authorize(callback=url_for(url, next=request.args.get('next'),
                                               _external=True))

@facebook.tokengetter
def get_facebook_token():
    return session.get('facebook_token')

@app.route("/facebook_authorized")
@facebook.authorized_handler
def facebook_authorized(resp):
    next_url = request.args.get('next') or '/'
    if resp is None or 'access_token' not in resp:
        return redirect(next_url)

    session['facebook_token'] = (resp['access_token'], '')
    data = facebook.get('/me').data
    profile_picture = facebook.get('/me/picture').data

    if 'id' in data and 'name' in data \
        and 'email' in data and 'link' in data:

        provider_user_id = data['id']
        name = data['name']
        username = data['username']
        user_email = data['email']
        profile_url = data['link']
        profile_picture = profile_picture['url']

        user = User.query.filter(User.email == user_email).first()
        if not user:
            user = users.create_user(name=name,
                                     email=user_email,
                                     photo=profile_picture,
                                     password=None,
                                     active=True)
            users.commit()
        connection = Connection.query.filter(Connection.user_id == user.id,
                                             Connection.provider_id == 'facebook').first()
        if not connection:
            print "no prior connection"
            connection = Connection(user=user,
                                    provider_id='facebook',
                                    provider_user_id=provider_user_id,
                                    access_token=resp['access_token'],
                                    profile_url=profile_url,
                                    image_url=profile_picture,
                                    full_name=name,
                                    display_name=username
            )
            db.session.add(connection)
            db.session.commit()
        else:
            print "updating prior connection"
            connection.access_token = resp['access_token']
            db.session.commit()

        if connection and login_user(user):
            users.commit()
            return redirect(next_url)

    return redirect("/login")