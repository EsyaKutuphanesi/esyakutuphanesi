# -*- coding: utf-8 -*-

from datetime import datetime

from flask.ext.security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, Security
from __init__ import app, db
from flask_security.forms import RegisterForm
from wtforms.validators import Required, Length
from wtforms import TextField, TextAreaField, BooleanField

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

conversation_users = db.Table(
    'conversation_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('conversation_id', db.Integer(), db.ForeignKey('conversation.id'))
)

categories_types = db.Table(
    'categories_types',
    db.Column('category_id', db.Integer(), db.ForeignKey('category.id')),
    db.Column('stufftype_id', db.Integer(), db.ForeignKey('stufftype.id'))
)

"""
stuff_type_stuff_list = db.Table('stuff_type_stuff_list',
        db.Column('stuff_id', db.Integer(), db.ForeignKey('stuff.id')),
        db.Column('stufftype_id', db.Integer(), db.ForeignKey('stufftype.id')))
"""


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        return self.name

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'role', self.id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    about = db.Column(db.String(1000))
    why = db.Column(db.String(1000))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=False)
    approved = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    registered_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def is_logged_in(self):
        return False if self.is_anonymous() else True

    @property
    def is_admin(self):
        return self.roles and self.roles[0].name == 'admin'

    def __repr__(self):
        return self.name

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'user', self.id)

    @property
    def url(self):
        return "%s/%s/" % ('profiles', self.name)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    detail = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref="addresses")
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '%s[%s]' % (self.name, self.user.name)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'address', self.id)

    @property
    def url(self):
        return "%s/%s/" % ('addresses', self.id)


class Stuff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(10000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='stuff_list')
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    stuff_address = db.relationship('Address', backref='stuff_list')
    date = db.Column(db.DateTime, default=datetime.now)
    stuff_type = db.relationship('StuffType', backref='stuff_list')
    type_id = db.Column(db.Integer, db.ForeignKey('stufftype.id'))
    category = db.relationship('Category', backref='stuff_list')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    group = db.relationship('Group', backref='stuff_list')
    approved = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=1)
    is_wanted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "%s" % (self.title)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'stuff', self.id)

    @property
    def edit_url(self):
        return "%s/%s" % ('edit_stuff', self.id)

    @property
    def url(self):
        return "%s/%s" % ('show_stuff', self.id)


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='photos')


class StuffPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='object_photos')
    stuff_id = db.Column(db.Integer, db.ForeignKey('stuff.id'))
    stuff = db.relationship('Stuff', backref='photos')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    stuff_id = db.Column(db.Integer, db.ForeignKey('stuff.id'))
    stuff = db.relationship('Stuff', backref='tags')

    def __repr__(self):
        return "%s" % (self.name)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return self.name

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'category', self.id)

    @property
    def url(self):
        return "%s/%s/" % ('category', self.name)


class StuffType(db.Model):
    __tablename__ = "stufftype"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    category_list = db.relationship(
        'Category',
        secondary=categories_types,
        backref=db.backref('type_list', lazy='dynamic')
    )

    def __repr__(self):
        return self.name

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'stufftype', self.id)

    @property
    def url(self):
        return "%s/%s/" % ('stuff_type', self.name)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stuff_id = db.Column(db.Integer, db.ForeignKey('stuff.id'))
    stuff = db.relationship('Stuff', backref='requests')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='requests', foreign_keys=[user_id])
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_user = db.relationship('User', backref='incoming_requests', foreign_keys=[from_user_id])
    status = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    given_at = db.Column(db.DateTime)
    returned_at = db.Column(db.DateTime)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'request', self.id)

    @property
    def url(self):
        return "%s/%s" % ('request', self.id)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship('User', secondary=conversation_users,
                            backref=db.backref('conversations', lazy='dynamic'))
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    request = db.relationship('Request', backref='conversation')
    title = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'conversation', self.id)

    @property
    def url(self):
        return "%s/%s" % ('conversation', self.id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_user = db.relationship('User', backref='incoming_messages', foreign_keys=[to_user_id])
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_user = db.relationship('User', backref='messages', foreign_keys=[from_user_id])
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    conversation = db.relationship('Conversation', backref='messages')
    txt = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Integer, default=0)

    def __repr__(self):
        return self.txt

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'conversation', self.id)

    @property
    def url(self):
        return "%s/%s" % ('conversation', self.id)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(1000))
    logo = db.Column(db.String(255), nullable=False)
    members = db.relationship("GroupMembership", backref="group")

    def __repr__(self):
        return self.name


class GroupMembership(db.Model):
    __tablename__ = 'group_membership'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), primary_key=True)
    is_moderator = db.Column(db.Boolean)
    user = db.relationship("User", backref='groups')

    def __repr__(self):
        return "%s[%s] " % (self.user.name, self.group.name)


class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    full_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)
    user = db.relationship('User', backref='social_connections')


class Invitations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    emails = db.Column(db.String(255))
    message = db.Column(db.String(1000))
    datetime = db.Column(db.DateTime, default=datetime.now)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='reviews', foreign_keys=[user_id])
    reviewed_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_user = db.relationship('User', backref='reviews_about', foreign_keys=[reviewed_user_id])
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    request = db.relationship('Request', backref='reviews')
    comment = db.Column(db.String(1000))
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return str(self.id)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'review', self.id)

    @property
    def url(self):
        return "%s/%s/" % ('review', self.id)

users = SQLAlchemyUserDatastore(db, User, Role)
# social = Social(app, SQLAlchemyConnectionDatastore(db, Connection))


class ExtendedRegisterForm(RegisterForm):
    name = TextField(u'İsim Soyisim', [Required(u'İsmini girmen gerekli')])
    why = TextAreaField(
        u'Eşya Kütüphanesi\'ne neden geldiğinden kısaca bahsedebilir misin? '
        u'Mesela buradan beklentilerin neler? '
        u'Bizi nereden duydun?',
        [Length(min=0, max=1000, message=u'En fazla 1000 karakter girebilirsin.'),
         Required(u'Seni daha yakından tanımayı istiyoruz.')]
    )
    about = TextAreaField(
        u'Hobilerin neler? Bir ejderhan olsa adını ne koyardın? '
        u'En sevdiğin yemek ne? Boş zamanlarında ne yapmaktan hoşlanırsın?',
        [Length(min=0, max=1000, message=u'En fazla 1000 karakter girebilirsin.'),
         Required(u'Bize biraz kendinden bahseder misin?')]
    )
    agreement = BooleanField('', [Required(u'Kullanıcı sözleşmesini onaylamalısın.')])

security = Security(app, users, register_form=ExtendedRegisterForm)
