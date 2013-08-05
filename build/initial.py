from ek import db
from models import users

users_list = [
    {'email': 'yigiit@gmail.com', 'password': 'ekek', 'name': 'yigit'},
    {'email': 'umutcanonal@gmail.com', 'password': 'ekek', 'name': 'umut'},
    {'email': 'aysu@esyakutuphanesi.com', 'password': 'ekek', 'name': 'aysu'},
    {'email': 'ayse@esyakutuphanesi.com', 'password': 'ekek', 'name': 'ayse'},
    ]

db.create_all()

for user in users_list:
    users.create_user(email=user.get('email'), password=user.get('password'), name=user.get('name'))

db.session.commit()
