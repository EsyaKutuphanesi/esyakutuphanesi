from flask import render_template, flash, redirect, request, send_from_directory
from flask_login import current_user, login_required
from sqlalchemy.orm.exc import NoResultFound
from forms import *
from ek import app, db, ALLOWED_EXTENSIONS
from models import *

import uuid
import os.path
import json

@app.route('/')
@app.route('/categories')
def home():
    form = SeachForm()
    last_objects = Stuff.query.order_by(Stuff.id.desc()).limit(5)
    return render_template("index.html",user=current_user,last_objects=last_objects,form=form)

@app.route('/search',methods=["GET", "POST"])
def search():
    form = SeachForm()
    last_objects = list()
    if request.method == 'GET':
        last_objects = Stuff.query.join(Address).filter(Address.id==Stuff.address_id,
                                                        Stuff.title.like('%'+unicode(request.args.get('stuff'))+'%'),
                                                        Address.detail.like('%'+unicode(request.args.get('address'))+'%'))

    return render_template("search.html", user=current_user, last_objects=last_objects, form=form)

@login_required
@app.route('/new_address',methods=["GET", "POST"])
def new_address():
    if request.method == 'POST':
        print unicode(request.form)
        new_address = Address(user=current_user,
                              lat=request.form.get('lat'),
                              lng=request.form.get('lng'),
                              detail=unicode(request.form.get('address')),
                              name=request.form.get('address_name'))
        db.session.add(new_address)
        db.session.commit()
    return render_template("map.html", user=current_user)

@login_required
@app.route('/new_stuff',methods=["GET", "POST"])
def new_stuff():
    form = EditStuffForm()
    if current_user.addresses:
        address_choices = [(address.id,address.name)for address in current_user.addresses]
    else:
        address_choices = []
    form.address.choices = address_choices
    categories  = Category.query.order_by(Category.name)
    category_choices = [(category.id,category.name)for category in categories]
    form.category.choices = category_choices
    stuff_types = categories[0].type_list
    stuff_type_choices = [(stuff_type.id, stuff_type.name)for stuff_type in stuff_types]
    form.stuff_type.choices = stuff_type_choices
    if request.method == 'POST':
        category  = Category.query.filter(Category.id == form.category.data).first()
        stuff_types = category.type_list
        stuff_type_choices = [(stuff_type.id, stuff_type.name)for stuff_type in stuff_types]
        form.stuff_type.choices = stuff_type_choices
        if form.validate_on_submit():
            address = Address.query.filter(Address.id == form.address.data, Address.user_id==current_user.id).first()
            category = Category.query.filter(Category.id == form.category.data).first()
            stuff_type = StuffType.query.filter(StuffType.id == form.stuff_type.data).first()
            tags = form.tags.data.split(',')
            new_stuff = Stuff(title=form.title.data,
                                detail=form.detail.data,
                                stuff_address=address,
                                owner=current_user,
                                category=category,
                                stuff_type=stuff_type)
            db.session.add(new_stuff)
            file = form.photo.file
            if file:
                file_ext = get_file_extension(file.filename)
                generated_name = str(uuid.uuid1())+'.'+file_ext
                filepath = os.path.join(app.config['UPLOADS_FOLDER'],generated_name)
                file.save(filepath)
                new_photo = StuffPhoto(owner=current_user,filename= generated_name,stuff=new_stuff)
                db.session.add(new_photo)
                db.session.commit()
            for t in tags:
                new_tag = Tag(stuff=new_stuff,name=t)
                db.session.add(new_tag)
            db.session.commit()
            form.fill_form(new_stuff)
            return redirect('edit_profile')
    return render_template("edit_stuff.html", user=current_user, form=form, action='Add',stuff=None)

