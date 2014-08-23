import json

from flask.ext.script import Manager, prompt_bool
from sqlalchemy.exc import OperationalError

from esyakutuphanesi import db

from esyakutuphanesi.models import Role, Category, StuffType, users

manager = Manager(usage="Perform database operations")


@manager.option('-s', '--sample-data', dest='sample_data', default='yes')
def create(sample_data):
    "Creates database tables from sqlalchemy models"

    db.create_all()
    print("Tables were created.")

    if sample_data.lower()[0] is "y":
        populate()


@manager.command
def drop():
    "Drops database tables"
    if prompt_bool("Are you sure you want to lose all your data? ('y' or 'n')"):
        db.drop_all()
        print("All tables were dropped.")


@manager.option('-s', '--sample-data', dest='sample_data', default='yes')
def recreate(sample_data):
    "Recreates database tables (same as issuing 'drop' and then 'create')"
    drop()
    create(sample_data)


@manager.command
def populate(sample_data=True):
    "Populate database with default data"

    files = {
        "roles_file": "sample_data/roles.json",
        "users_list_file": "sample_data/users_list.json",
        "categories_file": "sample_data/categories.json",
        "stuff_types_file": "sample_data/stuff_types.json",
    }

    with open(files["roles_file"]) as roles_file:
        roles = json.loads(roles_file.read())

    with open(files["users_list_file"]) as users_list_file:
        users_list = json.loads(users_list_file.read())

    with open(files["categories_file"]) as categories_file:
        categories = json.loads(categories_file.read())

    with open(files["stuff_types_file"]) as stuff_types_file:
        stuff_types = json.loads(stuff_types_file.read())

    try:
        for role_name in roles.values():
            role = Role(name=role_name)
            db.session.add(role)

        db.session.commit()

        # Sample user password is "ekekek"
        for user in users_list:
            new_user = users.create_user(
                email=user.get('email'),
                password=user.get('password'),
                name=user.get('name'),
                approved=user.get('approved')
            )

            for role in user.get('roles'):
                role_db = Role.query.filter_by(name=role).first()

                new_user.roles.append(role_db)

            db.session.add(new_user)

        db.session.commit()

        for category in categories:
            new_category = Category(name=category)
            db.session.add(new_category)
            if category in stuff_types:
                for stuff_type in stuff_types[category]:
                    new_type = StuffType(name=stuff_type)
                    db.session.add(new_type)
                    new_category.type_list.append(new_type)
            else:
                new_type = StuffType(name=category)
                db.session.add(new_type)
                new_category.type_list.append(new_type)

        db.session.commit()

        print("Database was populated with sample data.")

    except OperationalError, e:
        print str(e)
        print("Did you create the database?")

    except Exception, e:
        print str(e)
