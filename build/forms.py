# coding=utf-8

from flask.ext.wtf import Form
from wtforms import TextField, HiddenField, PasswordField, validators, SubmitField
from wtforms import TextAreaField, SelectField, FileField, RadioField

from models import User

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
        # validators.Required()
    ])
    address = SelectField(u'Adres', coerce=int, validators=[validators.Required()])
    group = SelectField(u'Grup', coerce=int, validators=[validators.Required()])
    submit = SubmitField("Kaydet")
    delete = SubmitField("Eşyayı kaldır")
    tags = TextField(u'Etiketler',[
        validators.Length(min=0, max=255)
    ])
    category = SelectField('Kategori', coerce=int, validators=[validators.Required()])
    stuff_type = SelectField(u'Eşya Türü', coerce=int, validators=[validators.Required()])
    is_wanted = SelectField(u'İstiyorum?', choices=[('False', u'Vermek'), ('True', u'Almak')])
    address_str = TextField('')

    lat = HiddenField('lat')
    lng = HiddenField('lng')
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

        if self.address.data == -1:
            if not (self.lat.data and
                    self.lng.data and
                    self.address_str.data):
                print 'sec'
                message = u'Haritada bir nokta işaretlemeniz lazım. ' \
                          u'Adres girip ara\'ya basın veya ' \
                          u'sağ tıklayıp bir nokta seçin.'
                self.address_str.errors.append(message)
                return False
        return True

class SearchForm(Form):
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
    message = TextAreaField(u'Mesaj yaz', [
        validators.Length(min=0, max=1000),
        validators.Required()
    ])

    duration = TextField('', [
        validators.Length(min=0, max=4),
        validators.Required()
    ])

    unit = SelectField('', coerce=int, choices=[(1, u'Gün'),
                                                (7, u'Hafta')])
    stuff_id = HiddenField()
    is_wanted = HiddenField()

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

class ReviewForm(Form):
    comment = TextAreaField(u'Yorum', [
        validators.Length(min=2, max=1000),
    ])

    # rating = RadioField(u'Puan', coerce=int,
    #                     choices=[(1, u'1'),
    #                              (2, u'2'),
    #                              (3, u'3'),
    #                              (4, u'4'),
    #                              (5, u'5')])

    request_id = HiddenField()

    submit = SubmitField(u"Gönder")

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True

class ContactForm(Form):
    user_name = TextField(u'İsmin Soyismin', [
        validators.Required()
    ])

    user_email = TextField(u'E-posta adresin', [
        validators.email(),
        validators.Required()
    ])

    message = TextAreaField(u'Sen yaz biz okuyalım', [
        validators.Length(min=0, max=1000),
        validators.Required()
    ])

    submit = SubmitField(u"Gönder")

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True