@login_required
@app.route('/edit_stuff/<stuff_id>',methods=["GET", "POST"])
def edit_stuff(stuff_id):
    stuff = Stuff.query.filter(Stuff.id == stuff_id).first()
    form = EditStuffForm()
    if current_user.addresses:
        address_choices = [(address.id,address.name)for address in current_user.addresses]
    else:
        address_choices = [('none','None')]
    form.address.choices = address_choices
    categories  = Category.query.order_by(Category.name)
    category_choices = [(category.id,category.name)for category in categories]
    form.category.choices = category_choices
    category  = Category.query.filter(Category.id == stuff.category_id).first()
    stuff_types = category.type_list
    stuff_type_choices = [(stuff_type.id, stuff_type.name)for stuff_type in stuff_types]
    form.stuff_type.choices = stuff_type_choices
    if request.method == 'POST':
        category  = Category.query.filter(Category.id == form.category.data).first()
        stuff_types = category.type_list
        stuff_type_choices = [(stuff_type.id, stuff_type.name)for stuff_type in stuff_types]
        form.stuff_type.choices = stuff_type_choices
        if form.validate_on_submit():
            stuff_query = Stuff.query.filter(Stuff.id == form.stuffid.data)
            file = form.photo.file
            tags = form.tags.data.split(',')
            if file:
                file_ext = get_file_extension(file.filename)
                generated_name = str(uuid.uuid1())+'.'+file_ext
                filepath = os.path.join(app.config['UPLOADS_FOLDER'],generated_name)
                file.save(filepath)
                new_photo = StuffPhoto(owner=current_user,filename= generated_name,stuff=stuff)
                db.session.add(new_photo)
                db.session.commit()
            stuff_query.update({Stuff.title: form.title.data,
                                Stuff.detail: form.detail.data,
                                Stuff.address_id: form.address.data,
                                Stuff.category_id: form.category.data,
                                Stuff.type_id: form.stuff_type.data
                                })
        for t in tags:
            if t > '':
                new_tag = Tag(stuff=stuff,name=t)
                db.session.add(new_tag)
        db.session.commit()
    if stuff:
        form.fill_form(stuff)
    return render_template("edit_stuff.html", user=current_user, form=form, action='Edit', stuff=stuff)

@login_required
@app.route('/my_stuff',methods=["GET", "POST"])
def my_stuff():
    return render_template("my_stuff.html", user=current_user)


@app.route('/get_stuff_types/<category_id>',methods=["GET", "POST"])
@app.route('/get_stuff_types',methods=["GET", "POST"])
def get_stuff_types(category_id=None):
    if category_id:
        category  = Category.query.filter(Category.id == category_id).first()
        stuff_types = category.type_list
    else:
        stuff_types = StuffType.query.order_by(StuffType.name)

    stuff_type_choices = [{"id":stuff_type.id, "name": stuff_type.name}for stuff_type in stuff_types]
    stuff_type_choices_json = json.dumps(stuff_type_choices)
    return stuff_type_choices_json

@app.route('/get_categories',methods=["GET", "POST"])
@app.route('/get_categories/<type_id>',methods=["GET", "POST"])
def get_categories(type_id=None):
    if type_id:
        stuff_type = StuffType.query.filter(StuffType.id == type_id).first()
        categories = stuff_type.category_list
    else:
        categories  = Category.query.order_by(Category.name)

    category_list = [{"id":category.id, "name": category.name}for category in categories]
    category_list_json = json.dumps(category_list)
    return category_list_json

@login_required
@app.route('/show_stuff/<stuff_id>',methods=["GET", "POST"])
def show_stuff(stuff_id):
    stuff = Stuff.query.filter(Stuff.id == stuff_id).first()
    return render_template("show_stuff.html", user=current_user,stuff=stuff)

@login_required
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    print current_user.is_anonymous()
    if current_user.is_anonymous():
        return redirect('/')
    form = EditUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        if current_user.id == int(form.userid.data):
            file = form.photo.file
            if file:
                file_ext = get_file_extension(file.filename)
                generated_name = str(uuid.uuid1())+'.'+file_ext
                filepath = os.path.join(app.config['UPLOADS_FOLDER'], generated_name)
                file.save(filepath)
                new_photo = Photo(owner=current_user, filename=generated_name)
                db.session.add(new_photo)
                db.session.commit()
            User.query.filter(User.id == current_user.id).update({
                                  User.name: form.name.data,
                                  User.email: form.email.data,
                                  User.phone_number: form.phone_number.data,
                                  User.about: form.about.data})
            db.session.commit()

    form.fill_form(current_user)
    return render_template('edit_profile.html',
                           form=form,
                           user=current_user)

