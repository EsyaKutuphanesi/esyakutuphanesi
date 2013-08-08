from datetime import datetime

from flask.ext.security import UserMixin, RoleMixin, SQLAlchemyUserDatastore, Security

from ek import app, db, RESPONSE_CHOICES



roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

categories_things = db.Table('categories_things',
        db.Column('category_id', db.Integer(), db.ForeignKey('category.id')),
        db.Column('thing_id', db.Integer(), db.ForeignKey('thing.id')))

objects_things = db.Table('objects_things',
        db.Column('object_id', db.Integer(), db.ForeignKey('object.id')),
        db.Column('thing_id', db.Integer(), db.ForeignKey('thing.id')))

users_things = db.Table('users_things',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('thing_id', db.Integer(), db.ForeignKey('thing.id')))


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
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    registered_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return self.name

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'user', self.id)

    @property
    def url(self):
        return "%s/%s" % ('profiles', self.nickname)


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
        return "%s/%s" % ('categories', self.name)


class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    categories = db.relationship('Category', secondary=categories_things, backref=db.backref('things', lazy='dynamic'))

    def __repr__(self):
        return self.name

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'thing', self.id)

    @property
    def url(self):
        return "%s/%s" % ('things', self.name)


class Object(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref='objects')
    thing_id = db.Column(db.Integer, db.ForeignKey('thing.id'))
    thing = db.relationship('Thing', backref='objects')
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "%s's %s" % (self.owner, self.thing)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'object', self.id)

    @property
    def url(self):
        return "%s/%s/%s/%s" % ('profiles', self.owner.nickname, 'objects', self.id)


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    by = db.relationship('User', backref=db.backref('requests', lazy='dynamic'))
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'))
    object = db.relationship('Object', backref=db.backref('requests', lazy='dynamic'))
    date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "%s requested %s" % (self.by, self.object)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'request', self.id)

    @property
    def url(self):
        return "%s/%s/%s/%s" % ('profiles', self.owner.nickname, 'requests', self.id)


class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    request = db.relationship('Request', backref=db.backref('responses', lazy='dynamic'))
    date = db.Column(db.DateTime, default=datetime.now)
    response = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return "%s %s %s's %s request." % (self.request.object.owner, RESPONSE_CHOICES[self.response], self.request.by, self.request.object.thing)

    @property
    def admin_url(self):
        return "%s/%s/%s" % (app.config['ADMIN_URL'], 'response', self.id)

    @property
    def url(self):
        return "%s/%s/%s/%s" % ('profiles', self.owner.nickname, 'responses', self.id)

users = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, users)