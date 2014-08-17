from ek import db
from models import users, Role, Category, Thing, User, Object

roles = {'admin': 'admin',
         'member': 'member',
         }

users_list = [
    {
        'email': 'yigiit@gmail.com',
        'password': 'ekek',
        'name': 'yigit',
        'roles': [roles['admin']],
        'nickname':'yigit'
    },
    {
        'email': 'umutcanonal@gmail.com',
        'password': 'ekek',
        'name': 'umut',
        'roles': [roles['admin']],
        'nickname':'umutcan'
    },
    {
        'email': 'aysu@esyakutuphanesi.com',
        'password': 'ekek',
        'name': 'aysu',
        'roles': [roles['admin']],
        'nickname':'aysu'
    },
    {
        'email': 'ayse@esyakutuphanesi.com',
        'password': 'ekek',
        'name': 'ayse',
        'roles': [roles['admin']],
        'nickname':'ayse'
    },
]

categories = ['sports', 'music instruments']

things = {
    'tandem bike': ['sports'],
    'didgeridoo': ['music instruments'],
}

objects = {
    'yigit': ['tandem bike'],
    'umutcan': ['didgeridoo'],
}

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


for category in categories:
    new_category = Category(name=category)
    db.session.add(new_category)

db.session.commit()

for thing in things:
    new_thing = Thing(name=thing)
    for category in things[thing]:
        new_category = Category.query.filter(Category.name == category).one()
        new_thing.categories.append(new_category)
    db.session.add(new_thing)
db.session.commit()

for user in objects:
    owner = User.query.filter(User.nickname == user).one()
    for object in objects[user]:
        thing = Thing.query.filter(Thing.name == object).one()
        new_object = Object(owner=owner, thing=thing)
    db.session.add(new_object)
db.session.commit()
