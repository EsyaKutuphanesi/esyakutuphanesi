from flask_login import current_user
from flask_superadmin import Admin, AdminIndexView, expose

from ek import app, db
from models import User, Role, Address, Stuff, Category, StuffType,\
    Group, GroupMembership


class AdminIndexView(AdminIndexView):

    def is_accessible(self):
        return current_user.is_authenticated()

    @expose('/')
    def index(self):
        users = User.query.order_by(User.id.desc()).limit(5)

        return self.render('admin/index.html',
                           users=users,
                           )

admin = Admin(app, app.config['NAME'], url=app.config['ADMIN_URL'], index_view=AdminIndexView())

admin.register(User, session=db.session)
admin.register(Role, session=db.session)
admin.register(Address, session=db.session)
admin.register(Stuff, session=db.session)
admin.register(Category, session=db.session)
admin.register(StuffType, session=db.session)
admin.register(Group, session=db.session)
admin.register(GroupMembership, session=db.session)