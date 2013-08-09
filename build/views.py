from flask import render_template, flash, redirect
from flask.ext.login import current_user
from sqlalchemy.orm.exc import NoResultFound

from ek import app, db, RESPONSE_CHOICES

from models import User, Category, Thing, Object, Response, Request

@app.route('/')
def home():
    objects = Object.query.order_by(Object.id.desc()).limit(5)
    users = User.query.order_by(User.id.desc()).limit(5)
    responses = Response.query.order_by(Response.id.desc()).limit(5)
    requests = Request.query.order_by(Request.id.desc()).limit(5)
    if current_user.is_anonymous():
        waiting_requests = None
    else:
        waiting_requests = Request.query.join(Object).filter(Object.owner==current_user, Request.responses == None)

    return render_template('index.html',
                           user=current_user,
                           objects=objects,
                           users=users,
                           responses=responses,
                           requests=requests,
                           waiting_requests=waiting_requests,
                           )
    

@app.route('/search/<context>/')
def search(context):
    contexts = {
             'category':Category,
             'thing':Thing,
             'user':User,
             'Object':Object,
             }
    if context in contexts:
        f = contexts[context]
        result = f.query.order_by(f.id.desc()).limit(5)
        return render_template('list.html',
                               user=current_user,
                               result=result,
                               context=context)
    else:
        return render_template('404.html',
                               user=current_user)

@app.route('/categories/<category_name>/')
@app.route('/things/<thing_name>/')
def categories(category_name=None,thing_name=None):
    if category_name:
        category = Category.query.filter(Category.name==category_name).first()
        return render_template('category.html',
                               user=current_user,
                               category=category,
                               thing=None)
    elif thing_name:
        thing = Thing.query.filter(Thing.name==thing_name).first()
        return render_template('category.html',
                               user=current_user,
                               category=None,
                               thing=thing)
    else:
        return render_template('404.html',
                               user=current_user)
    
@app.route('/profiles/<username>/')
def profiles(username=None):
    if username:
        profile = User.query.filter(User.nickname == username).first()
        return render_template('profile.html',
                               user=current_user,
                               profile=profile)
    else:
        return render_template('404.html',
                               user=current_user)



@app.route('/profiles/<username>/objects/<object_id>/')
def show_object(username, object_id):
    try:
        object = Object.query.filter(Object.id==object_id).one()
    except NoResultFound:
        return render_template('404.html',
                               user=current_user)

    return render_template('object.html',
                           object=object,
                           user=current_user,
                           owner_nick=username,
                           )

@app.route('/profiles/<username>/objects/<object_id>/request/')
def add_request(username, object_id):
    object = Object.query.filter(Object.id==object_id).one()
    request = Request(by=current_user, object=object )
    db.session.add(request)
    db.session.commit()
    flash('Requested object', 'info')
    return render_template('object.html',
                           object=object,
                           user=current_user,
                           owner_nick=username,
                           )

@app.route('/my_requests/')
def my_requests():
    requests = Request.query.join(Object).filter(Object.owner==current_user, Request.responses == None)
    return render_template('my_requests.html',
                           requests=requests,
                           user=current_user)

@app.route('/my_requests/<request_id>/<response>')
def respond_to_request(request_id, response):
    request = Request.query.join(Object).filter(Request.id==request_id, Object.owner == current_user).one()
    response_object = Response(request=request, response=filter(lambda x: RESPONSE_CHOICES[x]==response, RESPONSE_CHOICES)[0])
    db.session.add(response_object)
    db.session.commit()

    flash("%s %s's request" %(response, request.by),'info')

    return redirect('/my_requests')
