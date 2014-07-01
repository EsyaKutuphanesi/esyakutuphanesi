# coding=utf-8
from ek import db
from models import users, Role, User,Address, Stuff,\
    Conversation, Message, Request, Connection, Category, StuffType,\
    Group, GroupMembership

db.drop_all()
roles = {'admin': 'admin',
         'member': 'member',
         'moderator': 'moderator'
         }
# şifre 3 kere ek
users_list = [
    {'email': 'yigiit@gmail.com',
     'password': "$5$rounds=80000$Yj2S6AtoBQ7mOmuZ$gevIsEG8fTUw92bAfRJw9YQxdyq.0VRkKB3xvoi3cb/",
     'name': 'yigit', 'roles': [roles['admin']]},
    {'email': 'umutcanonal@gmail.com',
     'password': "$5$rounds=80000$Yj2S6AtoBQ7mOmuZ$gevIsEG8fTUw92bAfRJw9YQxdyq.0VRkKB3xvoi3cb/",
     'name': 'umut', 'roles': [roles['admin']]},
    {'email': 'aysu@esyakutuphanesi.com',
     'password': "$5$rounds=80000$Yj2S6AtoBQ7mOmuZ$gevIsEG8fTUw92bAfRJw9YQxdyq.0VRkKB3xvoi3cb/",
     'name': 'aysu', 'roles': [roles['admin']]},
    {'email': 'ayse@esyakutuphanesi.com',
     'password': "$5$rounds=80000$Yj2S6AtoBQ7mOmuZ$gevIsEG8fTUw92bAfRJw9YQxdyq.0VRkKB3xvoi3cb/",
     'name': 'ayse', 'roles': [roles['admin']]},
    ]

"""
adress_list = [
    {'lat':'40.996427', 'lng':'29.033614','user':['umutcan']}
]
addresses = {
    'umutcan':[{'lat':'40.996427', 'lng':'29.033614','name':'acibadem','detail':u'acıbadem mh. ömer cemalbey sokak istanbul'}]
}
"""
db.create_all()

for role_name in roles.values():
    role = Role(name=role_name)
    db.session.add(role)

db.session.commit()

for user in users_list:
    new_user = users.create_user(email=user.get('email'),
                                 password=user.get('password'),
                                 name=user.get('name')
                                 )

    for role in user.get('roles'):
        role_db = Role.query.filter_by(name=role).first()

        new_user.roles.append(role_db)

    db.session.add(new_user)

db.session.commit()
"""
for email in addresses:
    owner = User.query.filter(User.email==email).one()
    for address in addresses[email]:
        new_address = Address(user=owner,
                              lat=address.get('lat'),
                              lng=address.get('lng'),
                              detail=unicode(address.get('detail')),
                              name=address.get('name'))
    db.session.add(new_address)
"""
db.session.commit()

categories = [u'Bebek ve çocuk', u'Doğada ve sporda', u'Elektronik', u'Giysi dolabı', u'Hırdavat', u'Keyiflik',
              u'Kütüphane', u'Mobilya', u'Mutfak']
stuff_types =  {
    u'Doğada ve Sporda': [u' Hayvan dostu', u'Spor malzemeleri', u'Ulaşım', u'Yolda'],
    u'Elektronik': [u'Ev elektroniği' ,u'Bilgisayar', u'Beyaz eşya', u'Telefon'],
    u'Giysi dolabı': [u'Ayakkabı', u'Giysi', u'Gelinlik', u'Özel günlerde'],
    u'Keyiflik': [u'Film',u'Müzik',u'Oyun',u'Konsol oyunları'],
    u'Kütüphane': [u'Roman', u'Dergi', u'Teknik kitap']
}

for category in categories:
    new_category = Category(name=category)
    db.session.add(new_category)
    if category in stuff_types:
        for stuff_type in stuff_types[category]:
            new_type = StuffType(name=stuff_type)
            db.session.add(new_type)
            new_category.type_list.append(new_type)

db.session.commit()
