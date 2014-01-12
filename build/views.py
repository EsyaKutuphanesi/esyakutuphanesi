from flask import render_template, flash, redirect, request, send_from_directory
from flask_login import current_user, login_required
from sqlalchemy.orm.exc import NoResultFound
from forms import *
from ek import app, db, ALLOWED_EXTENSIONS
from models import users, User, Role, Address, Stuff, Photo, StuffPhoto, Tag
import uuid
import os.path

@app.route('/')
def home():
    form = SeachForm()
    last_objects = Stuff.query.order_by(Stuff.id.desc()).limit(5)
    return render_template("index.html",user=current_user,last_objects=last_objects,form=form)

@app.route('/search',methods=["GET", "POST"])
def search():
    form = SeachForm()
    last_objects = list()
    print request
    if request.method == 'POST':
        last_objects = Stuff.query.join(Address).filter(Address.id== Stuff.address_id,
                                                        Stuff.title.like('%'+form.stuff.data+'%'),
                                                        Address.detail.like('%'+form.address.data+'%'))
    return render_template("search.html",user=current_user,last_objects=last_objects,form=form)

@app.route('/qsearch',methods=["GET", "POST"])
def qsearch():
    form = SeachForm()
    last_objects = list()
    print request
    if request.method == 'POST':
        last_objects = Stuff.query.join(Address).filter(Address.id== Stuff.address_id,
                                                        Stuff.title.like('%'+form.stuff.data+'%'),
                                                        Address.detail.like('%'+form.address.data+'%'))
    return render_template("search.html",user=current_user,last_objects=last_objects,form=form)

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
    if request.method == 'POST' and form.validate_on_submit():
        address = Address.query.filter(Address.id == form.address.data, Address.user_id==current_user.id).first()
        tags = form.tags.data.split(',')
        new_stuff = Stuff(title=form.title.data,
                            detail=form.detail.data,
                            stuff_address=address,
                            owner=current_user)
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
    if request.method == 'POST' and form.validate_on_submit():
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
                            Stuff.address_id: form.address.data
                            })
        for t in tags:
            if t > '':
                new_tag = Tag(stuff=stuff,name=t)
                db.session.add(new_tag)
        db.session.commit()
    if stuff:
        form.fill_form(stuff)
    return render_template("edit_stuff.html", user=current_user, form=form, action='Edit',stuff=stuff)

@login_required
@app.route('/my_stuff',methods=["GET", "POST"])
def my_stuff():
    return render_template("my_stuff.html", user=current_user)


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
                filepath = os.path.join(app.config['UPLOADS_FOLDER'],generated_name)
                file.save(filepath)
                new_photo = Photo(owner=current_user,filename= generated_name)
                db.session.add(new_photo)
                db.session.commit()
            User.query.filter(User.id == current_user.id).update({
                                  User.name: form.name.data,
                                  User.email: form.email.data,
                                  User.nickname: form.nickname.data,
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