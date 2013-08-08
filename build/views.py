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
    
@app.route('/search/<type>')
def search(type):
    if current_user.is_anonymous():
        user = None
    else:
        user = current_user
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
                               user=user,
                               list=list,
                               type=type)
    else:
        return render_template('404.html',
                               user=user)  

@app.route('/categories/<category_name>')
@app.route('/things/<thing_name>')
def categories(category_name=None,thing_name=None):
    if current_user.is_anonymous():
        user = None
    else:
        user = current_user
        
    if category_name:
        category = Category.query.filter(Category.name==category_name).first()
        return render_template('category.html',
                               user=user,
                               category=category,
                               thing=None)
    elif thing_name:
        thing = Thing.query.filter(Thing.name==thing_name).first()
        return render_template('category.html',
                               user=user,
                               category=None,
                               thing=thing)
    else:
        return render_template('404.html',
                               user=user)
    
@app.route('/profiles/<user_name>')
def profiles(user_name=None):
    if current_user.is_anonymous():
        user = None
    else:
        user = current_user
    if user_name:
        profile = User.query.filter(User.name == user_name).first()
        return render_template('profile.html',
                               user=user,
                               profile=profile)
    else:
        return render_template('404.html',
                               user=user)
        
            

