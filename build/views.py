from flask import render_template, flash, redirect, request, send_from_directory
from flask_login import current_user, login_required
from sqlalchemy.orm.exc import NoResultFound
from forms import *
from ek import app, db, ALLOWED_EXTENSIONS
from models import users, User, Role, Address, Stuff, Photo
import uuid
import os.path
@app.route('/')
def home():
    last_objects = Stuff.query.order_by(Stuff.id.desc()).limit(5)
    return render_template("index.html",user=current_user,last_objects=last_objects)

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
        address_choices = [('none','None')]
    form.address.choices = address_choices
    if request.method == 'POST' and form.validate_on_submit():
        address = Address.query.filter(Address.id == form.address.data, Address.user_id==current_user.id).first()
        new_stuff = Stuff(title=form.title.data,
                            detail=form.detail.data,
                            stuff_address=address,
                            owner=current_user)
        print new_stuff
        db.session.add(new_stuff)
        db.session.commit()
        form.fill_form(new_stuff)
        return redirect('edit_profile')
    return render_template("edit_stuff.html", user=current_user, form=form, action='Add')

@login_required
@app.route('/edit_stuff/<stuff_id>',methods=["GET", "POST"])
def edit_stuff(stuff_id):

    form = EditStuffForm()
    if current_user.addresses:
        address_choices = [(address.id,address.name)for address in current_user.addresses]
    else:
        address_choices = [('none','None')]
    form.address.choices = address_choices
    if request.method == 'POST' and form.validate_on_submit():
        stuff = Stuff.query.filter(Stuff.id == form.stuffid.data)
        stuff.update({Stuff.title: form.title.data,
                            Stuff.detail: form.detail.data,
                            Stuff.address_id: form.address.data
                            })
        db.session.commit()
    obj = Stuff.query.filter(Stuff.id == stuff_id).first()
    if obj:
        form.fill_form(obj)
    return render_template("edit_stuff.html", user=current_user, form=form, action='Edit')

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