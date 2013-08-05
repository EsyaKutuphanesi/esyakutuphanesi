from ek import db
from models import users

db.create_all()
users.create_user(email='yigiit@gmail.com', password='ekek', name='yigit')
db.session.commit()
