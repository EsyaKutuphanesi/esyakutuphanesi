# coding=utf-8
from flask_security.forms import RegisterForm
from flask_wtf import Form, TextField,Required, HiddenField, PasswordField,validators, SubmitField
from flask_wtf import TextAreaField

from models import User

class ExtendedRegisterForm(RegisterForm):
    name = TextField('Ad Soyad', [Required()])
    nickname = TextField('Takma Ad', [Required()])


class EditUserForm(Form):
    userid = HiddenField('userid');
    name = TextField('Isminiz', [
        validators.Length(min=4, max=25),
        validators.Required()
    ])
    nickname = TextField('Takma Isim', [
        validators.Length(min=4, max=25),
        validators.Required()
    ])
    email = TextField('E-Posta Adresiniz', [
        validators.Length(min=6, max=35),
        validators.Required()
    ])
    phone_number = TextField('Telefonunuz', [
        validators.Length(min=0, max=35),
    ])
    about = TextAreaField('Hakkinizda', [
        validators.Length(min=0, max=1000),
    ])
    password = PasswordField('New Password', [
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    submit = SubmitField("Kaydet")

    def fill_form(self, user):
        self.name.data = user.name
        self.nickname.data = user.nickname
        self.email.data = user.email
        self.userid.data = user.id
        self.phone_number.data = user.phone_number
        self.about.data = user.about

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data).first()
        print self.userid.data
        print user.id
        if user and user.id <> int(self.userid.data):
            self.email.errors.append('There is already a user registered with this email')
            return False

        user = User.query.filter_by(
            nickname=self.nickname.data).first()
        if user and user.id <> int(self.userid.data):
            self.nickname.errors.append('This nickname is already taken')
            return False

        return True