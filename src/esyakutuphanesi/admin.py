# -*- coding: utf-8 -*-
from flask import render_template
from flask.ext.login import current_user, flash, redirect, url_for
from flask.ext.admin import Admin, AdminIndexView, expose
from flask_mail import Message as MailMessage

from __init__ import app, db, mail
from models import User, Role, Stuff, Category, StuffType, Request

from flask.ext.admin.contrib.sqla import ModelView


class DemoAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated() and current_user.is_admin

admin = Admin(
    app,
    url='/admin',
    base_template='admin_layout.html',
    index_view=DemoAdminIndexView()
)


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
        unapproved_user = User.query.filter(User.approved == False, User.id == id).first()
        if not unapproved_user:
            flash(u"Kullanıcı zaten onaylı!")
            return redirect(url_for('.index_view'))

        unapproved_user.approved = True
        db.session.commit()

        msg_body = render_template('email/welcome.txt', user=unapproved_user)
        html_msg = render_template('email/welcome.html', user=unapproved_user)

        msg_subject = u"Hoşgeldin!"
        msg = MailMessage(
            body=msg_body,
            html=html_msg,
            subject=msg_subject,
            sender=(u"Eşya Kütüphanesi", "no-reply@esyakutuphanesi.com"),
            recipients=[unapproved_user.email]
        )

        mail.send(msg)
        flash(u"Kullanıcı onaylandı ve e-posta gönderildi!")
        return redirect(url_for('.index_view'))

    @expose('/userview/request_detail/<id>')
    def request_detail_view(self, id):
        unapproved_user = User.query.filter(User.approved == False, User.id == id).first()
        if not unapproved_user:
            flash(u"Kullanıcı zaten onaylı!")
            return redirect(url_for('.index_view'))

        msg_body = render_template('email/request_detail.txt', user=unapproved_user)
        html_msg = render_template('email/request_detail.html', user=unapproved_user)

        msg_subject = u"Ufak bir rica!"
        msg = MailMessage(
            body=msg_body,
            html=html_msg,
            subject=msg_subject,
            sender=(u"Eşya Kütüphanesi", "bilgi@esyakutuphanesi.com"),
            recipients=[unapproved_user.email]
        )

        mail.send(msg)
        flash(u"Kullanıcıya e-posta gönderilerek daha fazla bilgi vermesi talep edildi!")
        return redirect(url_for('.index_view'))

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)


admin.add_view(
    UserView(
        db.session,
        column_list=('id', 'name', 'email', 'why', 'approved'),
        list_template='admin_user_list.html',
        column_searchable_list=('email', 'name'),
        column_sortable_list=('id',),
        column_filters=('id', 'name', 'email', 'approved')
    )
)

admin.add_view(ExtendedModelView(Role, db.session))

admin.add_view(
    ExtendedModelView(
        Stuff,
        db.session,
        column_list=('id', 'owner', 'stuff_address', 'stuff_type', 'category',
                     'title', 'detail', 'create_at', 'approved'),
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
