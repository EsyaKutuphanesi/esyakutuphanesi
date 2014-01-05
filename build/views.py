from flask import render_template, flash, redirect, request
from flask_login import current_user, login_required
from sqlalchemy.orm.exc import NoResultFound
from forms import *
from ek import app, db


from models import users, User, Role, Address, Object

@app.route('/')
def home():
    last_objects = Object.query.order_by(Object.id.desc()).limit(5)
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
@app.route('/new_object',methods=["GET", "POST"])
def new_object():
    form = EditObjectForm()
    if current_user.addresses:
        address_choices = [(address.id,address.name)for address in current_user.addresses]
    else:
        address_choices = [('none','None')]
    form.address.choices = address_choices
    if request.method == 'POST' and form.validate_on_submit():
        print unicode(request.form)
        address = Address.query.filter(Address.id == form.address.data, Address.user_id==current_user.id).first()
        print address
        new_object = Object(title=form.title.data,
                            detail=form.detail.data,
                            address=address,
                            owner=current_user)
        print new_object
        db.session.add(new_object)
        db.session.commit()
    return render_template("new_object.html", user=current_user, form=form)

@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    print current_user.is_anonymous()
    if current_user.is_anonymous():
        return redirect('/')
    form = EditUserForm()
    if request.method == 'POST' and form.validate_on_submit():
        if current_user.id == int(form.userid.data):
            User.query.filter(User.id == current_user.id).update({
                                  User.name: form.name.data,
                                  User.email: form.email.data,
                                  User.nickname: form.nickname.data,
                                  User.phone_number: form.phone_number.data,
                                  User.about: form.about.data})
            db.session.commit()

    form.fill_form(current_user)
    return render_template('profile.html',
                           form=form,
                           user=current_user)