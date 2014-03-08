# coding=utf-8
from ek import db
from models import users, Role, User, Address, Stuff, Conversation, Message, Request, Connection
db.drop_all()
roles = {'admin': 'admin',
         'member': 'member',
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