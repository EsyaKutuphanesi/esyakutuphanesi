# coding=utf-8
from flask_security.forms import RegisterForm
from flask.ext.wtf import Form
from wtforms import TextField, HiddenField, PasswordField, validators, SubmitField
from wtforms import TextAreaField, SelectField, FileField
from wtforms.validators import Required

from models import User

class ExtendedRegisterForm(RegisterForm):
    name = TextField(u'İsim Soyisim', [Required()])


class EditUserForm(Form):
    userid = HiddenField('userid');
    photo = FileField(u'Resim Yükle')
    name = TextField(u'İsim', [
        validators.Length(min=4, max=25),
        validators.Required()
    ])
    email = TextField(u'Email Adresi', [
        validators.Length(min=6, max=35),
        validators.Required()
    ])
    phone_number = TextField(u'Telefon', [
        validators.Length(min=0, max=35),
    ])
    about = TextAreaField(u'Sevdiklerin', [
        validators.Length(min=0, max=1000),
    ])
    password = PasswordField(u'Yeni Şifre', [
        validators.EqualTo('confirm', message=u'Şifreler aynı olmalı.')
    ])
    confirm = PasswordField(u'Şifreyi Onayla')

    submit = SubmitField(u"Güncelle")

    def fill_form(self, user):
        self.name.data = user.name
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
            self.email.errors.append(u'Bu email adresi ile kayıtlı bir kullanıcı bulunuyor.')
            return False

        return True

class EditStuffForm(Form):
    stuffid = HiddenField('stuffid')
    photo = FileField(u'Resim Yükle')
    title = TextField(u'Başlık', [
        validators.Length(min=4, max=255),
        validators.Required()
    ])
    detail = TextAreaField(u'Detaylar', [
        validators.Length(min=0, max=1000),
        validators.Required()
    ])
    address = SelectField(u'Adres', coerce=int, validators=[validators.Required()])
    group = SelectField(u'Grup', coerce=int, validators=[validators.Required()])
    submit = SubmitField("Kaydet")
    tags = TextField(u'Etiketler',[
        validators.Length(min=0, max=255)
    ])
    category = SelectField('Kategori', coerce=int, validators=[validators.Required()])
    stuff_type = SelectField(u'Eşya Türü', coerce=int, validators=[validators.Required()])
    is_wanted = SelectField(u'İstiyorum?', choices=[('False', u'Vermek'), ('True', u'Almak')])

    def fill_form(self, stuff):
        self.tags.data = ''
        self.title.data = stuff.title
        self.detail.data = stuff.detail
        self.stuffid.data = stuff.id
        self.address.data = stuff.address_id
        self.stuff_type.data = stuff.type_id
        self.category.data = stuff.category_id
        self.is_wanted.data = str(stuff.is_wanted)

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True

class SeachForm(Form):
    stuff = TextField(u'Ne arıyorsun?', [
        validators.Length(min=0, max=255)
    ])

    address = TextField(u'Nerede arıyorsun?', [
        validators.Length(min=0, max=255)
    ])
    submit = SubmitField("Ara")

class ConversationForm(Form):
    message = TextAreaField(u'Mesaj Yaz', [
        validators.Length(min=0, max=1000),
        validators.Required()
    ])

    submit = SubmitField(u"Gönder")

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            print 'not OK'
            return False

        return True

class InvitationForm(Form):
    emails = TextField(u'a@b.com, ...', [
        validators.email(),
        validators.Required()
    ])

    message = TextAreaField(u'Eşyakütüphanesine sen de katıl :)', [
        validators.Length(min=0, max=1000),
        validators.Required()
    ])

    submit = SubmitField(u"Davet et")

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True

class RequestForm(Form):
    message = TextField(u'Mesaj yaz', [
        validators.Length(min=0, max=1000),
        validators.Required()
    ])

    duration = TextField('', [
        validators.Length(min=0, max=4),
    ])

    unit = SelectField('', coerce=int, choices=[(1, u'Gün'),
                                                (7, u'Hafta')])
    stuff_id = HiddenField()

    submit = SubmitField(u"Gönder")

class CreateGroupForm(Form):
    group_name = TextField(u'Grup adı', [
        validators.Length(min=2, max=100),
        validators.Required()
    ])

    text = TextAreaField(u'Bu grubu neden kurmak istiyorsun?', [
        validators.Length(min=0, max=1000),
        validators.Required()
    ])

    submit = SubmitField(u"Gönder")

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True