from flask import render_template, flash
from flask.ext.login import current_user
from sqlalchemy.orm.exc import NoResultFound

from ek import app,db

from models import User, Category, Thing, Object, Response, Request

@app.route('/')
def home():
    objects = Object.query.all()
    users = User.query.all()
    responses = Response.query.all()
    requests = Request.query.all()

    return render_template('index.html',
                           user=current_user,
                           objects=objects,
                           users=users,
                           responses=responses,
                           requests=requests,
                           )
    
@app.route('/search/<type>/')
def search(type):
    #type='category'
    types = {
             'category':Category.query.order_by(Category.id.desc()).limit,
             'thing':Thing.query.order_by(Thing.id.desc()).limit,
             'user':User.query.order_by(User.id.desc()).limit,
             'Object':Object.query.order_by(Object.id.desc()).limit,
             }
    if type in types:
        f = types[type]
        list = f(5)
        return render_template('list.html',
                               user=current_user,
                               list=list,
                               type=type)
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
