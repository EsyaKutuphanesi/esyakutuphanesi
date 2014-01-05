from datetime import datetime

from flask_security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, Security

from ek import app, db

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

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
    nickname = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    about = db.Column(db.String(1000))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    registered_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def is_logged_in(self):
        return False if self.is_anonymous() else True

    def __repr__(self):
        return self.name

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'user', self.id)

    @property
    def url(self):
        return "%s/%s/" % ('profiles', self.nickname)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    detail = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref="addresses")
    detail = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '%s[%s]' % (self.name,self.user.nickname)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'address', self.id)

    @property
    def url(self):
        return "%s/%s/" % ('addresses', self.id)


class Stuff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    detail = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='stuff_list')
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    stuff_address = db.relationship('Address', backref='stuff_list')
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "%s's %s" % (self.owner, self.title)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'stuff', self.id)

    @property
    def url(self):
        return "%s/%s/%s/%s/" % ('profiles', self.owner.nickname, 'stuff', self.id)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='photos')

class ObjectPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='object_photos')
    stuff_id = db.Column(db.Integer, db.ForeignKey('stuff.id'))
    stuff = db.relationship('Stuff', backref='photos')
users = SQLAlchemyUserDatastore(db, User, Role)