@app.route('/photos/<path:filename>')
def photos_static(filename):
    return send_from_directory(app.root_path + '/photos/', filename)

def get_file_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1]

@app.route('/category/<category_name>/',methods=["GET", "POST"])
def category_view(category_name=None):
    if category_name:
        category = Category.query.filter(Category.name == category_name).first()
        stuff_list = category.stuff_list
    else:
        stuff_list = Stuff.query.order_by(Stuff.id.desc()).limit(20)
    params = {
        'category': {
            'type': 'category',
            'value': category.id
        }
    }
    return render_template("browse.html", user=current_user, stuff_list=stuff_list, params=params)

@app.route('/stuff_type/<type_name>/',methods=["GET", "POST"])
def stuff_type_view(type_name=None):
    if type_name:
        stuff_type = StuffType.query.filter(StuffType.name == type_name).first()
        stuff_list = stuff_type.stuff_list
    else:
        stuff_list = Stuff.query.order_by(Stuff.id.desc()).limit(20)
    params = {
        'stuff_type': {
            'type': 'stuff_type',
            'value': stuff_type.id
        },
    }
    return render_template("browse.html", user=current_user, stuff_list=stuff_list, params=params)

@app.route('/category/<category_name>/type/<type_name>',methods=["GET", "POST"])
def category_stuff_type_view(category_name, type_name):
    if category_name and type_name:
        stuff_type = StuffType.query.filter(StuffType.name == type_name).first()
        category = Category.query.filter(Category.name == category_name).first()
        stuff_list = Stuff.query.\
            join(Category).\
            join(StuffType).\
            filter(StuffType.id == stuff_type.id).\
            filter(Category.id == category.id).\
            limit(5)
    else:
        stuff_list = Stuff.query.order_by(Stuff.id.desc()).limit(20)
    params = {
        'category': {
            'type': 'category',
            'value': category.id
        },
        'stuff_type': {
            'type': 'stuff_type',
            'value': stuff_type.id
        },
    }
    return render_template("browse.html", user=current_user, stuff_list=stuff_list, params=params)

@login_required
@app.route('/my_messages',methods=["GET", "POST"])
def my_messages():
    return render_template("my_messages.html", user=current_user)

@login_required
@app.route('/conversations/<conversation_id>', methods=["GET", "POST"])
def show_conversation(conversation_id):
    conversation = Conversation.query.filter(Conversation.id == conversation_id).first()
    if current_user not in conversation.users:
        redirect('/my_messages')
    print request.form
    form = ConversationForm(request.form)
    print form.message.data
    if request.method == 'POST' and form.validate_on_submit():
        print "OK"
        new_message = Message(user=current_user,
                              conversation=conversation,
                              txt=form.message.data)
        db.session.add(new_message)
        db.session.commit()
    return render_template("conversation.html", user=current_user, form=form, action='Edit', conversation=conversation)

@login_required
@app.route('/make_request/<stuff_id>', methods=["GET", "POST"])
def make_request(stuff_id):
    stuff = Stuff.query.filter(Stuff.id == stuff_id).first()
    new_request = Request(stuff_id=stuff_id,
                          user_id=current_user.id,
                          from_user_id=stuff.owner_id)
    db.session.add(new_request)

    new_conversation = Conversation(title='new conversation',
                                    users=[current_user, stuff.owner],
                                    request=new_request)

    db.session.add(new_conversation)

    new_message = Message(user=current_user,
                          conversation=new_conversation,
                          txt='Merhaba %s, %s esyasini istiyorum' % (stuff.owner.name, stuff.title))
    db.session.commit()
    return render_template("my_messages.html", user=current_user)