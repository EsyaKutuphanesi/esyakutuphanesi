from flask.ext.login import current_user
from flask.ext.superadmin import Admin, AdminIndexView, expose

from ek import app, db
from models import User, Role, Category, Thing, Object


class AdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/')
    def index(self):
        objects = Object.query.order_by(Object.id.desc()).limit(5)
        users = User.query.order_by(User.id.desc()).limit(5)
        categories = Category.query.order_by(Category.id.desc()).limit(5)
        things = Thing.query.order_by(Thing.id.desc()).limit(5)
        return self.render('admin/index.html',
                           objects=objects,
                           users=users,
                           categories=categories,
                           things=things
                           )

admin = Admin(app, app.config['NAME'], url=app.config['ADMIN_URL'], index_view=AdminIndexView())

admin.register(User, session=db.session)
admin.register(Role, session=db.session)
admin.register(Category, session=db.session)
admin.register(Thing, session=db.session)
admin.register(Object, session=db.session)
