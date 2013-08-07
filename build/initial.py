from ek import db
from models import users, Role

roles = {'admin': 'admin',
         'member': 'member',
         }

users_list = [
    {'email': 'yigiit@gmail.com', 'password': 'ekek', 'name': 'yigit', 'roles': [roles['admin']], 'nickname':'yigit'},
    {'email': 'umutcanonal@gmail.com', 'password': 'ekek', 'name': 'umut', 'roles': [roles['admin']], 'nickname':'umutcan'},
    {'email': 'aysu@esyakutuphanesi.com', 'password': 'ekek', 'name': 'aysu', 'roles': [roles['admin']], 'nickname':'aysu'},
    {'email': 'ayse@esyakutuphanesi.com', 'password': 'ekek', 'name': 'ayse', 'roles': [roles['admin']], 'nickname':'ayse'},
    ]


db.create_all()

for role_name in roles.values():
    role = Role(name=role_name)
    db.session.add(role)

db.session.commit()

for user in users_list:
    new_user = users.create_user(email=user.get('email'),
                                 password=user.get('password'),
                                 name=user.get('name'),
                                 nickname=user.get('nickname')
                                 )

    for role in user.get('roles'):
        role_db = Role.query.filter_by(name=role).first()

        new_user.roles.append(role_db)

    db.session.add(new_user)

db.session.commit()
