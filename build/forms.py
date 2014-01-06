# coding=utf-8
from flask_security.forms import RegisterForm
from flask_wtf import Form, TextField,Required, HiddenField, PasswordField,validators, SubmitField
from flask_wtf import TextAreaField, SelectField, FileField

from models import User

class ExtendedRegisterForm(RegisterForm):
    name = TextField('Ad Soyad', [Required()])
    nickname = TextField('Takma Ad', [Required()])


class EditUserForm(Form):
    userid = HiddenField('userid');
    photo = FileField(u'Resim Yükle')
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
    about = TextAreaField(u'Hakkınızda', [
        validators.Length(min=0, max=1000),
    ])
    password = PasswordField(u'Yeni Şifre', [
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField(u'Şifreyi Onayla')

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

class EditStuffForm(Form):
    stuffid = HiddenField('stuffid');
    photo = FileField(u'Resim Yükle')
    title = TextField('Esya Tanimi', [
        validators.Length(min=4, max=255),
        validators.Required()
    ])
    detail = TextAreaField('Detaylar', [
        validators.Length(min=0, max=1000),
    ])
    address = SelectField('Adress', coerce=int)
    submit = SubmitField("Kaydet")
    tags = TextField(u'Etiketler',[
        validators.Length(min=0, max=255)
    ])
    def fill_form(self, stuff):
        self.tags.data=''
        self.title.data = stuff.title
        self.detail.data = stuff.detail
        self.stuffid.data = stuff.id
        self.address.data = stuff.address_id

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True

class SeachForm(Form):
    stuff = TextField(u'Ne Arıyorsun?', [
        validators.Length(min=0, max=255)
    ])

    address = TextField(u'Nerede Arıyorsun?', [
        validators.Length(min=0, max=255)
    ])
    submit = SubmitField("Ara")
