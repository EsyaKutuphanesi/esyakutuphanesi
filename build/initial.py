from ek import db
from models import users, Role

roles = {'admin': 'admin',
         'member': 'member',
         }

users_list = [
    {'email': 'yigiit@gmail.com', 'password': 'ekek', 'name': 'yigit', 'roles': [roles['admin']]},
    {'email': 'umutcanonal@gmail.com', 'password': 'ekek', 'name': 'umut', 'roles': [roles['admin']]},
    {'email': 'aysu@esyakutuphanesi.com', 'password': 'ekek', 'name': 'aysu', 'roles': [roles['admin']]},
    {'email': 'ayse@esyakutuphanesi.com', 'password': 'ekek', 'name': 'ayse', 'roles': [roles['admin']]},
    ]


db.create_all()

for role_name in roles.values():
    role = Role(name=role_name)
    db.session.add(role)

db.session.commit()

for user in users_list:
    new_user = users.create_user(email=user.get('email'), password=user.get('password'), name=user.get('name'))

    for role in user.get('roles'):
        role_db = Role.query.filter_by(name=role).first()

        new_user.roles.append(role_db)

    db.session.add(new_user)

db.session.commit()
