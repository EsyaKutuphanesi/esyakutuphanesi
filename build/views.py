import uuid
import json

from flask import render_template, send_from_directory, flash
from flask_login import current_user, login_required
from forms import *
from oauth_handler import *
import os.path


@app.route('/')
@app.route('/categories')
def home():
    form = SeachForm()
    last_objects_shared = Stuff.query.filter(Stuff.approved == 1,
                                             Stuff.is_wanted == 0).order_by(Stuff.id.desc()).limit(8)
    last_objects_wanted = Stuff.query.filter(Stuff.approved == 1,
                                             Stuff.is_wanted == 1).order_by(Stuff.id.desc()).limit(8)

    return render_template("index.html", user=current_user,
                           last_objects_wanted=last_objects_wanted, last_objects_shared=last_objects_shared, form=form)

@app.route('/search')
def search():
    form = SeachForm()
    last_objects = list()

    if request.method == 'GET':
        stuff_key = unicode(request.args.get('stuff'))
        address_key = unicode(request.args.get('address'))
        print stuff_key
        last_objects = Stuff.query.join(Address).\
            filter(Stuff.approved == 1,
                   Address.id == Stuff.address_id,
                   Stuff.title.like('%'+stuff_key+'%'),
                   Address.detail.like('%'+address_key+'%')).limit(8)

    return render_template("search.html", user=current_user,
                           last_objects=last_objects, form=form)

@app.route('/new_address', methods=["GET", "POST"])
@login_required
def new_address():
    if request.method == 'POST':
        print unicode(request.form)
        address = Address(user=current_user,
                          lat=request.form.get('lat'),
                          lng=request.form.get('lng'),
                          detail=unicode(request.form.get('address_str')),
                          name=request.form.get('address_name'))
        db.session.add(address)
        db.session.commit()
        flash(u"Adresiniz kaydedildi")

        return redirect(url_for("edit_profile"))
    return render_template("map.html", user=current_user)

@app.route('/edit_stuff/<stuff_id>', methods=["GET", "POST"])
@app.route('/new_stuff', methods=["GET", "POST"])
@login_required
def edit_stuff(stuff_id=None):
    stuff = Stuff.query.filter(Stuff.id == stuff_id).first()
    form = EditStuffForm()
    is_new = True
    is_wanted = unicode(request.args.get('is_wanted'))
    if is_wanted == 'true':
        form.is_wanted.data = 'True'

    address_choices = []
    if current_user.addresses:
        address_choices = [(address.id, address.detail)
                           for address in current_user.addresses]
    address_choices += [(20, u'Yeni Adres')]
    #else:
    #    flash('Adres girmeniz gerekiyor')
    #    return redirect(url_for("new_address",
    #                            next=request.script_root+request.path))

    form.address.choices = address_choices

    if current_user.groups:
        group_choices = [(membership.group.id, membership.group.name)
                         for membership in current_user.groups]
        group_choices = [(-1, u'Herkese Acik')] + group_choices
    else:
        group_choices = [(-1, u'Herkese Acik')]

    form.group.choices = group_choices

    categories = Category.query.order_by(Category.name)
    category_choices = [(category.id, category.name)
                        for category in categories]
    form.category.choices = category_choices
    if stuff:
        category = Category.query. \
            filter(Category.id == stuff.category_id).first()
    else:
        category = categories[0]
    stuff_types = category.type_list
    stuff_type_choices = [(stuff_type.id, stuff_type.name)
                          for stuff_type in stuff_types]
    form.stuff_type.choices = stuff_type_choices

    if request.method == 'POST':
        category = Category.query.\
            filter(Category.id == form.category.data).first()

        stuff_types = category.type_list
        stuff_type_choices = [(stuff_type.id, stuff_type.name)
                              for stuff_type in stuff_types]
        form.stuff_type.choices = stuff_type_choices
        print unicode(request.form.get('address_str'))
        if form.validate_on_submit():
            photo_file = form.photo.data
            if photo_file:
                file_ext = get_file_extension(photo_file.filename)
                generated_name = str(uuid.uuid1())+'.'+file_ext
                filepath = os.path.join(app.config['UPLOADS_FOLDER'],
                                        generated_name)
                photo_file.save(filepath)

            if form.address.data == 20:
                address = Address(user=current_user,
                                  lat=request.form.get('lat'),
                                  lng=request.form.get('lng'),
                                  detail=unicode(request.form.get('address_str')),
                                  name="addr")
                db.session.add(address)
            else:
                address = Address.query.\
                    filter(Address.id == form.address.data).\
                    first()
            if stuff:
                stuff.title = form.title.data
                stuff.detail = form.detail.data
                stuff.stuff_address = address
                stuff.category_id = form.category.data
                stuff.type_id = form.stuff_type.data
                stuff.is_wanted = form.is_wanted.data == 'True'
                if photo_file:
                    new_photo = StuffPhoto(owner=current_user,
                                           filename=generated_name,
                                           stuff=stuff)
                    db.session.add(new_photo)
                    db.session.commit()
                flash("Esya guncellendi")

            else:
                stuff = Stuff(title=form.title.data,
                              detail=form.detail.data,
                              stuff_address=address,
                              owner=current_user,
                              category_id=form.category.data,
                              type_id=form.stuff_type.data,
                              group_id=form.group.data,
                              is_wanted=form.is_wanted.data == 'True')
                db.session.add(stuff)
                if photo_file:
                    new_photo = StuffPhoto(owner=current_user,
                                           filename=generated_name,
                                           stuff=stuff)
                    db.session.add(new_photo)
                    db.session.commit()
                flash("Esya kaydedildi")

            tags = form.tags.data.split(',')
            for t in tags:
                if t > '':
                    new_tag = Tag(stuff=stuff, name=t)
                    db.session.add(new_tag)

            db.session.commit()
            if stuff_id is None:
                return redirect(url_for('edit_stuff', stuff_id=stuff.id))


    if stuff:
        is_new = False

        if stuff.group_id > 0:
            group_choices = [(stuff.group_id, stuff.group.name)]
        else:
            group_choices = [(-1, u'Herkese Acik')]

        form.group.choices = group_choices
        form.fill_form(stuff)

    return render_template("edit_stuff.html", user=current_user,
                           form=form, action='Edit', stuff=stuff,
                           is_new=is_new)

