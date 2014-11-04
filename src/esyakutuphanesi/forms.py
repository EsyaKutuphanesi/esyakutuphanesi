# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms import TextField, HiddenField, PasswordField, validators, SubmitField
from wtforms import TextAreaField, SelectField, FileField

from models import User


class EditUserForm(Form):
    userid = HiddenField('userid')
    photo = FileField(u'Resim Yükle')
    name = TextField(u'İsim', [
        validators.Length(min=4, max=25, message=u'En az 4, en fazla 25 karakter girebilirsin.'),
        validators.Required(u'İsmini girmelisin.')
    ])
    email = TextField(u'Email Adresi', [
        validators.Length(min=6, max=35),
        validators.Required(u'Email adresini girmelisin.')
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
        if user and user.id != int(self.userid.data):
            self.email.errors.append(u'Bu email adresi ile kayıtlı bir kullanıcı bulunuyor.')
            return False

        return True


class EditStuffForm(Form):
    stuffid = HiddenField('stuffid')
    photo = FileField(u'Resim Yükle')
    title = TextField(u'Başlık *', [
        validators.Length(min=4, max=255, message=u'Eşyanın başlığı en az 4 karakter olmalı.'),
        validators.Required(u'Eşya için başlık girmelisin.')
    ])
    detail = TextAreaField(u'Detaylar', [
        validators.Length(min=0, max=1000, message=u'En fazla 1000 karaktere kadar açıklama girebilirsin.')
        # validators.Required()
    ])
    address = SelectField(u'Adres *', coerce=int, validators=[validators.Required()])
    group = SelectField(u'Grup', coerce=int, validators=[validators.Required()])
    submit = SubmitField(u"Tamamla")
    delete = SubmitField(u"Eşyayı kaldır")
    tags = TextField(u'Etiketler', [
        validators.Length(min=0, max=255, message=u'En fazla 255 karaktere kadar etiket girebilirsin.')
    ])
    category = SelectField(u'Kategori *', coerce=int, validators=[validators.Required()])
    stuff_type = SelectField(u'Eşya Türü', coerce=int)
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
                message = u'Haritada bir nokta işaretlemen lazım. ' \
                          u'Adres girip ara\'ya bas veya ' \
                          u'sağ tıklayıp bir nokta seç.'
                self.address_str.errors.append(message)
                return False
        return True


class EditAddressForm(Form):
    addressid = HiddenField('addressid')
    address_title = TextField(u'Adres ismi', [
        validators.Length(min=1, max=255, message=u'Adresin ismi en az 4 karakter olmalı.'),
        validators.Required(u'Adres için isim girmelisin.')
    ])
    lat = HiddenField('lat')
    lng = HiddenField('lng')

    address_str = TextField(u'Adres')
    submit = SubmitField(u"Tamamla")

    def fill_form(self, address):
        self.address_title.data = address.name
        self.address_str.data = address.detail
        self.addressid.data = address.id
        self.lat.data = address.lat
        self.lng.data = address.lng
        self.addressid.data = address.id

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True


class SearchForm(Form):
    stuff = TextField(u'Ne arıyorsun?', [
        validators.Length(min=0, max=255, message=u'En fazla 255 karakter girebilirsin.')
    ])

    address = TextField(u'Nerede arıyorsun?', [
        validators.Length(min=0, max=255, message=u'En fazla 255 karakter girebilirsin.')
    ])
    submit = SubmitField("Ara")


class ConversationForm(Form):
    message = TextAreaField(u'Mesaj Yaz', [
        validators.Length(min=0, max=1000, message=u'En fazla 1000 karakter girebilirsin.'),
        validators.Required(u'Mesajını girmelisin.')
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
        validators.Required(u'E-posta adresini girmelisin.')
    ])

    message = TextAreaField(u'Eşya Kütüphanesine sen de katıl :)', [
        validators.Length(min=0, max=1000, message=u'En fazla 1000 karakter girebilirsin.'),
        validators.Required(u'Mesajını girmelisin.')
    ])

    submit = SubmitField(u"Davet et")

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True


class RequestForm(Form):
    message = TextAreaField(u'Mesaj yaz', [
        validators.Length(min=0, max=1000, message=u'En fazla 1000 karakter girebilirsin.'),
        validators.Required(u'Mesajını girmelisin.')
    ])

    duration = TextField('', [
        validators.Length(min=0, max=4),
        validators.Required(u'Ne kadar süre istediğini girmelisin.')
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
        validators.Length(min=2, max=1000, message=u'En fazla 1000 karakter girebilirsin.'),
    ])

    # rating = RadioField(
    #     u'Puan',
    #     coerce=int,
    #     choices=[(1, u'1'),
    #           (2, u'2'),
    #           (3, u'3'),
    #           (4, u'4'),
    #           (5, u'5')
    #     ]
    # )

    request_id = HiddenField()

    submit = SubmitField(u"Gönder")

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True


class ContactForm(Form):
    user_name = TextField(u'İsmin Soyismin', [
        validators.Required(u'İsmini girmelisin.')
    ])

    user_email = TextField(u'E-posta adresin', [
        validators.email(),
        validators.Required(u'E-posta adresini girmelisin.')
    ])

    message = TextAreaField(u'Sen yaz biz okuyalım', [
        validators.Length(min=0, max=1000, message=u'En fazla 1000 karakter girebilirsin.'),
        validators.Required(u'Bu alanı doldurmalısın.')
    ])

    submit = SubmitField(u"Gönder")

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        return True
