from flask.ext.login import current_user, flash, redirect, url_for
from flask.ext.admin import Admin, AdminIndexView, expose

from ek import app, db
from models import User, Role, Address, Stuff, Category, StuffType,\
    Group, GroupMembership, Request

from flask.ext.admin.contrib.sqla import ModelView


class DemoAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin

admin = Admin(app, url='/admin', base_template='admin_layout.html',
              index_view=DemoAdminIndexView())


class ExtendedModelView(ModelView):

    def is_accessible(self):
        return current_user.roles[0].name == 'admin'

    def __init__(self, model, session, **kwargs):
        # You can pass name and other parameters if you want to
        available_settings = [
            'column_list',
            'column_searchable_list',
            'list_template',
            'column_filters',
            'column_sortable_list'
        ]
        for setting in available_settings:
            if setting in kwargs:
                self.__setattr__(setting, kwargs[setting])
                del(kwargs[setting])
        super(ExtendedModelView, self).__init__(model, session, **kwargs)


class UserView(ExtendedModelView):

    @expose('/userview/approve/<id>')
    def approval_view(self, id):
        flash('%s is approved' % str(id))
        return redirect(url_for('.index_view'))

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)


admin.add_view(
    UserView(
        db.session,
        column_list=('id', 'email', 'why', 'approved'),
        list_template='admin_user_list.html',
        column_searchable_list=('email',),
        column_sortable_list=('id',),
        column_filters=('id', 'email', 'approved')
    )
)

admin.add_view(ExtendedModelView(Role, db.session))

admin.add_view(
    ExtendedModelView(
        Stuff,
        db.session,
        column_list=('id', 'owner', 'stuff_address', 'stuff_type', 'category', 'title', 'detail', 'create_at', 'approved'),
        column_searchable_list=('title', 'detail',),
        column_sortable_list=(('id', Stuff.id),),
        column_filters=('id', 'stuff_type', 'category', 'approved', 'owner')
    )
)


admin.add_view(ExtendedModelView(Category, db.session))
admin.add_view(ExtendedModelView(StuffType, db.session))
admin.add_view(ExtendedModelView(Request, db.session))


# admin.register(User, session=db.session)
# admin.register(Role, session=db.session)
# admin.register(Address, session=db.session)
# admin.register(Stuff, session=db.session)
# admin.register(Category, session=db.session)
# admin.register(StuffType, session=db.session)
# admin.register(Group, session=db.session)
# admin.register(GroupMembership, session=db.session)