@app.route('/my_stuff')
@login_required
def my_stuff():
    return render_template("my_stuff.html", user=current_user)

@app.route('/get_stuff_types/<category_id>')
@app.route('/get_stuff_types')
def get_stuff_types(category_id=None):
    if category_id:
        category = Category.query.filter(Category.id == category_id).first()
        stuff_types = category.type_list
    else:
        stuff_types = StuffType.query.order_by(StuffType.name)

    stuff_type_choices = [{"id": stuff_type.id, "name": stuff_type.name}
                          for stuff_type in stuff_types]
    stuff_type_choices_json = json.dumps(stuff_type_choices)

    return stuff_type_choices_json

@app.route('/get_categories')
@app.route('/get_categories/<type_id>')
def get_categories(type_id=None):
    if type_id:
        stuff_type = StuffType.query.filter(StuffType.id == type_id).first()
        categories = stuff_type.category_list
    else:
        categories = Category.query.order_by(Category.name)

    category_list = [{"id": category.id, "name": category.name}
                     for category in categories]
    category_list_json = json.dumps(category_list)

    return category_list_json

@app.route('/show_stuff/<stuff_id>')
def show_stuff(stuff_id):
    stuff = Stuff.query.filter(Stuff.id == stuff_id).first()
    stuff_owner = User.query.filter(User.id == stuff.owner_id).first()

    stuff_address = Address.query.filter(Address.id == stuff.address_id).first()

    return render_template("show_stuff.html", stuff_address=stuff_address, stuff_owner=stuff_owner, user=current_user, stuff=stuff)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditUserForm()

    if request.method == 'POST' and form.validate_on_submit():
        if current_user.id == int(form.userid.data):
            photo_file = form.photo.data

            if photo_file:
                file_ext = get_file_extension(photo_file.filename)
                generated_name = str(uuid.uuid1())+'.'+file_ext
                filepath = os.path.join(app.config['UPLOADS_FOLDER'],
                                        generated_name)
                photo_file.save(filepath)
                new_photo = Photo(owner=current_user, filename=generated_name)
                db.session.add(new_photo)
                db.session.commit()

            User.query.filter(User.id == current_user.id).\
                update({User.name: form.name.data,
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
    return send_from_directory(app.root_path + '/static/photos/', filename)

def get_file_extension(filename):
    if '.' in filename:
        return filename.rsplit('.', 1)[1]

@app.route('/category/<category_name>/')
def category_view(category_name=None):
    is_wanted = request.args.get('is_wanted')

    category = Category.query.\
        filter(Category.name == category_name).first()
    #stuff_list = category.stuff_list
    if is_wanted is None:
        stuff_list = Stuff.query.\
            filter(Stuff.category == category).\
            limit(20)
    else:
        stuff_list = Stuff.query.\
            filter(Stuff.category == category,
                   Stuff.is_wanted == is_wanted).\
            limit(20)
    params = {
        'category': {
            'type': 'category',
            'value': category.id
        },
        'stuff_type': {
            'type': 'stuff_type',
            'value': 'all'
        },
        'is_wanted': {
            'type': 'is_wanted',
            'value': is_wanted if is_wanted is not None else 2
        }
    }

    return render_template("browse.html", user=current_user,
                           stuff_list=stuff_list, params=params)

#@app.route('/stuff_type/<type_name>/')
#def stuff_type_view(type_name=None):
#    stuff_type = StuffType.query.\
#        filter(StuffType.name == type_name).first()
#    stuff_list = stuff_type.stuff_list
#    params = {
#        'stuff_type': {
#            'type': 'stuff_type',
#            'value': stuff_type.id
#        },
#    }
#    return render_template("browse.html", user=current_user,
#                           stuff_list=stuff_list, params=params)

@app.route('/category/<category_name>/type/<type_name>')
def category_stuff_type_view(category_name, type_name):
    is_wanted = request.args.get('is_wanted')
    stuff_type = StuffType.query.\
        filter(StuffType.name == type_name).first()
    category = Category.query.\
        filter(Category.name == category_name).first()
    if is_wanted is None:
        stuff_list = Stuff.query.\
            join(Category).\
            join(StuffType).\
            filter(StuffType.id == stuff_type.id).\
            filter(Category.id == category.id).\
            limit(8)
    else:
        stuff_list = Stuff.query.\
            join(Category).\
            join(StuffType).\
            filter(StuffType.id == stuff_type.id).\
            filter(Category.id == category.id).\
            filter(Stuff.is_wanted == is_wanted).\
            limit(8)

    params = {
        'category': {
            'type': 'category',
            'value': category.id
        },
        'stuff_type': {
            'type': 'stuff_type',
            'value': stuff_type.id
        },
        'is_wanted': {
            'type': 'is_wanted',
            'value': is_wanted if is_wanted is not None else 2
        }
    }

    return render_template("browse.html", user=current_user,
                           stuff_list=stuff_list, params=params)

@app.route('/my_messages')
@login_required
def my_messages():
    return render_template("my_messages.html", user=current_user)

@app.route('/conversations/<conversation_id>', methods=["GET", "POST"])
@login_required
def show_conversation(conversation_id):
    conversation = Conversation.query.\
        filter(Conversation.id == conversation_id).first()

    if current_user not in conversation.users:
        redirect('/my_messages')

    form = ConversationForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_message = Message(user=current_user,
                              conversation=conversation,
                              txt=form.message.data)
        db.session.add(new_message)
        db.session.commit()

    return render_template("conversation.html", user=current_user,
                           form=form, action='Edit', conversation=conversation)

@app.route('/make_request/<stuff_id>')
@login_required
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
                          txt='Merhaba %s, %s esyasini istiyorum'
                              % (stuff.owner.name, stuff.title))
    db.session.add(new_message)

    db.session.commit()
    return render_template("my_messages.html", user=current_user)

@app.route('/moderation')
@login_required
def moderation():
    action = request.args.get("action")
    id = request.args.get("id")

    if action == 'approve' and id>0:
        if 'admin' in current_user.roles:
            stuff = Stuff.query.filter(Stuff.approved == 0,
                                       Stuff.id == id). \
                order_by(Stuff.id.desc()).first()
        else:
            stuff = Stuff.query.join(Group).join(GroupMembership) \
                .filter(GroupMembership.user_id == current_user.id,
                        GroupMembership.is_moderator,
                        Stuff.id == id,
                        Stuff.approved == 0). \
                order_by(Stuff.id.desc()).first()
        if stuff:
            stuff.approved = 1
            db.session.commit()

    if 'admin' in current_user.roles:
        last_objects = Stuff.query.filter(Stuff.approved == 0).\
            order_by(Stuff.id.desc()).limit(8)
    else:
        last_objects = Stuff.query.join(Group).join(GroupMembership)\
            .filter(GroupMembership.user_id == current_user.id,
                    GroupMembership.is_moderator,
                    Stuff.approved == 0).\
            order_by(Stuff.id.desc()).limit(8)

    return render_template("moderation.html", user=current_user,
                           last_objects=last_objects)

@app.route('/profile/<user_id>')
def get_profile(user_id):
    user_profile = User.query.filter(User.id == user_id).first()
    user_stuff_shared = Stuff.query.filter(Stuff.owner_id == user_id, Stuff.is_wanted == 0).limit(8)
    user_stuff_wanted = Stuff.query.filter(Stuff.owner_id == user_id, Stuff.is_wanted == 1).limit(8)

    users_group = Group.query.join(GroupMembership).\
        filter(GroupMembership.group_id == Group.id,
               GroupMembership.user_id == user_id)

    return render_template("profile.html", user_stuff_shared=user_stuff_shared, user_stuff_wanted=user_stuff_wanted,
                           users_group=users_group, user_profile=user_profile, user=current_user)

@app.route('/groups')
@login_required
def groups():

    return render_template("groups.html", user=current_user)

@app.route('/group/<group_id>')
@login_required
def group(group_id):
    group_info = Group.query.filter(Group.id == group_id).first()

    group_shares = Stuff.query.filter(Stuff.group_id == group_id)

    group_members = User.query.join(GroupMembership).\
        filter(GroupMembership.group_id == group_id, User.id == GroupMembership.user_id)

    for members_photos in group_members:
        photos = Photo.query.filter(Photo.owner_id == members_photos.id)

    return render_template("group.html", group_info=group_info, group_shares=group_shares,
                           group_members=group_members, photos=photos, user=current_user)

@app.route('/invite') #, methods=["GET", "POST"]
@login_required
def invite():
    # if request.method == 'POST':
    #         print unicode(request.form)
    #         invite_info = Invitations(user=current_user,
    #                           emails=request.form.get('invited-emails'),
    #                           message=request.form.get('invite_message'),
    #         db.session.add(invitations)
    #         db.session.commit()
    #         flash(u"")
    #
    #         return redirect(url_for("invite"))
    return render_template("invite.html", user=current_user)